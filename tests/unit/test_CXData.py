from canvasxpress.data.base import CXData


class SampleData(CXData):
    """
    A generic CXData for testing the abstract base class.
    """

    __data: dict = None

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        if data:
            self.__data = data
        else:
            self.__data = dict()

    def data(self) -> dict:
        result = super().data
        if not result:
            result = self.__data
        return result

    def get_raw_dict_form(self) -> dict:
        result = super().render_to_dict()
        if not result:
            result = self.__data
        return result

    def render_to_dict(self) -> dict:
        result = super().render_to_dict()
        if not result:
            result = self.__data
        return result


def test_CXData_get_data():
    sample_data = {
        "y": {
            "vars": ["Gene1"],
            "smps": ["Smp1", "Smp2", "Smp3"],
            "data": [[10, 35, 88]],
        }
    }

    testable_data: SampleData = SampleData(sample_data)

    assert testable_data.data() == sample_data
