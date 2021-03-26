from canvasxpress.data.convert import CXDictConvertable


class TestableDictConvertable(CXDictConvertable):

    def render_to_dict(self) -> dict:
        return super().render_to_dict()


def test_CXDictConvertable_render_to_dict():
    candidate: CXDictConvertable = TestableDictConvertable()
    assert candidate.render_to_dict() is None
