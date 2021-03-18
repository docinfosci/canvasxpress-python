from abc import ABC, abstractmethod


class CXHtmlConvertable(ABC):
    """
    CXHtmlConvertable represents an object that can be converted into HTML.
    """

    @abstractmethod
    def render_to_html_parts(self) -> str:
        """
        Converts the object into HTML5 complant script.
        """
        pass


class CXDictConvertable(ABC):
    """
    CXDictConvertable represents an object that can be converted into a dict.
    """

    @abstractmethod
    def render_to_dict(self) -> dict:
        """
        Converts the object into HTML5 complant script.
        """
        pass


class CXJavascriptConvertable(ABC):
    """
    CXJavascriptConvertable represents an object that can be converted into JS.
    """

    @abstractmethod
    def render_to_js(self) -> str:
        """
        Converts the object into HTML5 complant script.
        """
        pass
