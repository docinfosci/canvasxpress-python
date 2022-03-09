<!-- PRD Badge Location -->
# Project Status

| Topic | _main branch_ | _develop branch_ |
|---|---|---|
| **Version Info** | [![Release](https://img.shields.io/pypi/v/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | [No Badge Available for test.pypi.org](https://test.pypi.org/project/canvasxpress) |
| **Popularity** | ![PyPI - Downloads](https://img.shields.io/pypi/dm/canvasxpress) | [No Badge Available for test.pypi.org](https://test.pypi.org/project/canvasxpress) |
| **Compatibility** | [![Compatibility](https://img.shields.io/pypi/pyversions/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | [No Badge Available for test.pypi.org](https://test.pypi.org/project/canvasxpress) |
| **Implementations** | [![Implementations](https://img.shields.io/pypi/implementation/canvasxpress.svg)](https://pypi.org/project/canvasxpress) | [No Badge Available for test.pypi.org](https://test.pypi.org/project/canvasxpress) |
| **Build Status** | [![docinfosci](https://circleci.com/gh/docinfosci/canvasxpress-python/tree/main.svg?style=shield)](https://circleci.com/gh/docinfosci/canvasxpress-python/?branch=main) | [![docinfosci](https://circleci.com/gh/docinfosci/canvasxpress-python/tree/develop.svg?style=shield)](https://circleci.com/gh/docinfosci/canvasxpress-python/?branch=develop) |
| **Test Status** | [![Coverage Status](https://coveralls.io/repos/github/docinfosci/canvasxpress-python/badge.svg?branch=main)](https://coveralls.io/github/docinfosci/canvasxpress-python?branch=main) | [![Coverage Status](https://coveralls.io/repos/github/docinfosci/canvasxpress-python/badge.svg?branch=develop)](https://coveralls.io/github/docinfosci/canvasxpress-python?branch=develop) |
| **Requirements Status** | [![Requirements Status](https://requires.io/github/docinfosci/canvasxpress-python/requirements.svg?branch=main)](https://requires.io/github/docinfosci/canvasxpress-python/requirements/?branch=main) | [![Requirements Status](https://requires.io/github/docinfosci/canvasxpress-python/requirements.svg?branch=develop)](https://requires.io/github/docinfosci/canvasxpress-python/requirements/?branch=develop) |
| **Documentation Status** | [![Documentation Status](https://readthedocs.org/projects/canvasxpress-python/badge/?version=latest)](https://canvasxpress-python.readthedocs.io/en/latest/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) | [![Documentation Status](https://readthedocs.org/projects/canvasxpress-python/badge/?version=develop)](https://canvasxpress-python.readthedocs.io/en/develop/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
 |
| **Activity** | [![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/main)](https://github.com/docinfosci/canvasxpress-python) | [![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/develop)](https://github.com/docinfosci/canvasxpress-python/tree/develop) |
<!-- End Badges -->
   
## Roadmap

This package is actively maintained and developed.  Our focus for 2021 is:

### Immediate Focus

* Detailed documentation and working examples of all Python functionality

### General Focus

* Embedded CanvasXpress for JS libraries (etc.) for offline work
* Integraton with dashboard frameworks for easier applet creation
* Continued alignment with the CanvasXpress Javascript library
* Continued stability and security, if/as needed

## Recent Enhancements

#### 2021 July 6: Extensive examples for Jupyter Notebooks
Hundreds of chart examples based on the CanvasXpress site examples are now 
available in github.com at:

[tutorials/notebook/cx_site_chart_examples/](https://github.com/docinfosci/canvasxpress-python/tree/main/tutorials/notebook/cx_site_chart_examples)

#### 2021 June 30: Example code generation utility
CanvasXpress for Python now includes `generator.py`, which includes 
functions for creating example Python code to define and display charts.
`generate_canvasxpress_code_from_json` will accept a reproducible research 
JSON `str` and generate the corresponding Python code, and
`generate_canvasxpress_code_from_json_file` will accept a file path reference
to a reproducible JSON to achieve the same thing.  Find the functions at 
`canvasxoress.util.example.generator.py`.

#### 2021 June 30: Support for raw text data
CanvasXPress for Javascript can accept text data.  `CXTextData` has been added
as a means by which a `str` value can be directly provided to the CanvasXpress 
for Javascript constructor, and along with that value all assumptions about
transformation or error handling.

#### 2021 June 21: Support for reproducable research JSON
CanvasXpress for Javascript can save JSON representations of a rendered chart.
`CanvasXpress` now offers `from_reproducible_json`, which accepts such a JSON
and creates a new `CanvasXpress` object with all properties updated with the 
relevant portions of the JSON.

#### 2021 June 21: CanvasXPress __repr__ now available for example code
The `CanvasXpress` `__repr__` method now produces example Python code for
all properties of the object.  The Python built-in`eval` method can read
the provided string to reconstruct the `CanvasXpress` object when the proper
imports for the CanvasXpress packages/modules are included in the file.

### 2021 June 16: CXNoteBook accepts file paths for output
The `CXNoteBook` class now accepts a file path at which output rendered in 
Jupyter will also be captured for viewing in later sessions.  Until now a 
temporary file had be used, which remains the default behaviour.

### 2021 June 16: CXConfigs now accepts lists of values
The `CXConfigs` class can now be initialized using lists of `CXConfig` objects
or their `list/tuple` equivalents (e.g., `["label", "value"]`).  The `add` 
method supports the same formats.  Similarly, wherever the `CanvasXpress` class
accepts a `CXConfigs` object during initialization or assigment a `list` of
`CXConfig` or equivalent objects can be provided.  This is in additon to the 
already supported `dict` collections of `CXConfig` value equivalents.

### 2021 June 16: direct DataFrame support for CanvasXpress.data
The `CanvasXpress` class already supported `None`, `CXData`, and `dict` data
assignments.  Now raw `DataFrame` is supported on initialization or use of 
the `data` property.

### 2021 June 16: pop-up browser support
One or more charts can now be displayed in a new Web page using the default 
browser for the host system, assuming it is graphical (e.g., MacOS X or 
Windows).  The **A Quick Script/Console Example** below illustrates the use.

### 2021 June 11: afterRender support
CanvasXpress objects accept the `afterRender` property, which defines a list
of functions and parameters for each function.  This list is executed once
the canvas element has been updated by the creation Javascript.  CanvasXpress
for Python now supports this with the addition of the `after_render` property.

### 2021 June 11: Jupyter rendering supports bundled charts
CanvasXpress supports data broadcasting, which permits charts on the same Web
page with the same data references to synchronize data selections and refreshes
with no or minimal work on the developer's part.  When used with Jupyter 
Notebooks, CanvasXpress for Python rendered each chart in its own Web container,
which prevented broadcasting from working.  With this release, `CXNoteBook` 
now permits multiple charts to be included in the same Web container. 

### 2021 June 9: Network, Genome, and Raw JSON data now supported
The CanvasXpress JSON data format allows for network diagram specific data.
`CXNetworkProfile` has been added to support network JSON data.  A minimum
verification of data type (only key-pair is permitted) is provided for a 
Python tier sanity check.  Multiple network data formats are allowed by the
Javascript library and enhanced validation will be built over time.

The CanvasXPress JSON data format allows for genome diagram specific data.
`CXGenomeProfile` has been added to support genome JSON data.  Only key-pair
data is permitted, and it is verified for the `tracks` and `type` attributes
in terms of presence and data type.  Variations for track elements are
permitted by the Javascript library and enhanced validation will be built
over time.

`CXProfiledData` defaults to using no profile, and upon being used in the 
`CanvasXpress` `render_to_html()` function are assigned a profile if none
is associated per the `graphType` configuration if present.  A `CXData` 
object with no profile provides its `dict`-form of data as-is.  To avoid
profile assignment, the `CXRawProfile` can be assigned to data objects.  This
profile will pass-through the `dict`-form unmodified and avoid default profile
assignment by the `CanvasXpress` object.  This allows advanced data formatting
or support for unknown data formats by advanced users or development releases
of the CanvasXpress Javascript library.

### 2021 June 7: Venn JSON data now supported
The CanvasXpress JSON data format allows for venn diagram specific data.
`CXVennProfile` has been added to support venn JSON data.

Additionally, `render_to_html_parts` now checks as to whether a profile has 
been assigned to data objects, and if not then per the `graphType` config
parameter assigns a render profile.

### 2021 June 3: x, z, and cors JSON data now supported
The CanvasXpress JSON data format allows for `x` and `z` attributes to provide
metadata for columns and rows, respectively.  Correlation diagrams also accept
the `y[cors]` attribute for pre-calculated correlation data.

The `CXStandardProfile` now explicity supports `x` and `z` attributes, and will
provide essential verification for alignment with respective `y` components.

The `CXStandardProfile` now explicity supports `y[cors]` data in addition to
`y[data]` and will handle metadata defaults for `y[vars]` and `y[smps]` 
accordingly.  This brings `cxStandardProfile` into full compliance with 
typical JSON data objects.  

Note that correlation data is not calculated for matrix data types, but 
CanvasXpress for Javasxcript will calculate those values for the referenced 
matrix in the JSON data if a correlation chart is indicated.

### 2021 May 28: width, height, and canvas properties
The `CanvasXpress` object now accepts dedicated `width`, `height`, `canvas` 
properties.  

`width` and `height` replace the now-deprecated `element_width` and 
`element_height` properties, and these are expected to be the final 
names used for each.  Values for each are used in the `<canvas>` element
generated for use in HTML, and they affect the render container sizes when
used in conjunction with contexts such as Jupyter Notebooks.

`canvas` tracks `CXConfig` values that become attributes of the generated
`<canvas>` element.  In this manner attributes such as `class` or `style`
can be calculated and managed at the Python tier.

See the documentation and examples for detailed usage.

### 2021 May 28: dict and tuple values now supported for CXConfigs
The `CanvasXpress` class uses `CXConfigs` to track configuration parameters 
for the chart and `<canvas>` element.  These now accept `dict` and `tuple`
values for more convenient initialization of the `CanvasXpress` object.

See the documentation and examples for detailed usage.

### 2021 May 21: CXUrlData added
CanvasXpress accepts URL references to files or endpoints with properly 
formatted JSON data.  `CXUrlData` has been added to support URL passthrough 
to the CanvasXpress Javascript, along with some validation ability at the
Python tier.

### 2021 May 18: CXDataProfile added
CanvasXpress has specific requirements for data organization within a JSON so 
that it can be properly rendered in a chart.  See the 
[CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data) for
additional information.

Data generated or provided at the Python tier might not satisfy those 
requirements, especially where matrix data is concerned.  CXDataProfile has
been added as a component to facilitate proper JSON formatting when providing
the data to the rendered CanvasXpress Javascript.  CXData has been enhanced to
make use of CXDataProfile.

The [CanvasXpress for Python documentation](https://canvasxpress-python.readthedocs.org)
 discusses profiles in detail, but in summary:

* Each CXData object is provided with a CXStandardProfile that understands how
  to pass through or add `y` `vars`, `smps`, and `data` attributes as proper.

* Default values for `vars` and `smps` are autogenerated if missing, provided 
  that sufficient information in the data is available.  This is especially
  handy for common matrix data sources typical in Python applications.
  
* Validation is supported for affirming that rows and columns in data align with
  provided `vars` and `smps` attributes, respectively.
  
As such, raw data can be passed on to CanvasXpress via key-pair structures so as
to keep mapping between Javascript and Python sources simple; however, custom
or default formatting is now supported at the Python tier to ease integration
and exploration where `y` attributes are not present in the source data.

***Additional** functionality will be added soon, such as to support `x` and `z`
CanvasXpress JSON data profiles.  Expect rapid enhancements in this area.*

### 2021 May 17: Adjusted property names
To better align with CanvasXpress for Javascript, or otherwise avoid confusion, 
some property names were changed in the `CanvasXpress` class:

* `target_id` has been replaced with `render_to` to align with the JS 
  `renderTo` attribute.  Functionality is identical.  `target_id` will 
  remain as a deprecated property through May, after which it will be removed
  per team convenience.
  
* `configs` has been replaced with `config` to align with the JS 
  `config` attribute.  Functionality is identical.  `configs` will 
  remain as a deprecated property through May, after which it will be removed
  per team convenience.
  
* `chart_width` and `chart_height` are replaced with `element_width` and 
  `element_height`, respectively.  These properties dictate the container
  size at the Python tier in application, such as the render window provided
  for Jupyter Notebooks.  The actual CanvasXpress chart continues to use the
  `width` and `height` attributes per the JS documentation, and if these values
  result in a rendered chart larger than the element window then depending on
  the application context aspects such as scrollbars might appear to provide
  full access.  The distinction is maintained for applications with non-reactive
  user interfaces, such as what might be typical of QT apps.
