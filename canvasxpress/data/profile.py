from copy import deepcopy
from typing import Union

from canvasxpress.data.base import CXData, CXDataProfile, VARS, SMPS, \
    CXDataProfileException, CXMatrixData, Y, DATA, \
    CXKeyPairData


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

    def render_to_profiled_dict(
            self,
            data: CXData,
            match_vars_to_rows: bool = False,
            match_smps_to_cols: bool = False
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

            else:
                cx_rev_data = {
                    Y: {
                        VARS: self.vars,
                        SMPS: self.smps,
                        DATA: cx_data.get(DATA, [])
                    }
                }

                if cx_data.get('x'):
                    cx_rev_data['x'] = cx_data['x']

                if cx_data.get('z'):
                    cx_rev_data['z'] = cx_data['z']

                for key in cx_data.keys():
                    if key not in ['x', 'z']:
                        if key == DATA:
                            cx_rev_data[Y][DATA] = cx_data[key]

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

            # Clean up the root of the JSON data object
            cx_data = deepcopy(cx_data)
            for key in reversed(cx_data.keys()):
                if key not in [Y, 'x', 'z']:
                    del cx_data[key]

            # Validate essentials
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

            # Establish minimal var and smps values per data if that has
            # yet to be accomplished.
            if len(cx_data[Y][VARS]) == 0:
                cx_data[Y][VARS] = [
                    str(index + 1)
                    for index
                    in range(len(cx_data[Y][DATA]))
                ]

            if len(cx_data[Y][SMPS]) == 0:
                if len(cx_data[Y][DATA]) > 0:
                    cx_data[Y][SMPS] = [
                        str(index + 1)
                        for index
                        in range(len(cx_data[Y][DATA][0]))
                    ]

        # Reject any other data type
        else:
            raise CXDataProfileException(
                f"data is of an unknown type: {type(data)}."
            )

        # Validate vars vs data rows
        if match_vars_to_rows:
            row_count = len(cx_data[Y][DATA])
            var_count = len(cx_data[Y][VARS])
            if not row_count == var_count:
                raise CXDataProfileException(
                    f"match_vars_to_rows requires that y[vars] and data rows"
                    f" are equal in number.  Found {row_count} rows and"
                    f" {var_count} vars."
                )

        # Validate smps vs data columns
        if match_smps_to_cols:
            col_count = len(cx_data[Y][DATA][0])
            smps_count = len(cx_data[Y][SMPS])
            if not col_count == smps_count:
                raise CXDataProfileException(
                    f"match_smps_to_cols requires that y[smps] and data"
                    f" columns are equal in number.  Found {col_count}"
                    f" columns and {smps_count} smps."
                )

        return cx_data

    def __init__(self):
        """
        Initializes the CXStandardProfile object.
        """
        super().__init__()
