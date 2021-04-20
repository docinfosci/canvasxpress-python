from canvasxpress.config.type import CXConfig


class SampleConfig(CXConfig):
    """
    A generic CXConfig for testing the abstract base class.
    """

    __value: str = None

    def __init__(self, label: str, value: str) -> None:
        super().__init__(label, value)
        self.value = value

    @property
    def value(self):
        result = super().value
        if not result:
            result = self.__value
        return result

    @value.setter
    def value(self, value: object) -> None:
        CXConfig.value.fset(
            self,
            value
        )
        if not self.__value:
            self.__value = str(value)


def test_CXConfig_value():
    testable_data: SampleConfig = SampleConfig(
        "label",
        "value"
    )
    assert testable_data.value == "value"
