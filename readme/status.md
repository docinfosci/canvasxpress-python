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
| **Documentation Status** | [![Documentation Status](https://readthedocs.org/projects/canvasxpress-python/badge/?version=latest)](https://canvasxpress-python.readthedocs.io/en/latest/) | [![Documentation Status](https://readthedocs.org/projects/canvasxpress-python/badge/?version=develop)](https://canvasxpress-python.readthedocs.io/en/develop/) |
| **Activity** | [![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/main)](https://github.com/docinfosci/canvasxpress-python) | [![Activity](https://img.shields.io/github/last-commit/docinfosci/canvasxpress-python/develop)](https://github.com/docinfosci/canvasxpress-python/tree/develop) |
<!-- End Badges -->

### Recent Enhancements

#### 2021 June 3: cors JSON data now recognized
The `CXStandardProfile` now explicity supports `y[cors]` data in addition to
`y[data]` and will handle metadata defaults for `y[vars]` and `y[smps]` 
accordingly.  This brings `cxStandardProfile` into full compliance with 
typical JSON data objects.  

Note that correlation data is not calculated for matrix data types, but 
CanvasXpress for Javasxcript will calculate those values for the referenced 
matrix in the JSON data if a correlation chart is indicated.

#### 2021 May 28: width, height, and canvas properties
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

#### 2021 May 28: dict and tuple values now supported for CXConfigs
The `CanvasXpress` class uses `CXConfigs` to track configuration parameters 
for the chart and `<canvas>` element.  These now accept `dict` and `tuple`
values for more convenient initialization of the `CanvasXpress` object.

See the documentation and examples for detailed usage.

#### 2021 May 21: CXUrlData added
CanvasXpress accepts URL references to files or endpoints with properly 
formatted JSON data.  `CXUrlData` has been added to support URL passthrough 
to the CanvasXpress Javascript, along with some validation ability at the
Python tier.

#### 2021 May 18: CXDataProfile added
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

#### 2021 May 17: Adjusted property names
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

### Roadmap

This package is actively maintained and developed.  Our focus for 2021 is:

#### Immediate Focus

- Enhanced examples and documentation for CXDataProfile components
- Support CanvasXpress JSON data object `x` and `z` attributes in profiles
- Support alternate CanvasXpress data objects for venn (etc.)

#### General Focus

- Continued alignment with the CanvasXpress Javascript library
- Continued stability and security, if/as needed
- Expanded examples and tutorials
- Expanded platform integrations
