import json
from functools import total_ordering
from typing import Union

from pandas import DataFrame

from canvasxpress.data.base import CXMatrixData


@total_ordering
class CXDataframeData(CXMatrixData):
    """
    A CXData class dedicated to processing Python DataFrame, matrix-structured
     data.
    """

    __data: DataFrame = DataFrame()
    """
    The data managed by an object of this class.
    """

    @property
    def dataframe(self) -> DataFrame:
        """
        Provides the data managed by the object.
        :returns: `DataFrame` The managed data.
        """
        return self.__data

    @dataframe.setter
    def dataframe(self, value: Union[DataFrame, None] = None) -> None:
        """
        Sets the dataframe managed by the object.
        :param value: `Union[DataFrame, None]`
            `None` results in an empty `DataFrame`.  A deepcopy will be made of
            `DataFrame` values.
        """
        if not isinstance(value, (DataFrame, type(None))):
            raise TypeError("The assignment value must be a DataFrame or None.")

        candidate = value
        if candidate is None:
            candidate = DataFrame()

        self.data = candidate

    @property
    def data(self) -> dict:
        """
        Provides the data managed by the object.
        :returns: `DataFrame` The managed data.
        """
        return self.dataframe.to_dict(orient="list")

    @data.setter
    def data(self, value: Union["CXDataframeData", DataFrame, None] = None) -> None:
        """
        Sets the dataframe managed by the object.
        :param value: `Union['CXDataframeData', DataFrame, dict, str, None]`
            `None` results in an empty `DataFrame`.  A deepcopy will be made of
            `DataFrame` or equivalent values.
        """
        if value is None:
            self.__data = DataFrame()

        elif not isinstance(value, (CXDataframeData, DataFrame, type(None))):
            raise TypeError("The assignment value must be a DataFrame or None.")

        elif isinstance(value, CXDataframeData):
            self.__data = value.dataframe.copy(deep=True)

        elif isinstance(value, DataFrame):
            self.__data = value.copy(deep=True)

        else:
            self.__data = DataFrame()

    def get_raw_dict_form(self) -> dict:
        """ "
        Provides a simple dict perspective of the data with no metadata or other
        contextual transformations performed.  For example, if the data is
        natively in `dict` form then it would be passed-through with no
        modification or enhancement.

        This implementation provides matrix data formatted in a `dict` object
        with `DataFrame.to_dict('split')` behaviour.

        :returns: `dict`
            The `dict` perspective of the data with as little modification or
            interpretation as is reasonable.
        """
        return self.__data.to_dict(orient="split")

    def render_to_dict(self, **kwargs) -> dict:
        """
        Provides a dict representation of the data.
        :returns: `dict`
            The data in `dict` form.
        """
        candidate = self.get_raw_dict_form()
        return candidate

    def __init__(self, data: Union["CXDataframeData", DataFrame, None] = None) -> None:
        """
        Initializes the CXData object with data.  Only `DataFrame` or compatible
         data types are accepted.
        :param data: `Union['CXDataframeData', DataFrame, dict, str, None]`
            `None` to initialize with an empty `DataFrame`, or a `DataFrame`
            like object to assign mapped data.
        """
        super().__init__(data)
        self.data = data

    def __copy__(self) -> "CXDataframeData":
        """
        *copy constructor* that returns a copy of the CXDataframeData object.
        :returns: `CXDataframeData`
            A copy of the wrapping object.
        """
        return self.__class__(self.dataframe)

    def __deepcopy__(self, memo) -> "CXDataframeData":
        """
        *deepcopy constructor* that returns a copy of the CXDataframeData object.
        :returns: `CXDataframeData` A copy of the wrapping object and deepcopy of
            the tracked data.
        """
        return self.__class__(self.dataframe)

    def __lt__(self, other: "CXDataframeData") -> bool:
        """
        *less than* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDataframeData` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDataframeData` object then False
            <li> If `other` is a `CXDataframeData` object then True of all
                `CXDataframeData` aspects are also less than the data tracked by
                `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXDataframeData):
            return False

        else:
            self_c = self.dataframe.columns.unique()
            other_c = other.dataframe.columns.unique()

            if len(self_c) < len(other_c):
                return True

            elif len(self_c) > len(other_c):
                return False

            else:
                for i in [s for s in self_c if s not in other_c]:
                    if any([i < o for o in other_c]):
                        return True

                return self.dataframe.lt(other.dataframe).all(axis=None)

    def __eq__(self, other: "CXDataframeData") -> bool:
        """
        *equals* comparison.  Also see `@total_ordering` in `functools`.
        :param other:
            `CXDataframeData` The object to compare.
        :returns: `bool`
            <ul>
            <li> If `other` is `None` then `False`
            <li> If `other` is not a `CXDataframeData` object then False
            <li> If `other` is a `CXDataframeData` object then True of all
                `CXDataframeData` aspects are also less than the data tracked by
                `self`.
            </ul>
        """
        if other is None:
            return False

        if not isinstance(other, CXDataframeData):
            return False

        else:
            self_c = self.dataframe.columns.unique()
            other_c = other.dataframe.columns.unique()

            if len(self_c) != len(other_c):
                return False

            if any([s not in other_c for s in self_c]):
                return False

            return self.dataframe.eq(other.dataframe).all(axis=None)

    def __str__(self) -> str:
        """
        *str* function.  Converts the CXDataframeData object into a JSON
        representation.
        :returns" `str` JSON form of the `CXDataframeData`.
        """
        if self.dataframe is None:
            return str(None)

        else:
            return json.dumps(self.render_to_dict())

    def __repr__(self) -> str:
        """
        *repr* function.  Converts the CXDataframeData object into a pickle
         string that can be used with `eval` to establish a copy of the object.
        :returns: `str` An evaluatable representation of the object.
        """
        candidate = (
            f"CXDataframeData("
            f"data=pandas.read_csv("
            f'StringIO("""{self.dataframe.to_csv(index=True)}"""),'
            f"index_col=0))"
        )
        candidate = candidate.replace("Infinity", "float('inf')")
        candidate = candidate.replace("NaN", "float('nan')")

        return candidate


def merge_dataframes_into_xyz_object(
    data: CXDataframeData,
    sample_annotation: CXDataframeData = None,
    variable_annotation: CXDataframeData = None,
) -> dict:
    """
    Converts a set of DataFrame like objects into an XYZ dict.
    """
    xyz_data = {}

    if data is not None:
        xyz_data["y"] = {}
        xyz_data["y"]["data"] = data.dataframe.values.tolist()
        xyz_data["y"]["smps"] = data.dataframe.columns.tolist()
        xyz_data["y"]["vars"] = data.dataframe.index.tolist()

    if sample_annotation is not None and sample_annotation.dataframe.size > 0:

        xyz_data["x"] = {}

        try:

            # 1.  Scan first column - use values in each row.
            # 2.  Else use first row - use values in each column
            # 3.  Else scan index for a matching sample identifier - use values in each row.
            # 4.  Else scan the header - use values in each column

            # 1.  Scan first column - use values in each row.
            found_strategy = True
            for field in sample_annotation.dataframe[
                sample_annotation.dataframe.columns[0]
            ].values:
                if field not in xyz_data["y"]["smps"]:
                    found_strategy = False
                    break

            if found_strategy:
                for row_index in range(sample_annotation.dataframe.shape[0]):
                    key = sample_annotation.dataframe.iloc[row_index, 0]
                    if not isinstance(key, str):
                        x_key = key.item()
                    xyz_data["x"][key] = sample_annotation.dataframe.iloc[row_index][1:]

            # 2.  Else use first row - use values in each column
            else:
                found_strategy = True
                for column_index in range(sample_annotation.dataframe.shape[1]):
                    if (
                        sample_annotation.dataframe.iloc[0, column_index]
                        not in xyz_data["y"]["smps"]
                    ):
                        found_strategy = False
                        break

                if found_strategy:
                    for column_index in range(sample_annotation.dataframe.shape[1]):
                        column = sample_annotation.dataframe.columns[column_index]
                        meta_name = sample_annotation.dataframe[column][0]
                        if not isinstance(meta_name, str):
                            meta_name = meta_name.item()
                        meta_data = sample_annotation.dataframe[column][1:]
                        xyz_data["x"][meta_name] = meta_data

                # 3.  Else scan header for a matching sample identifier - use values in each column.
                else:
                    found_strategy = True
                    for header in sample_annotation.dataframe.columns.values:
                        if header not in xyz_data["y"]["smps"]:
                            found_strategy = False
                            break

                    if found_strategy:
                        for column_index, column in enumerate(
                            sample_annotation.dataframe.columns.values
                        ):
                            xyz_data["x"][
                                column if isinstance(column, str) else column.item()
                            ] = sample_annotation.dataframe[column]

                    # 4.  Else scan the index - use values in each row
                    else:
                        for index in sample_annotation.dataframe.index.values:
                            xyz_data["x"][
                                index if isinstance(index, str) else index.item()
                            ] = sample_annotation.dataframe.loc[index]

        except Exception as e:
            raise ValueError(
                "Sample Annotation data (x) cannot be parsed or aligned with Chart data (y)"
            )

    if variable_annotation is not None and variable_annotation.dataframe.size > 0:

        xyz_data["z"] = {}

        try:

            # 1.  Scan first column - use values in each row.
            # 2.  Else use first row - use values in each column
            # 3.  Else scan index for a matching sample identifier - use values in each row.
            # 4.  Else scan the header - use values in each column

            # 1.  Scan first column - use values in each row.
            found_strategy = True
            for field in variable_annotation.dataframe[
                variable_annotation.dataframe.columns[0]
            ].values:
                if field not in xyz_data["y"]["vars"]:
                    found_strategy = False
                    break

            if found_strategy:
                for row_index in range(variable_annotation.dataframe.shape[0]):
                    key = variable_annotation.dataframe.iloc[row_index, 0]
                    if not isinstance(key, str):
                        key = key.item()
                    xyz_data["z"][key] = variable_annotation.dataframe.iloc[row_index][
                        1:
                    ]

            # 2.  Else use first row - use values in each column
            else:
                found_strategy = True
                for column_index in range(variable_annotation.dataframe.shape[1]):
                    if (
                        variable_annotation.dataframe.iloc[0, column_index]
                        not in xyz_data["y"]["vars"]
                    ):
                        found_strategy = False
                        break

                if found_strategy:
                    for column_index in range(variable_annotation.dataframe.shape[1]):
                        column = sample_annotation.dataframe.columns[column_index]
                        meta_name = sample_annotation.dataframe[column][0]
                        if not isinstance(meta_name, str):
                            meta_name = meta_name.item()
                        meta_data = sample_annotation.dataframe[column][1:]
                        xyz_data["z"][meta_name] = meta_data

                # 3.  Else scan header for a matching sample identifier - use values in each column.
                else:
                    found_strategy = True
                    for header in variable_annotation.dataframe.columns.values:
                        if header not in xyz_data["y"]["vars"]:
                            found_strategy = False
                            break

                    if found_strategy:
                        for column_index, column in enumerate(
                            variable_annotation.dataframe.columns.values
                        ):
                            xyz_data["z"][
                                column if isinstance(column, str) else column.item()
                            ] = variable_annotation.dataframe[column]

                    # 4.  Else scan the index - use values in each rpw
                    else:
                        for index in variable_annotation.dataframe.index.values:
                            xyz_data["z"][
                                index if isinstance(index, str) else index.item()
                            ] = variable_annotation.dataframe.loc[index]

        except Exception as e:
            raise ValueError(
                "Variable Annotation data (z) cannot be parsed or aligned with Chart data (y)"
            )

    # Convert to Python native types for serialization

    if "x" in xyz_data:
        for annotation in xyz_data["x"].keys():
            xyz_data["x"][annotation] = [
                element if isinstance(element, str) else element.item()
                for element in xyz_data["x"][annotation]
            ]

    if "z" in xyz_data:
        for annotation in xyz_data["z"].keys():
            xyz_data["z"][annotation] = [
                element if isinstance(element, str) else element.item()
                for element in xyz_data["z"][annotation]
            ]

    return xyz_data
