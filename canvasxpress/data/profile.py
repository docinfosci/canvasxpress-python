from copy import deepcopy
from typing import Union

from canvasxpress.data.base import CXData, CXDataProfile, VARS, SMPS, \
    CXDataProfileException, CXMatrixData, Y, DATA, CORS, \
    CXKeyPairData, X, Z, VENN, LEGEND


class CXStandardProfile(CXDataProfile):
    """
    `CXStandardProfile` provides standard chart data profile functionality,
    by which the topics of `y`, `x`, and `z` are handled in conversions.
    """

    __y: dict = {
        VARS: list(),
        SMPS: list()
    }
    """
    Tracks the `y` CanvasXPress JSON data topic.  For example:
    ```python
    "y": {
        "vars": [ "Variable1", Variable2 ],
        "smps": [ "Sample1", "Sample2", "Sample3" ],
        "data": [
            [ 10, 20, 30 ],  
            [ 40, 50, 60 ]  
        ]
    },
    ```
    Also see [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data).
    """

    __x: dict = {}
    """
        Tracks the `x` CanvasXPress JSON data topic.  For example:
        ```python
        "y": {
            "vars": [ "Variable1", Variable2 ],
            "smps": [ "Sample1", "Sample2", "Sample3" ],
            "data": [
                [ 10, 20, 30 ],  
                [ 40, 50, 60 ]  
            ]
        },
        "x": {
            "sample-annotations": [
                "Sample1-annotation", 
                "Sample2-annotation", 
                "Sample3-annotation"
            ]
        }
        ```
        Also see [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data).
        """

    __z: dict = {}
    """
        Tracks the `z` CanvasXPress JSON data topic.  For example:
        ```python
        "y": {
            "vars": [ "Variable1", Variable2 ],
            "smps": [ "Sample1", "Sample2", "Sample3" ],
            "data": [
                [ 10, 20, 30 ],  
                [ 40, 50, 60 ]  
            ]
        },
        "z": {
            "variable-annotations": [
                "Variable1-annotation", 
                "Variable2-annotation"
            ]
        }
        ```
        Also see [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data).
        """

    @property
    def vars(self) -> list:
        """
        Provides the `y["vars"]` CanvasXPress JSON data topic.  `vars` are used
        to describe the rows of data.  For example:
        ```python
        "y": {
            "vars": [ "Variable1", Variable2 ],
            "smps": [ "Sample1", "Sample2", "Sample3" ],
            "data": [
                [ 10, 20, 30 ],  # <- This sub-list is what Variable1 references
                [ 40, 50, 60 ]  # <- This sub-list is what Variable2 references
            ]
        },
        ```
        Also see [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data).

        :returns: `list`
            A list of variables, for which there should be one per row.
        """
        return self.__y[VARS]

    @vars.setter
    def vars(self, variables: Union[list, None]) -> None:
        """
        Sets the variable labels to be used for rows of data.
        :param variables: `Union[list, None]`
            The list of var values.  Each must be convertable to `str`, and
            the number of var elements must match the row count.  `None` will
            reset the var list.
        """
        if variables:
            if not isinstance(variables, list):
                raise TypeError("variables must be a list or None")
            else:
                self.__y[VARS] = variables

        else:
            self.__y[VARS] = list()

    @property
    def smps(self) -> list:
        """
        Provides the `y["smps"]` CanvasXPress JSON data topic.  `smps` are used
        to describe the columns of data.  For example:
        ```python
        "y": {
            "vars": [ "Variable1", Variable2 ],
            "smps": [ "Sample1", "Sample2", "Sample3" ],
            "data": [
                [ 10, 20, 30 ],
                [ 40, 50, 60 ]
                #  ^-- This is Sample1
                #      ^-- This is Sample2
                #          ^-- This is Sample3
            ]
        },
        ```
        Also see [CanvasXpress documentation](https://www.canvasxpress.org/docs.html#data).

        :returns: `list`
            A list of samples, for which there should be one per column.
        """
        return self.__y[SMPS]

    @smps.setter
    def smps(self, samples: Union[list, None]) -> None:
        """
        Sets the sample labels to be used for columns of data.
        :param samples: `Union[list, None]`
            The list of smps values.  Each must be convertable to `str`, and
            the number of var elements must match the column count.  `None` will
            reset the smps list.
        """
        if samples:
            if not isinstance(samples, list):
                raise TypeError("samples must be a list or None")
            else:
                self.__y[SMPS] = samples

        else:
            self.__y[SMPS] = list()

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value: Union[dict, None]) -> None:
        """
        Sets the `y` attribute for the data, which is the primary data for the
        chart.  At a minimum `vars` and `smps` should be present, and if those
        are not provided then defaults will be provided.
        A deepcopy of the provided dict is made.
        :param value: `Union[dict, None]`
            A dict value of list attributes, for which `vars` and `smps` values
            will be provided if none are specified.  Provide `None` to set
            default values.
        """
        if value is None:
            self.__y = dict()

        elif not isinstance(value, dict):
            raise TypeError("value must be a dict or None.")

        else:
            candidate = value
            if Y in candidate.keys():
                candidate = value[Y]
                if not isinstance(candidate, dict):
                    raise TypeError(
                        "The JSON data Y attribute must be a dict of lists."
                    )

            for i in candidate.keys():
                if not isinstance(candidate[i], list):
                    raise TypeError(
                        "The JSON data Y attribute must be a dict of lists."
                    )

            self.__y = deepcopy(candidate)

        # Ensure essential values are provided.
        if not self.__y.get(VARS):
            self.__y[VARS] = list()

        if not self.__y.get(SMPS):
            self.__y[SMPS] = list()

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value: Union[dict, None]) -> None:
        """
        Sets the `x` attribute for the data, which corresponds to the
        annotations for each `smps` element.  Quantities should match.
        A deepcopy of the provided dict is made.
        :param value: `Union[dict, None]`
            A dict value of list attributes that should each contain one
            element per list for each `smps` element.  Provide `None` to
            reset the `x` attributes.
        """
        if value is None:
            self.__x = dict()

        elif not isinstance(value, dict):
            raise TypeError("value must be a dict or None.")

        else:
            candidate = value
            if X in candidate.keys():
                candidate = value[X]
                if not isinstance(candidate, dict):
                    raise TypeError(
                        "The JSON data X attribute must be a dict of lists."
                    )

            for i in candidate.keys():
                if not isinstance(candidate[i], list):
                    raise TypeError(
                        "The JSON data X attribute must be a dict of lists."
                    )

            self.__x = deepcopy(candidate)

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, value: Union[dict, None]) -> None:
        """
        Sets the `z` attribute for the data, which corresponds to the
        annotations for each `vars` element.  Quantities should match.
        A deepcopy of the provided dict is made.
        :param value: `Union[dict, None]`
            A dict value of list attributes that should each contain one
            element per list for each `vars` element.  Provide `None` to
            reset the `z` attributes.
        """
        if value is None:
            self.__z = dict()

        elif not isinstance(value, dict):
            raise TypeError("value must be a dict or None.")

        else:
            candidate = value
            if Z in candidate.keys():
                candidate = value[Z]
                if not isinstance(candidate, dict):
                    raise TypeError(
                        "The JSON data Z attribute must be a dict of lists."
                    )

            for i in candidate.keys():
                if not isinstance(candidate[i], list):
                    raise TypeError(
                        "The JSON data Z attribute must be a dict of lists."
                    )

            self.__z = deepcopy(candidate)

    def add_data_section(
            self,
            section: str,
            source: dict,
            target: dict,

    ) -> None:
        """
        Adds a source data section, such as X, to the target if such a section
        does not yet exist.
        :param section: `str`
            The name of the section, such as X.
        :param source: `dict`
            The dict of lists to add.
        :param target: `dict`
            The dict to which source should be added.
        """
        if not target.get(section):
            target[section] = source

        else:
            if not isinstance(target[section], dict):
                target[section] = source

            elif len(target[section].keys()) == 0:
                target[section] = source

            else:
                # Preserve user provided section
                pass

        for key in target[section].keys():
            if not isinstance(target[section][key], list):
                raise TypeError(f"data[{section}][{key}] must be of type list")

    def render_to_profiled_dict(
            self,
            data: CXData,
            match_vars_to_rows: bool = True,
            match_smps_to_cols: bool = True,
            match_x_to_smps: bool = True,
            match_z_to_vars: bool = True,
            **kwargs,
    ) -> dict:
        """
        Converts a given `CXData` instance into a dict suitable for use by
        `CanvasXpress` when creating data instructions for the JS object.

        *For matrix data:*<br>
        If `vars` are not set then `data` will be inspected:
        - The index will be used.
        If `smps` are not set then `data` will be inspected:
        - The column headers will be used.

        *For key-pair data:*<br>
        If `vars` are not set then `data` will be inspected:
        - If `y` is not provided then an attribute will be established.
        - If y[vars] is not provided then vars will be assigned numerically
          for each row in data.

        If `smps` are not set then `data` will be inspected:
        - If `y` is not provided then an attribute will be established.
        - If y[smps] is not provided then smps will be assigned numerically
          for each row in data.

        `x` and `z` values are passed-through to the rendered JSON data.

        :param data: `CXData`
            The data object to introspect to create an enveloping profile.

        :param match_vars_to_rows: `bool`
            Indicates whether the number `y[vars]` must equal the number of
            rows specified in `y[data]`.  If `True` then an exception will be
            raised should the number of vars and rows of data not match.

        :param match_smps_to_cols: `bool`
            Indicates whether the number `y[smps]` must equal the number of
            columns specified in `y[data]`.  If `True` then an exception will be
            raised should the number of smps and columns of data not match.

        :param match_x_to_smps: `bool`
            Indicates whether for each attribute of `x` the number of list
            elements should match the number of `smps` elements.  If `True`
            then an exception will be raised if the counts do not align.

        :param match_z_to_vars: `bool`
            Indicates whether for each attribute of `z` the number of list
            elements should match the number of `vars` elements.  If `True`
            then an exception will be raised if the counts do not align.

        :returns: `dict`
            A CanvasXpress compliant JSON data object in the form of a `dict`
            with topics such as `y['vars'] properly completed.  If an issue
            is found with the data then a `CXDataProfileException` will be
            raised.
        """

        # Reject None values
        if data is None:
            raise CXDataProfileException(
                "data cannot be None."
            )

        # cx_data is the object to be returned after being appropriately
        # populated with matrix or key-pair data and metadata.
        cx_data = dict()

        ### Y

        # Handle matrix data
        if isinstance(data, CXMatrixData):

            raw_dict = data.get_raw_dict_form()

            cx_data[Y] = {
                VARS: raw_dict['index'] if len(self.vars) == 0 else self.vars,
                SMPS: raw_dict['columns'] if len(self.smps) == 0 else self.smps,
                DATA: raw_dict['data']
            }

        # Handle key-pair data
        elif isinstance(data, CXKeyPairData):

            cx_data = data.get_raw_dict_form()

            # Handle if a y section is already defined
            if cx_data.get(Y):

                # If the user has specified vars OR vars is missing from Y
                # then override the data's copy
                if len(self.vars) != 0:
                    cx_data[Y][VARS] = self.vars

                elif cx_data[Y].get(VARS) is None:
                    cx_data[Y][VARS] = list()
                    if cx_data[Y].get(DATA):
                        if isinstance(cx_data[Y].get(DATA), list):
                            for i, r in enumerate(cx_data[Y].get(DATA)):
                                cx_data[Y][VARS].append(i)

                else:
                    # Preserve the specified values
                    pass

                # If the user has specified smps OR smps is missing from Y
                # then override the data's copy
                if len(self.smps) != 0:
                    cx_data[Y][SMPS] = self.smps

                elif cx_data[Y].get(SMPS) is None:
                    cx_data[Y][SMPS] = list()
                    if cx_data[Y].get(DATA):
                        if isinstance(cx_data[Y].get(DATA), list):
                            if len(cx_data[Y].get(DATA)) > 0:
                                if isinstance(cx_data[Y][DATA][0], list):
                                    for i, c in enumerate(cx_data[Y][DATA][0]):
                                        cx_data[Y][SMPS].append(i)

                else:
                    # Preserve the specified values
                    pass

            # Missing y section
            else:
                cx_rev_data = {
                    Y: {
                        VARS: self.vars,
                        SMPS: self.smps,
                        DATA: cx_data.get(DATA, [])
                    }
                }

                for key in cx_data.keys():
                    if key not in [X, Z]:
                        if key == DATA:
                            cx_rev_data[Y][DATA] = cx_data[key]

                        elif key == CORS:
                            cx_rev_data[Y][CORS] = cx_data[key]

                        elif key == VARS:
                            cx_rev_data[Y][VARS] = cx_data[key]

                        elif key == SMPS:
                            cx_rev_data[Y][SMPS] = cx_data[key]

                        elif isinstance(cx_data[key], list):
                            if len(cx_rev_data.get(DATA, [])) == 0:
                                cx_rev_data[Y][DATA] = cx_data[key]

                        else:
                            continue

                # Swap objects
                cx_data = cx_rev_data

        # Reject any other data type
        else:
            raise CXDataProfileException(
                f"data is of an unknown type: {type(data)}."
            )

        ### X
        self.add_data_section(
            X,
            self.x,
            cx_data
        )

        ### Z
        self.add_data_section(
            Z,
            self.z,
            cx_data
        )

        # Clean up the root of the JSON data object
        cx_data = deepcopy(cx_data)
        for key in reversed(cx_data.keys()):
            if key not in [Y, X, Z]:
                del cx_data[key]

        # Valid data format
        if cx_data[Y].get(DATA):
            if not isinstance(cx_data[Y][DATA], list):
                raise CXDataProfileException(
                    f"data must be a list of sub-list where each sub-list"
                    f" is a row of data.  Found {type(cx_data[Y][DATA])}"
                )
            for row in cx_data[Y][DATA]:
                if not isinstance(row, list):
                    raise CXDataProfileException(
                        f"data must be a list of sub-list where each"
                        f" sub-list is a row of data.  Found element in"
                        f" master list of type {type(cx_data[Y][DATA])}"
                    )

        # Minor examination of cors (this is an extension to standard data
        # with correlation data pre-calculated for correlation diagrams).
        if cx_data[Y].get(CORS):
            if not isinstance(cx_data[Y][CORS], list):
                raise CXDataProfileException(
                    f"cors must be a list of sub-list where each sub-list"
                    f" is a row of data.  Found {type(cx_data[Y][CORS])}"
                )
            for row in cx_data[Y][CORS]:
                if not isinstance(row, list):
                    raise CXDataProfileException(
                        f"cors must be a list of sub-list where each"
                        f" sub-list is a row of data.  Found element in"
                        f" master list of type {type(cx_data[Y][CORS])}"
                    )

        # Get a data proxy for data and cors for use in var and smps defaults
        data_proxy = cx_data[Y].get(DATA, [])
        if len(data_proxy) == 0:
            data_proxy = cx_data[Y].get(CORS, [])

            # Also remove redundant data key
            if cx_data[Y].get(DATA) is not None:
                del cx_data[Y][DATA]

        # Establish minimal var values per data
        if not isinstance(cx_data[Y][VARS], list):
            raise CXDataProfileException(
                f"vars must be a list. Found {type(cx_data[Y][VARS])}"
            )
        if len(cx_data[Y][VARS]) == 0:
            cx_data[Y][VARS] = [
                index
                for index
                in range(len(data_proxy))
            ]

        # Establish minimal smps values per data
        if not isinstance(cx_data[Y][SMPS], list):
            raise CXDataProfileException(
                f"smps must be a list. Found {type(cx_data[Y][SMPS])}"
            )
        if len(cx_data[Y][SMPS]) == 0:
            if len(data_proxy) > 0:
                cx_data[Y][SMPS] = [
                    index
                    for index
                    in range(
                        len(data_proxy[0])
                    )
                ]

        if match_vars_to_rows:
            row_count = len(data_proxy)
            var_count = len(cx_data[Y][VARS])
            if not row_count == var_count:
                raise CXDataProfileException(
                    f"match_vars_to_rows requires that y[vars] and data rows"
                    f" are equal in number.  Found {row_count} rows and"
                    f" {var_count} vars."
                )

        if match_smps_to_cols:
            if len(data_proxy) > 0:
                col_count = len(data_proxy[0])
            else:
                col_count = 0
            smps_count = len(cx_data[Y][SMPS])
            if not col_count == smps_count:
                raise CXDataProfileException(
                    f"match_smps_to_cols requires that y[smps] and data"
                    f" columns are equal in number.  Found {col_count}"
                    f" columns and {smps_count} smps."
                )

        if match_x_to_smps:
            for key in cx_data[X].keys():
                if len(cx_data[X][key]) != len(cx_data[Y][SMPS]):
                    raise ValueError(
                        f"cx_data[X][{key}] must be the same length as"
                        f" cx_data[Y][SMPS]"
                    )

        if match_z_to_vars:
            for key in cx_data[Z].keys():
                if len(cx_data[Z][key]) != len(cx_data[Y][VARS]):
                    raise ValueError(
                        f"cx_data[Z][{key}] must be the same length as"
                        f" cx_data[Y][VARS]"
                    )

        return cx_data

    def __init__(self):
        """
        Initializes the CXStandardProfile object.
        """
        super().__init__()
        self.x = None
        self.y = None
        self.z = None


class CXVennProfile(CXDataProfile):
    """
    `CXVennProfile` provides Venn diagram chart data profile functionality,
    by which the topics of `venn` and `legend` are handled in conversions.
    """

    __legend: dict = dict()
    """
    The legend key-pair for use with the diagram.
    """

    @property
    def legend(self) -> dict:
        """
        Returns the values to be used for the legend if such are not defined
        in the data.

        :returns: `dict`
            The key-pair data that will be used in the legend.
        """
        return self.__legend

    @legend.setter
    def legend(
            self,
            value: Union[dict, None]
    ) -> None:
        """
        Sets the values to be used for the legend.  Overrides legend values in
        the data if available.

        "param value: `Union[dict, None]`
            The key-pair values to be used for the legend.  Use None to reset
            the key-pair values.
        """
        if value is None:
            self.__legend = dict()

        elif isinstance(value, dict):
            self.__legend = deepcopy(value)

        else:
            raise TypeError("value must be of type dict or None.")

    def render_to_profiled_dict(
            self,
            data: CXData,
            **kwargs
    ) -> dict:
        """
        Converts a given `CXData` instance into a dict suitable for use by
        `CanvasXpress` when creating data instructions for the JS object.

        *For matrix data:*<br>
        Data must be one column with numeric values plus one index. `legend`
        values will be provided as set for the profile.

        ```python
        df = DataFrame.from_dict(
            {
                "A": 340,
                "B": 562,
                "C": 620,
                "AB": 639,
                "AC": 456,
                "BC": 915,
                "ABC": 552
            },
            orient="index"
        )
        ```

        If an index is not specified then the implicit index is used.

        *For key-pair data:*<br>
        Data must be a dict with the attribute `venn` with child attributes
        `data` and `legend`.  Or, `venn` can be ommitted.  `legend` is
        optional, and if values are set for the profile these will override
        those in the JSON data.

        ```python
        {
            "venn": {
                "data": {
                    "A": 340,
                    "B": 562,
                    "C": 620,
                    "AB": 639,
                    "AC": 456,
                    "BC": 915,
                    "ABC": 552
                },
                "legend": {
                    "A": "List1",
                    "B": "List2",
                    "C": "List3"
                }
            }
        }
        ```

        If a legend value needs to be calculated then `kwargs` is examined for
        `config`, which is expected to be of type `CXConfigs`.  If `config` is
        available then the CXConfig labelled `vennGroups` is sought.  The value
        assigned to `vennGroups` is used to count out an index of legend labels.

        :param data: `CXData`
            The data object to introspect to create an enveloping profile.
        """
        # Reject None values
        if data is None:
            raise CXDataProfileException(
                "data cannot be None."
            )

        # Determine the number of elements that start the diagram.  We need
        # this count for legend processing.
        legend_count = 0
        if kwargs.get("config"):
            config = kwargs['config'].get_param("vennGroups")
            if config:
                legend_count = int(config.value)

        # cx_data is the object to be returned after being appropriately
        # populated with matrix or key-pair data and metadata.
        cx_data = dict()

        # Handle matrix data
        if isinstance(data, CXMatrixData):

            raw_dict = data.get_raw_dict_form()

            if not raw_dict.get(DATA):
                raw_dict[DATA] = []

            if not raw_dict.get('index'):
                raw_dict['index'] = [i for i in range(len(raw_dict['data']))]

            cx_data[VENN] = {
                DATA: {
                    raw_dict['index'][e] : raw_dict['data'][e][0]
                    for e in range(len(raw_dict['index']))
                },
                LEGEND: {
                    str(raw_dict['index'][l]): f"Group {l+1}"
                    for l in range(legend_count)
                }
            }

        # Handle key-pair data
        elif isinstance(data, CXKeyPairData):

            cx_data = data.get_raw_dict_form()
            cx_rev_data = dict()

            # If attribute venn is present
            if cx_data.get('VENN'):
                cx_rev_data[VENN] = deepcopy(cx_data[VENN])

            else:
                cx_rev_data[VENN] = dict()
                cx_rev_data[VENN][DATA] = deepcopy(cx_data.get(DATA, {}))
                if cx_data.get(LEGEND):
                    cx_rev_data[VENN][LEGEND] = deepcopy(cx_data[LEGEND])

            if not isinstance(cx_rev_data[VENN], dict):
                raise TypeError("attribute venn must be a dict of dicts")

            if cx_rev_data[VENN].get(DATA) is None:
                raise ValueError(
                    "attribute veen must have child attribute data, and"
                    "data must be a dict"
                )

            if not isinstance(cx_rev_data[VENN].get(DATA, {}), dict):
                raise ValueError(
                    "attribute veen must have child attribute data, and"
                    "data must be a dict"
                )

            if cx_rev_data[VENN].get(LEGEND) is None:
                legend_candidates = cx_rev_data[VENN][DATA].keys()
                cx_rev_data[VENN][LEGEND] = {
                    legend_candidates[l]: f"Group {l+1}"
                    for l in range(legend_count)
                    if l < len(legend_candidates)
                }

            if not isinstance(cx_rev_data[VENN].get(LEGEND, {}), dict):
                raise ValueError(
                    "attribute veen must have child attribute legend, and"
                    "legend must be a dict aligned with vennGroups"
                )

            cx_data = cx_rev_data

        return cx_data


class CXNetworkProfile(CXDataProfile):
    def render_to_profiled_dict(
            self,
            data: CXData,
            **kwargs
    ) -> dict:
        """
        Converts a given `CXData` instance into a dict suitable for use by
        `CanvasXpress` when creating data instructions for the JS object.

        *For matrix data:*<br>
        TBD

        *For key-pair data:*<br>
        TBD

        :param data: `CXData`
            The data object to introspect to create an enveloping profile.
        """
        raise NotImplementedError("Yet to be implemented.")


class CXGenomeProfile(CXDataProfile):
    def render_to_profiled_dict(
            self,
            data: CXData,
            **kwargs
    ) -> dict:
        """
        Converts a given `CXData` instance into a dict suitable for use by
        `CanvasXpress` when creating data instructions for the JS object.

        *For matrix data:*<br>
        TBD

        *For key-pair data:*<br>
        TBD

        :param data: `CXData`
            The data object to introspect to create an enveloping profile.
        """
        raise NotImplementedError("Yet to be implemented.")
