# ARCHITECTURE.md

The authoritative description of the canvasxpress-python architecture, for both
human and agent contributors. Process-level detail (environment setup, build,
CI, testing) lives in `AGENTS.md` and the project skills (`.opencode/skills/`);
this document describes **how the code is organized and the rules that keep it
that way**. When a change alters anything described here, update this file in
the same change (see "Keeping this file current").

---

## 1. The Big Picture

canvasxpress-python is a Python proxy to the CanvasXpress **JavaScript**
charting library (loaded from a CDN at render time). Python objects describe a
chart — data, configuration, events, dimensions — and the package's job is to
turn that description into HTML/CSS/JavaScript in whatever context the user is
in: Jupyter, Streamlit, Dash, Shiny, RStudio, a browser page, an image, or
plain JSON.

Two invariants follow from that design:

1. **All HTML, CSS and JavaScript the package produces flows through one
   layer** — `canvasxpress/render/context/` (with its shipped JavaScript in
   `canvasxpress/render/resources/`). No renderer, display hook, or utility
   builds chart HTML or a library loader on its own.
2. **The JavaScript library is the single source of runtime truth.** The Python
   package never reimplements chart behavior; it emits a `<canvas>` element and
   a `new CanvasXpress({...})` script. Library behavior (license-before-library
   loading, element creation, resize) is owned by the JS.

---

## 2. Package Map

```
canvasxpress/
├── __init__.py              Version stamp + installs the agent skills on import
├── canvas.py                CanvasXpress: the core object (spec → HTML parts, repr, display hook)
├── plot.py                  graph(): detects the target context and dispatches to a renderer
├── data/                    The data subsystem: CXData, CXDictData, CXDataframeData, CXTextData, CXUrlData
├── config/                  The configuration subsystem: CXConfig, CXConfigs (typed config collections)
├── js/                      The event subsystem: CXEvent, CXEvents (JavaScript as first-class citizens)
├── context/
│   └── platform.py          OS and default-browser detection (for the browser popup renderer)
├── render/
│   ├── base.py              CXRenderable / CXRenderAssociation: the renderer base classes
│   ├── environment.py       CANVASXPRESS_TARGET_CONTEXT env override for graph()
│   ├── jupyter.py           CXNoteBook (IPython display objects) + inject_cx_assets()
│   ├── streamlit.py         plot(): Custom Components v2 (or iframes on old releases)
│   ├── dash.py              CXDashElement: the Dash component, defined in Python
│   ├── shiny.py             Shiny tags/outputs + render objects for Shiny and RStudio viewers
│   ├── rstudio.py           CXHtml for RStudio
│   ├── popup.py             CXBrowserPopup: saved page + local browser window
│   ├── image.py             PNG export through Node.js
│   ├── json.py              Reproducible JSON (convert_to_reproducible_json)
│   ├── context/             ★ The centralized HTML/JS/CSS layer (see §3)
│   │   ├── assets.py        CXLibraryAssets, CXChartAssets, escape_script(), script_element()
│   │   ├── document.py      CXHtmlDocument: layout, scripts, loader, fragment, page
│   │   └── files.py         temp_directory(), page_file_name(), write_html_file()
│   └── resources/           ★ JavaScript shipped with the package (see §6)
├── agent_skills/            ★ The AI agent skills shipped with the package (see §8)
└── util/                    render_from_template(), logging, version stamping
```

★ marks the layers that contributors most often misunderstand.

---

## 3. The HTML/JS/CSS Pipeline (the core rule)

Every chart that ends up in a page is built by the same chain:

```
CanvasXpress.render_to_html_parts()          # core: unescaped chart JS, <canvas>, license tag
        │
        ▼
CXChartAssets.from_canvas() / from_canvases()   # render/context/assets.py
        │  fixes anonymous-chart IDs on a copy; dedupes shared render_to IDs
        ▼
CXHtmlDocument                               # render/context/document.py
        │  grid layout, fill_to_width/fill_to_height, library mode
        ▼
page() / fragment(library) / layout_html()+scripts_html() / layout_html()+loader_js()
        │
        ▼
each renderer (jupyter, streamlit, dash, shiny, rstudio, popup, ...)
```

### 3.1 The three building blocks

| Component | Owns |
|---|---|
| `CXLibraryAssets` | The CanvasXpress library/stylesheet/license URLs. `CXLibraryAssets.current()` reads the class-level configuration (`set_js_library_url`, `set_css_library_url`, `set_cdn_edition`). `tags()` emits `<link>`/`<script>` elements for pages parsed as a whole; `loader_js(code)` wraps chart code in the shared on-demand loader for pages that are already displayed; `to_loader_dict()` is the `{jsUrl, cssUrl, licenseUrl}` argument of the JS loader |
| `CXChartAssets` | One chart's `<canvas>` element and creation JS, width, height, license. `from_canvas()` renders without changing the caller's object and **pins the ID on a copy** — an anonymous chart (no `render_to`) mints a new UUID on every access, so any code that reads `render_to` more than once without this pinning will drift. `from_canvases()` gives unique IDs to charts that share a `render_to` |
| `CXHtmlDocument` | Arranges charts in a grid (`columns`, `gap`) and provides the HTML in the four forms contexts need: `page()` (complete document), `fragment(library)` (for insertion into an existing page; `library` is `LIBRARY_NONE` / `LIBRARY_TAGS` / `LIBRARY_LOADER`), and the separate parts `layout_html()` (canvases only) plus `scripts_html()` / `chart_js()` / `loader_js()`. `fill_to_width` / `fill_to_height` (via `FILL_JS`) make charts follow their container |

### 3.2 Library modes

| Mode | How the library arrives | Used by |
|---|---|---|
| `LIBRARY_NONE` | The page already provides it (e.g. a Shiny app head); only a license tag is added | embedded contexts |
| `LIBRARY_TAGS` | `<link>` + license + library `<script>` elements precede the charts; the browser parses them in order | saved pages, Quarto/RMD documents, classic notebooks' exported pages |
| `LIBRARY_LOADER` | A `<script>` element runs `window.canvasxpress.loadLibrary(...)` from `canvasxpress-loader.js`, which loads the stylesheet, then the **license, then the library**, once per page, and only then runs the chart code | live pages that are already displayed: Jupyter outputs, Streamlit components, the repr display hook |

**There is exactly one on-demand loader** (`canvasxpress-loader.js`, exposed as
`LOADER_JS` in Python). It dedupes script loads by URL on
`window.canvasxpress._scriptLoads` so every chart in a page shares one library
load, loads the license before the library so charts are created under the
license, and reuses `window.CanvasXpress` if the page already provides it. New
code that injects library or stylesheet tags on its own is a bug; extend the
loader or use `CXLibraryAssets` instead.

### 3.3 Escaping rule

`CanvasXpress.render_to_html_parts()` returns chart JavaScript **unescaped** —
chart data may legitimately contain `</script>` (in labels, tooltips, ...). Any
JavaScript that enters a `<script>` element must go through
`escape_script()` (via `script_element()`), which writes `</script` as
`<\/script`. Rendering paths that splice chart JS into HTML text without this
step break on such data.

### 3.4 ID rules

- A chart's `render_to` is its element ID and its CanvasXpress `renderTo`.
- Anonymous charts generate a fresh UUID per access; **capture the ID once**
  (this is what `CXChartAssets.from_canvas()` does by fixing it on a copy).
- Charts that share an ID in one document get unique variants
  (`CXChartAssets.from_canvases()`, Streamlit's duplicate-ID handling).

### 3.5 Import direction

```
canvasxpress.canvas  ◄──  canvasxpress.render.*  (all of them)
canvasxpress.data/config/js  ◄──  canvasxpress.canvas
```

The core (`canvas.py`, `data/`, `config/`, `js/`, `util/`) **never imports
`canvasxpress.render` at module level** — the dependency points the other way.
Code in the core that needs the render layer (today: only
`CanvasXpress._repr_mimebundle_`) imports it **locally, inside the function**,
which is safe because such code runs at display time, not import time. Do not
"fix" this with top-level imports; it creates a cycle.

---

## 4. Entry Points

| Entry | What it does |
|---|---|
| `graph(cx, ...)` (`plot.py`) | Detects the context (installed framework extras, running app, or `CANVASXPRESS_TARGET_CONTEXT`) and dispatches to the matching renderer. The primary user API |
| The renderers (`render/*.py`) | Explicit, per-platform rendering: `CXNoteBook`, Streamlit `plot()`, `CXDashElement`, Shiny outputs, `CXHtml` (RStudio), `CXBrowserPopup`, image export |
| `CanvasXpress._repr_mimebundle_` | The IPython display hook: a `CanvasXpress` object that is the result of a notebook cell (or passed to `display()`) renders on its own. It emits `text/plain` (= `repr()`), `text/html` (`CXHtmlDocument.fragment(LIBRARY_LOADER)` — canvas + escaped shared-loader script), and `application/javascript` (`CXHtmlDocument.loader_js()` — the same loader, which is exactly what `IPython.display.Javascript` emits). It is built from the shared layer per §3, so the hook and `CXNoteBook` cannot drift. Only IPython's display machinery invokes it; plain-Python platforms are never affected |
| `render/context` directly | Advanced users build pages themselves: `CXHtmlDocument([...]).page()` / `.fragment(LIBRARY_TAGS)` |

**Display-hook rule:** new IPython representations for a chart (mime types,
`display()` behavior) are expressed through the shared layer the same way
`_repr_mimebundle_` is — never with bespoke templates in `canvas.py`.

---

## 5. How Each Platform Renders

| Platform | Renderer | Library mode | Notes |
|---|---|---|---|
| Jupyter / IPython | `CXNoteBook` + `_repr_mimebundle_` | `LIBRARY_LOADER` | Two representations per render: HTML (canvases) and `application/javascript` (shared loader). Frontends that sanitize HTML output (JupyterLab, Notebook 7) rely on the JavaScript representation, which is the one `IPython.display.Javascript` produces |
| Streamlit | `plot()` | `LIBRARY_LOADER` (in-app) | Custom Components v2 renders in the app DOM (charts share one library copy, can broadcast); iframes + `page()` on older releases. `fill_to_width`/`fill_to_height` via `FILL_JS` |
| Dash | `CXDashElement` | `LIBRARY_LOADER` (in-app) | Component defined in Python (`render/dash.py`), backed by `canvasxpress-react.js` which uses the shared loader |
| Shiny | tags/outputs in `shiny.py` | `LIBRARY_NONE` | The app head provides the library; a license is still loaded |
| RStudio | `CXHtml` | `LIBRARY_TAGS` / `LIBRARY_LOADER` | Same naming as Jupyter for `output_file` directories |
| Browser | `CXBrowserPopup` | `LIBRARY_TAGS` | Saved in a per-user temp folder, named after the charts (`files.py`), opened locally; browser/OS detection via `context/platform.py` |
| Image | `image.py` | — | PNG through Node.js + the JS library (no HTML at all) |
| JSON | `json.py` | — | `convert_to_reproducible_json`: the `{data, config, ...}` spec with no HTML/JS |

---

## 6. Shipped JavaScript Resources (`render/resources/`)

Plain JavaScript, no build step, no npm dependency; each is read into Python at
import time (`LOADER_JS`, `FILL_JS`) or served to the host page (Dash, React).
They must stay readable, ES5-compatible, and free of build tooling.

| File | Defines |
|---|---|
| `canvasxpress-loader.js` | `window.canvasxpress.loadLibrary({jsUrl, cssUrl, licenseUrl})` — the single on-demand loader (§3.2) |
| `canvasxpress-fill.js` | `window.canvasxpress.fillContainer(...)` — `fill_to_width`/`fill_to_height` via a debounced `ResizeObserver`/window resize; package behavior, distinct from the CanvasXpress `resizable` config |
| `canvasxpress-react.js` | The CanvasXpress React wrapper used by the Dash component; uses the loader |
| `canvasxpress-dash.js` | The `CXDashElement` Dash component script |

Non-Python files must be listed in `[tool.setuptools.package-data]` in
`pyproject.toml` (and `MANIFEST.in`) or they are left out of the wheel.

---

## 7. Python 3.8 Rule (applies to all package logic)

Everything under `canvasxpress/` — including the agent-skills `.py` modules —
must be pure Python 3.8: `typing.List/Dict/Optional/Union` (never `list[int]`
or `X | Y`), no `str.removeprefix()`, no `match`, no `importlib.resources.files()`
without a guarded backport (reference pattern:
`canvasxpress/agent_skills/canvasxpress_charts/__init__.py`). Version-guarded
code marks the newer-API line with `# novermin`. Enforced by ruff
(`target-version = "py38"`) and vermin; agent-skill **content** (`.md` files)
may use modern Python. Tests run on 3.8 in CI and must execute there too.
Full detail: `AGENTS.md` and the `project_development` skill.

---

## 8. Agent Skills

The package ships four skills for end-user coding agents
(`canvasxpress_charts`, `canvasxpress_events`, `canvasxpress_notebooks`,
`canvasxpress_validator`) under `canvasxpress/agent_skills/`. `canvasxpress/__init__.py`
installs/refreshes them into standard agent directories on import
(`install_skills` in `agent_skills/registry.py`). These are **product
documentation**: whenever a user-facing capability changes, the corresponding
skill content changes with it. The project's own working skills
(`project_development`, `project_testing`) live in `.opencode/skills/`, are
tracked in git, and are never installed into user directories.

---

## 9. Extension Recipes

**Add a new platform renderer.** Create `render/<platform>.py` as a thin
adapter: build the HTML/JS/CSS through `CXHtmlDocument` / `CXChartAssets` /
`CXLibraryAssets` (picking a library mode from §3.2), add the framework extra
in `pyproject.toml`, wire detection into `plot.py`, add a subskill under
`canvasxpress/agent_skills/canvasxpress_charts/`, and add platform visual tests
under `tests/functional/platform/<platform>/` (canon shared across platforms —
see `tests/functional/platform/README.md`).

**Add a representation to the IPython display hook.** Extend
`CanvasXpress._repr_mimebundle_`. The new representation must be produced by the
shared layer (§4 display-hook rule), and `text/plain` must remain `repr()` so
frontends that understand nothing new behave as before.

**Change library loading or sizing behavior.** Change
`canvasxpress-loader.js` / `canvasxpress-fill.js` (or `CXLibraryAssets`), not
the call sites. Every consumer — Jupyter, Streamlit, Dash, the display hook —
picks up the change at once.

**Add chart data/config/event types.** Work in `data/`, `config/`, `js/`; the
HTML pipeline consumes them through `render_to_html_parts()` and
`prepare_html_element_parts()`, which should stay the only two spec→HTML seams
in the core.

**Add shipped JavaScript.** Put it in `render/resources/`, list it in
`[tool.setuptools.package-data]` and `MANIFEST.in`, and read it into Python in
`render/context/assets.py` (or serve it like the Dash/React resources).

---

## 10. Keeping this file current

Update `ARCHITECTURE.md` in the same change as:

- adding, removing, or renaming a module, renderer, or shipped resource;
- changing the HTML/JS/CSS pipeline (`render/context/`, `render/resources/`),
  including new library modes, loader behavior, or escaping rules;
- changing import direction or adding a new core→render seam;
- adding or changing an IPython display representation;
- adding a skill or changing which skills ship with the package.

The corresponding docstrings and agent-skill content change in the same commit.
`AGENTS.md` remains the source for process (environment, build, CI, testing);
this document is the source for structure.
