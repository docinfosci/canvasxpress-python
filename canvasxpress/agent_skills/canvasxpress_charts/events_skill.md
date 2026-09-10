---
name: events
description: CanvasXpress event handling including the complete event catalog, event handler patterns using JavaScript context variables (o, e, t), Shiny integration, dynamic event listeners, and post-render function calls. Use when creating interactive charts with custom click/hover/select behaviors, tooltips, effects, or any interactive event handling.
---

# Events & Interactivity

## Required Imports

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.js.function import CXEvent
from canvasxpress.js.collection import CXEvents
from canvasxpress.plot import graph
```

> **Note:** Use `CXEvent` for a single event or `CXEvents` to wrap multiple events. CanvasXpress accepts both `CXEvent` and `CXEvents` as the `events` parameter.

## Trigger Keywords

Route to this skill when the user mentions: `event`, `events`, `click`, `hover`, `tooltip`, `effect`, `interactive`, `interaction`, `handler`, `callback`, `onclick`, `mouseover`, `mousemove`, `selection`, `dynamic`.

## Event Handler Signature

Every event handler receives three arguments via JavaScript context variables:

```python
# script uses: o (data object), e (DOM event), t (CanvasXpress instance)
# CRITICAL: The script must ONLY use these three variables: o, e, t
# DO NOT use any other variables, parameters, or identifiers
# Keep in mind:
# - o contains chart-specific data (e.g., o.y.vars[0], o.y.smps[0])
# - e has native DOM properties (e.clientX, e.clientY, e.ctrlKey)
# - t is the full CanvasXpress API (t.showInfoSpan(), t.zoom(), etc.)
# IMPORTANT: Use the same data variables already defined in the chart's data parameter
```

## Complete Event Catalog

| Event | Description |
|---|---|
| `click` | Data element clicked |
| `clicklegend` | Legend item clicked |
| `contextmenu` | Right-click (prevent default for custom menu) |
| `dblclick` | Double-click |
| `drag` | During drag operation |
| `enddragnode` | Network node drag finished |
| `enddraw` | Rendering complete |
| `motion` | Motion complete (motion charts only) |
| `mousemove` | Mouse moving over chart elements |
| `mouseout` | Mouse left chart elements |
| `mouseover` | Mouse entered a data element |
| `mouseup` | Mouse button released |
| `remote` | Chart updated by remote source |
| `select` | Data points selected |
| `wheel` | Mouse wheel over chart |

## Basic Event Examples

```python
# Single event
events = CXEvent(
    id="click",
    script="var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0]; t.showInfoSpan(e, s);"
)

cx = CanvasXpress(data=data, config={"graphType": "Bar"}, events=events)
graph(cx)
```

> **Important:** CXEvent uses `script=` parameter (not `handler=`). The `script` parameter contains JavaScript code that will be wrapped in `function(o, e, t){...}`. The `id` parameter is the name of the JavaScript event to listen for (e.g., `"click"`, `"mouseover"`, `"mousemove"`).

```python
# Multiple events using CXEvents
events = CXEvents(
    CXEvent(
        id="click",
        script="var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0]; t.showInfoSpan(e, s);"
    ),
    CXEvent(
        id="mousemove",
        script="t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');"
    )
)

cx = CanvasXpress(data=data, config={"graphType": "Bar"}, events=events)
graph(cx)
```

## CRITICAL: JavaScript Constraints

CXEvent wraps the script in `function(o, e, t) { ... }`. You MUST adhere to these constraints:

1. **ONLY use `o`, `e`, `t` in the script** - These are the only variables available
2. **DO NOT declare new parameters** - The wrapper provides `o`, `e`, `t`
3. **DO NOT use arrow functions with custom parameters** - Use `function(o, e, t)` style
4. **Use the data already defined in the chart** - Reference `o.y.vars`, `o.y.smps`, `o.z`, `o.x` to access chart data

```python
# CORRECT - uses only o, e, t
CXEvent(id="click", script="var msg = o.y.vars[0]; t.showInfoSpan(e, msg);")

# INCORRECT - declares extra parameters
CXEvent(id="click", script="(function(myData, myEvent) { ... })")

# INCORRECT - uses undefined variables
CXEvent(id="click", script="var x = someOtherFunction(); t.showInfoSpan(e, x);")

# CORRECT - reuses data from chart's data parameter
# If chart data uses 'Gene1', 'Gene2' as vars, reference them via o.y.vars
```

> **CRITICAL: NEVER generate raw JavaScript objects or functions for events.**
> CanvasXpress Python code must ALWAYS use `CXEvent(id="...", script="...")` pattern.
> The `script` string is automatically wrapped in `function(o, e, t){...}` by CanvasXpress.
> 
> **ABSOLUTELY NEVER use these patterns:**
> ```python
> # ABSOLUTELY WRONG - raw JavaScript object
> events = {"click": "function(dat, el) { ... }"}
> 
> # ABSOLUTELY WRONG - inline JavaScript function pattern
> events = {"click": """function(dat, el) { ... }"""}
> 
> # ABSOLUTELY WRONG - nested dict structure with callback
> events = {"onClickData": {"callback": "function(data, chart) { ... }"}}
> 
> # ABSOLUTELY WRONG - custom function signature in script
> events = CXEvent(id="click", script="function(myData, myEvent) { ... }")
> 
> # ABSOLUTELY WRONG - using alert() for display
> events = CXEvent(id="click", script="alert('Hello');")
> ```
> 
> **ALWAYS use this pattern:**
> ```python
> # ALWAYS - single event
> events = CXEvent(id="click", script="var msg = o.y.vars[0]; t.showInfoSpan(e, msg);")
> 
> # ALWAYS - multiple events with CXEvents
> events = CXEvents(
>     CXEvent(id="click", script="var msg = o.y.vars[0]; t.showInfoSpan(e, msg);"),
>     CXEvent(id="mousemove", script="t.hideInfoSpan();")
> )
> ```
> 
> **Remember:** The CanvasXpress Python API does NOT accept raw JavaScript objects. Only `CXEvent` objects or lists of `CXEvent` objects.

## Using Chart Data in Events

Events should leverage the data already defined in the chart's `data` parameter:

```python
# Data already defined for the chart
df = pd.DataFrame({
    'GeneA': [10, 20, 30],
    'GeneB': [15, 25, 35],
    'Sample': ['S1', 'S2', 'S3']
})

cx = CanvasXpress(
    data=df,
    config={"graphType": "Heatmap", "title": "Gene Expression"},
    events=CXEvents(
        CXEvent(
            id="click",
            # Use o.y.vars and o.y.smps to access the data already in the chart
            script="var gene = o.y.vars[0]; var sample = o.y.smps[0]; t.showInfoSpan(e, gene + ' in ' + sample);"
        )
    )
)
```

When converting from other libraries or creating tooltips:
- Use `o.y.vars` to access variable names from the chart's data
- Use `o.y.smps` to access sample names from the chart's data
- Use `o.z` to access sample/variable annotations from the chart's data
- Use `o.x` to access additional data dimensions from the chart's data

## Common Mistakes

### Wrong Import Location
```python
# WRONG - CXEvents is not in function module
from canvasxpress.js.function import CXEvent, CXEvents

# CORRECT - Only import CXEvent from function
from canvasxpress.js.function import CXEvent
# CXEvents (if needed) would be: from canvasxpress.js.collection import CXEvents
```

### Forgetting to Wrap Events
```python
# WRONG - CXEvent must be wrapped in CXEvent or CXEvents
events = [CXEvent(id="click", script="...")]  # Don't use lists

# CORRECT - single event
events = CXEvent(id="click", script="...")

# CORRECT - multiple events
events = CXEvents(CXEvent(id="click", script="..."), CXEvent(id="mousemove", script="..."))
```

### Using Undefined Variables in Scripts
```python
# WRONG - uses variables not provided by CanvasXpress
CXEvent(id="click", script="var x = myFunction(); console.log(x);")

# CORRECT - only use o, e, t
CXEvent(id="click", script="console.log(o.y.vars[0]);")
```

### Wrong Event ID Values
```python
# WRONG - invalid event names
CXEvent(id="onClick", script="...")     # Python style
CXEvent(id="hover", script="...")       # Not a CanvasXpress event
CXEvent(id="onClickData", script="...") # Not a CanvasXpress event

# CORRECT - use CanvasXpress event names
CXEvent(id="click", script="...")       # Valid
CXEvent(id="mouseover", script="...")   # Valid
CXEvent(id="mousemove", script="...")   # Valid
```

### Generating Nested Dict Structures
```python
# WRONG - nested dict with callback
events = {"onClickData": {"callback": "function(data, chart) { ... }"}}

# CORRECT - use CXEvent
events = CXEvent(id="click", script="var msg = o.y.vars[0]; t.showInfoSpan(e, msg);")
```

### Not Checking for null Data Object
```python
# WRONG - crashes when dataObject is null (e.g., clicking background)
CXEvent(id="click", script="var s = o.y.vars[0]; t.showInfoSpan(e, s);")

# CORRECT - check if data object exists first
CXEvent(id="click", script="if (o && o.y) { var s = o.y.vars[0]; t.showInfoSpan(e, s); }")
```

## Event Handler Organization Pattern

For complex applications with multiple events, use `CXEvents`:

```python
events = CXEvents(
    CXEvent(id="click", script="/* handler code */"),
    CXEvent(id="mousemove", script="/* handler code */"),
    CXEvent(id="mouseout", script="/* handler code */"),
    CXEvent(id="dblclick", script="/* handler code */"),
)
```

## Dynamic Event Listeners (Post-Render)

Add or remove events after the chart is created:

```python
# After getting the chart instance:
# cx_instance = graph(cx)

# Add events dynamically
# cx_instance.addEventListener('click', handler_function)
# cx_instance.removeEventListener('click', handler_function)
```

## Shiny Integration Events

Trigger backend reactions from chart interactions:

```python
CXEvent(
    id="click",
    script="Shiny.setInputValue('point_selected', o.y);"
)
```

## Post-Render Function Calls

Apply transformations after initial render:

```python
cx = CanvasXpress(
    data=data,
    config={"graphType": "Bar"},
    after_render=[
        ["createRegression", [True, "Hip"]],   # Add regression
        ["pivotX", ["Gender"]],                 # Pivot by metadata
        ["createDOE", []]                       # Create DOE dashboard
    ]
)
graph(cx)
```

## Programmatic Chart Control

Access chart instance methods from event handlers:

```python
CXEvent(
    id="click",
    script="""
        // t is the CanvasXpress instance
        t.zoom();              // Zoom to fit
        t.filterSamples();     // Open filter panel
        // t.destroy();        // Destroy chart
    """
)
```

## Creating Tooltips with Events

For tooltips and hover effects, use `mousemove` or `mouseover` events with `t.showInfoSpan()`:

```python
# Simple tooltip showing data on hover
cx = CanvasXpress(
    data=df,
    config={"graphType": "Bar", "title": "Sales Data"},
    events=CXEvents(
        CXEvent(
            id="mousemove",
            # Tooltip using only o, e, t - accessing data from chart
            script="t.showInfoSpan(e, '<b>' + o.y.vars[0] + '</b>: ' + o.y.data[0][o.y.smps.indexOf(o.y.smps[0])]);"
        ),
        CXEvent(
            id="mouseout",
            script="t.hideInfoSpan();"
        )
    )
)
```

## Complete Events Template

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.js.function import CXEvent
from canvasxpress.plot import graph

# Single event - can pass directly
cx = CanvasXpress(
    data=data,
    config={"graphType": "Scatter2D", "title": "Interactive Chart"},
    events=CXEvent(
        id="click",
        script="var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0]; t.showInfoSpan(e, s);"
    )
)
graph(cx)

# Multiple events - use a list
cx = CanvasXpress(
    data=data,
    config={"graphType": "Scatter2D", "title": "Interactive Chart"},
    events=[
        CXEvent(
            id="click",
            script="var s = 'click on var ' + o.y.vars[0] + ' and smp ' + o.y.smps[0]; t.showInfoSpan(e, s);"
        ),
        CXEvent(
            id="mousemove",
            script="t.showInfoSpan(e, '<pre>' + t.prettyJSON(o) + '</pre>');"
        ),
        CXEvent(
            id="select",
            script="console.log('Selection made:', o);"
        )
    ]
)
graph(cx)
```

## Validation and Testing

When generating event code, use `convert_to_reproducible_json()` for headless testing instead of `graph()`:

```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.js.function import CXEvent
from canvasxpress.plot import convert_to_reproducible_json

cx = CanvasXpress(
    data=data,
    config={"graphType": "Bar"},
    events=CXEvent(id="click", script="var s = 'test'; t.showInfoSpan(e, s);")
)

# This validates the CanvasXpress object without requiring a browser/display
json_output = convert_to_reproducible_json(cx)
print(json_output)  # Validates code runs without exceptions
```

> **Why use convert_to_reproducible_json()?**
> - Works in headless environments (no browser needed)
> - Catches syntax errors, invalid configs, and event issues
> - Faster than rendering for validation
> - Returns JSON for debugging
>
> Only use `graph()` when you actually need to render the chart to a display environment.

## Validation Checklist for Event Handlers

Before presenting event handler code, verify:

- [ ] **Correct imports** - Only need `from canvasxpress.js.function import CXEvent`
- [ ] **Events accepted** - Single `CXEvent` or Python list `[CXEvent(...), ...]` both work
- [ ] **Proper structure** - Each event is a `CXEvent(id="...", script="...")` object, NOT a raw string, dict, or other format
- [ ] **Script ONLY uses `o`, `e`, `t`** variables (no other identifiers)
- [ ] **Script does NOT declare new parameters** or functions with custom arguments
- [ ] **Script references data** from the chart's existing data parameter via `o.y`, `o.x`, `o.z`
- [ ] **Variable names in script match** the actual data structure in the chart
- [ ] **Tooltips use `t.showInfoSpan(e, message)`** pattern
- [ ] **Cleanup events** (like `mouseout`) hide tooltips with `t.hideInfoSpan()`

### Event Object Validation

Every event in the generated code MUST be a properly constructed `CXEvent` object:

```python
# VALID - single CXEvent object
events = CXEvent(id="click", script="var msg = o.y.vars[0]; t.showInfoSpan(e, msg);")

# VALID - list of CXEvent objects
events = [
    CXEvent(id="click", script="var msg = o.y.vars[0]; t.showInfoSpan(e, msg);"),
    CXEvent(id="mousemove", script="t.hideInfoSpan();")
]

# INVALID - raw dict
events = {"click": "function(dat, el) { ... }"}

# INVALID - nested dict structure
events = {"onClickData": {"callback": "function(data, chart) { ... }"}}

# INVALID - raw string
events = "function(dat, el) { ... }"

# INVALID - CXEvent without proper id and script parameters
events = CXEvent(script="var msg = o.y.vars[0];")  # Missing id parameter

# INVALID - CXEvent with non-string id or script
events = CXEvent(id=123, script="var msg = o.y.vars[0];")  # id must be string
events = CXEvent(id="click", script=123)  # script must be string
```

> **Rule:** Every event must be `CXEvent(id="<string>", script="<string>")` where both `id` and `script` are strings. No raw strings, dicts, or other formats are accepted.
