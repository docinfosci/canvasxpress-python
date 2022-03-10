from abc import ABC, abstractmethod


class CXHtmlConvertable(ABC):
    """
    CXHtmlConvertable represents an object that can be converted into HTML.
    """

    @abstractmethod
    def render_to_html_parts(self) -> dict:
        """
        Converts the object into HTML5 compliant script.
        :returns: `dict`
            A `dict` representation of the object with each component of the
            necessary HTML indicated by a key.  For example, there might be
            a `div` element and a `script` import.
        """
        pass


class CXDictConvertable(ABC):
    """
    CXDictConvertable represents an object that can be converted into a dict.
    """

    @abstractmethod
    def render_to_dict(self, **kwargs) -> dict:
        """
        Converts the object into a dict representation.
        :param kwargs:
            Keyword arguments that can be supplied to facilitate rendering
            decisions.
        :returns: `dict`
            A dictionary representation of the object, such as what might be
            needed for a JSON export.
        """
        pass


class CXListConvertable(ABC):
    """
    CXListConvertable represents an object that can be converted into a list.
    """

    @abstractmethod
    def render_to_list(self, **kwargs) -> list:
        """
        Converts the object into a list representation.
        :param kwargs:
            Keyword arguments that can be supplied to facilitate rendering
            decisions.
        :returns: `list`
            A list representation of the object, such as what might be
            needed for a JSON export.
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
        :returns: `str`
            A string representation of the object in a form that can be used
            within HTML or Javascript.
        """
        pass
