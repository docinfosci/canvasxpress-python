from canvasxpress.data.convert import CXJavascriptConvertable


class TestableJavascriptConvertable(CXJavascriptConvertable):
    def render_to_js(self) -> str:
        return super().render_to_js()


def test_CXDictConvertable_render_to_dict():
    candidate: CXJavascriptConvertable = TestableJavascriptConvertable()
    assert candidate.render_to_js() is None
