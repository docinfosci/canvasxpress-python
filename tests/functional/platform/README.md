# Platform visual tests

These tests check that charts really appear in each live render target. For each
framework a minimal app or document is rendered in headless Chromium, the whole
browser window is captured, and the capture is compared with an approved
("canon") image.

| Folder | Render target | How it runs |
|---|---|---|
| `streamlit/` | Streamlit | `streamlit run app.py` (and `app_columns.py`) on a free local port |
| `dash/` | Plotly Dash | `python app.py` (and `app_columns.py`) on a free local port |
| `shiny/` | Shiny for Python | `shiny run app.py` (and `app_columns.py`) on a free local port |
| `jupyter/` | Jupyter | Notebooks executed headlessly (nbclient) and exported to HTML |
| `rstudio/` | RStudio (`CXHtml`) | The page `CXHtml.render(output_file=...)` saves, opened from disk |

The charts come from `charts.py`. Streamlit, Dash, Shiny and Jupyter each draw
two layouts:

- Stacked (`app.py`, or the first notebook): a bar chart at its configured
  500 x 350, above a scatter chart with `fill_to_width`. The bar chart is the
  control: it must keep its size, which shows that filling does not leak onto a
  chart that did not ask for it.
- Columns (`app_columns.py`, or the second notebook): two charts side by side in
  the framework's own columns (`st.columns`, a flex row in Dash,
  `ui.layout_columns` in Shiny, `CXNoteBook(...).render(columns=2)` in Jupyter),
  each with `fill_to_width`, so each follows the width of its column.

The RStudio page is already two charts side by side (`CXHtml.render(columns=2)`),
filling both width and height, so it has only the first layout.

Each layout is captured twice:

- `initial` (`columns_initial`): the window is 1920 x 1080 (1080p, 16:9).
- `resized` (`columns_resized`): loaded at 1920 x 1080, then resized to
  1280 x 720 (same ratio), which checks that the filling charts redraw.

Pages are captured at a device pixel ratio of 1, so a capture is the window's
size in pixels (1920 x 1080, or 1280 x 720 once resized) on every platform,
including high-density displays.

## Comparison

Each capture is the window image, `<case>.png`, and the box of each chart's
canvas on the page, `<case>.json`. A case passes when both match its canon
(constants in `visual.py`):

- Layout: every edge of every chart's box is within 4 pixels of canon
  (`LAYOUT_TOLERANCE_PX`). This shows that each chart is present, at its
  configured size, and that a filling chart follows its container.
- Image: the window is divided into 32-pixel cells, and the cells that are drawn
  on must overlap canon's by 0.85 or more (`OVERLAP_MIN`), counting the cells
  drawn on in both against those drawn on in either. This catches a chart that is
  blank or drawn wrongly, but tolerates the fonts of other platforms.

One canon per case is shared by Windows, macOS and Linux. Captures of the same
case on Windows and Linux (which substitutes other fonts for Arial) have the
same chart boxes to the pixel and overlap by 0.92 or more; a blank page overlaps
by 0, and a page missing a chart by 0.8 or less. Neither check notices a scatter
plot losing a few points, which is why a person reviews each capture before it
becomes canon.

Similarity of the whole window (SSIM) is not used: the white background
dominates it, so even a blank page scores about 0.95 against canon.

When a case does not match, the test fails, listing each chart edge that moved,
and writes `captures/<framework>/<case>.diff.png`: the capture, with cells drawn
on only in canon tinted red and only in the capture tinted blue.

## Approving canon images

A case without canon is skipped, and its capture is kept for review in
`captures/<framework>/<case>.png` and `.json` (not committed). To approve
captures:

1. Run the suite: `python -m pytest tests/functional/platform`
2. List the captures: `python -m tests.functional.platform.approve`
3. Look at each new capture. If it is right, approve it:
   `python -m tests.functional.platform.approve streamlit/initial dash/resized`,
   or `--all` for every capture.
4. Commit the approved `.png` and `.json` files in `<framework>/expected/`.

To accept an intended change in appearance, approve the new capture the same way.

## Where they run

The tests run in local builds, not in CircleCI. `build_local.sh` runs them with
the rest of the suite (`invoke test --platform`); plain `invoke test`, which
CircleCI uses, leaves them out. Run them directly with
`python -m pytest tests/functional/platform`.

They are kept out of CircleCI because they need a browser and its system
libraries on the build image, and network access to the CanvasXpress CDN. They
load the latest CanvasXpress release, so a new release can change a capture with
nothing changed in this repository.

## Requirements

The tests need the `dev` extra, which includes Playwright and scikit-image, and
Playwright's Chromium:

```shell
python -m playwright install chromium            # Windows and macOS
python -m playwright install --with-deps chromium  # Linux, with system libraries
```

The setup scripts and `build_local.sh` install Chromium. Without Playwright or
scikit-image (as on Python 3.15, see `pyproject.toml`) the tests skip; with
Playwright but no Chromium they fail with these instructions. The charts load
CanvasXpress from its CDN, so the tests need network access.
