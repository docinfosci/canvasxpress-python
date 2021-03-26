from canvasxpress.data.convert import CXHtmlConvertable


class TestableHtmlConvertable(CXHtmlConvertable):

    def render_to_html_parts(self) -> str:
        return super().render_to_html_parts()


def test_CXHtmlConvertable_render_to_html_parts():
    candidate: CXHtmlConvertable = TestableHtmlConvertable()
    assert candidate.render_to_html_parts() is None
