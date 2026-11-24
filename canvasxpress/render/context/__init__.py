"""
The context package provides the HTML, CSS and JavaScript shared by the renderers
in `canvasxpress.render` to put CanvasXpress charts into each runtime context.

- `CXLibraryAssets`: the CanvasXpress library, stylesheet and license.
- `CXChartAssets`: the canvas element and initialization JavaScript of a chart.
- `CXHtmlDocument`: arranges charts and provides them as a page, a fragment, or
  separate parts, optionally following the width and/or height of their
  container (`fill_to_width`, `fill_to_height`, implemented by `FILL_JS`).
- `temp_directory()`, `page_file_name()` and `write_html_file()`: where pages are
  written and what they are called.
"""

from canvasxpress.render.context.assets import (
    FILL_JS,
    LOADER_JS,
    CXChartAssets,
    CXLibraryAssets,
    escape_script,
    fill_container_js,
    fill_options,
    script_element,
)
from canvasxpress.render.context.document import (
    DEFAULT_GAP,
    LIBRARY_LOADER,
    LIBRARY_MODES,
    LIBRARY_NONE,
    LIBRARY_TAGS,
    CXHtmlDocument,
)
from canvasxpress.render.context.files import (
    ANONYMOUS_NAME,
    MAX_FILE_STEM,
    page_file_name,
    temp_directory,
    write_html_file,
)

__all__ = [
    "FILL_JS",
    "LOADER_JS",
    "CXChartAssets",
    "CXLibraryAssets",
    "escape_script",
    "fill_container_js",
    "fill_options",
    "script_element",
    "DEFAULT_GAP",
    "LIBRARY_LOADER",
    "LIBRARY_MODES",
    "LIBRARY_NONE",
    "LIBRARY_TAGS",
    "CXHtmlDocument",
    "ANONYMOUS_NAME",
    "MAX_FILE_STEM",
    "page_file_name",
    "temp_directory",
    "write_html_file",
]
