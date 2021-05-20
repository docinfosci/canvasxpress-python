# CanvasXpress Data Management

This section explores data management in CanvasXpress for Python in detail.
Specifically, there are two perspectives that need to be understood:

1. [CanvasXpress for Javascript JSON data objects](https://www.canvasxpress.org/docs.html#data)
1. Python data objects and their transformation into JSON data objects

## JSON Data Objects

To work with CanvasXpress, it is imperative to have a general understanding of
how data is structured so that it can be properly illustrated.  

It is **strongly** recommended that you read 
[CanvasXpress for Javascript JSON data objects](https://www.canvasxpress.org/docs.html#data).

In summary, CanvasXpress can work with various data formats.  These can be simple,
such as a CSV, or more complicated, such as for correlations or venn charts.

Regardless, CanvasXpress wants to know about three topics when consuming the 
data for plotting:

- The data itself, which is tracked in a `y` attribute
- Annotations for samples (columns), tracked in a `x` attribute
- Annotations for variables (rows), tracked in a `z` attribute

`y` is mandatory, but `x` and `z` are optional.

Consider the following matrix:
```text
   2020-01-01  2020-01-02  2020-01-03  2020-01-04  2020-01-05  2020-01-06
0    0.814815    1.875444    2.340841    2.279296    4.375831     3.54344
1    0.853220    1.736362    2.611956    3.597166    4.146341     4.63242
```

This is expressed at a minimum to CanvasXpress as a JSON data object:
```javascript
{
    "y": {
        "vars": [
            0,
            1
        ],
        "smps": [
            "2020-01-01",
            "2020-01-02",
            "2020-01-03",
            "2020-01-04",
            "2020-01-05",
            "2020-01-06"
        ],
        "data": [
            [
                0.9669040908711064,
                1.4666314831549938,
                2.7875097369585076,
                2.516903607418437,
                4.341416062897548,
                5.198483033228731
            ],
            [
                0.5708513177432284,
                1.1909844314943148,
                2.863968555094556,
                3.3922728372428548,
                3.4122582648495534,
                3.057544399275495
            ]
        ]
    }
}
```

The `y` attribute tells CanvasXpress that the enclosed information pertains to
the data itself.

The matrix header is used to describe samples, designated as the `smps` attribute.
Each column is a sample index that will form the X or Y axis markers per the 
chart orientation.

The row index, in this case not specifically assigned but ordinally implied as 
0..N from top to bottom, indicates variables designated as the `vars` attribute.

Each row of data (a variable) is plotted aligned with the proper column of data
(the sample) and marked accordingly.

The following code will generate a matrix, print the matrix, print the JSON
data object, and then plot the chart:
```python
from pandas import DataFrame
import json

from datetime import date, timedelta
from random import uniform

from canvasxpress.canvas import CanvasXpress
from canvasxpress.config.collection import CXConfigs
from canvasxpress.data.matrix import CXDataframeData
from canvasxpress.render.jupyter import CXNoteBook

# Generate a set of values over a 6-day period
start_date = date(2020, 1, 1)
header = [
    str(start_date + timedelta(days=i))
    for i in range(6)
]
content = [
    [
        uniform((i + 1) / 2, i + 1)
        for i in range(6)
    ],
    [
        uniform((i + 1) / 2, i + 1)
        for i in range(6)
    ]
]

# Establish the working matrix
values_by_day = DataFrame(
    content,
    columns=header
)
sample = CXDataframeData(values_by_day)

# Print the matrix
print("DataFrame:")
print(values_by_day)

# Print the corresponding JSON data object
print()
print("CX Data Perspective")
print(json.dumps(sample.render_to_dict(), indent=4))

# Configure a set of spark lines
chart_options = CXConfigs()
chart_options \
    .set_param("graphOrientation", "vertical") \
    .set_param("graphType", "Line") \
    .set_param("title", "Line Graphs")

# Create the chart
chart = CanvasXpress(
    render_to="sample_chart",
    data=sample,
    config=chart_options
)

# Render into Jupyter
nb = CXNoteBook(chart)
nb.render()
```

The above code illustrates a line chart, such as:

<img src="line_plot_data_tutorial.png" align="center" width="556"></a>

## Python Data

CanvasXpress for Python provides two perspectives into data at the Python tier:

1. The data itself, which can be matrix or key-pair in nature
1. A data profile, which understands JSON data object requirements can provides
   the metadata necessary to make the data useable by CanvasXpress Javascript

### CXData

All data is wrapped in the CXData structure, which is the root of a component
framework that understands the nature of various data sources and formats.
These components are responsible for converting the tracked data into a form
suitable for the `y -> data` portion of the JSON object.

Members of this framework include:

- CXData
    - CXProfiledData
        - CXMatrixData
            - CXDataframeData
            - CXCSVData
        - CXKeyPairData
            - CXDictData
            - CXJSONData
    
### CXDataProfile

The simplest means of getting started with CanvasXpress for Python is to use one
of the `CXKeyPairData` components and format the context exactly as how the
Javascript library prefers.  In fact, if working with example data from the 
[CanvasXpress](https://www.canvasxpress.org) site this is the faster way to
begin using the framework.

However, data consumed or generated by Python modules or scripts is very likely
to be unaware of CanvasXpress JSON data object requirements.  In this case, a 
`CXDataProfile` can be used to ensure that the `y` attribute is properly 
formatted and populated.

Members of the profile framework include:

- CXProfileException
- CXDataProfile
    - CXStandardProfile
    - CXCorrelationProfile (TBD)
    - CXVennProfile (TBD)
    
All `CXProfiledData` objects are provided with `CXStandardProfile`, which 
understands the typical JSON data object requirements.

For matrix data, `CXStandardProfile` will inspect the matrix and determine 
appropriate `vars` and `smps` values.

For key-pair data, `CXStandardProfile` will first check to see if attributes 
such as `y`, `vars`, `smps`, and `data` exist.  As they do, they are adopted
from the data as-is.  As they do not, the profile inspects the object for 
elements that can be used directly or for a calculation to create proxies.

It is also possible to override the `vars` and `smps` values in the data
objects by assigning new values to `vars` and `smps` properties for the 
profile.  For example, in the initial example on this page the sample object
provides default `vars` values of `[0, 1]` because that's the implied row 
index.  Instead, those values could be replaced:

```python
sample.profile.vars = ['A', 'B']
```

In which case, the legend in the screenshot would update to using the letters 
instead of the numbers.

Although data and profile components do their best to create appropriate
transformations to satisfy CanvasXpress at the Javascript tier, it is up
to the Python logic to ensure that reasonable data is provided to begin with.
A key-pair object that is not already arranged to satisfy CanvasXpress `y[data]`
expectations will not be usable by the chart, just as would be the case if
working in Javascript directly.

## Roadmap

For now, developers requiring access to full CanvasXpress JSOn data functionality
should use `CXKeyPairData` components and directly format the content as desired.

The current package provides `y` perspective translation as is typically needed
for charts other than Venn diagrams, whether the data is matrix or key-pair.

We are now actively working to add or enhance support for:

- Profiles addressing the custom data attributes for correlation and venn
- Attribute handling for `x` and `z` topics

The above functionality is expected to roll out as part of May and June releases.
