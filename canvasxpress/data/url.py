from urllib.parse import urlparse, urlunparse

from canvasxpress.data.base import CXData


class CXUrlData(CXData):
    """
    CXUrlData provides the ability to accept a URL and pass it properly to the
    CanvasXpress object.
    """

    __url: str = ""
    """
    The tracked URL.
    """

    @property
    def url(self) -> str:
        """
        Provides the URL formatted as a string.
        :returns: `str`
            A string representation of the URL, similer to the data that will
            be provided to the CanvasXpress object.
        """
        return self.__url

    @url.setter
    def url(self, url: str) -> None:
        """
        Tracks the specified URL. `ValueError` will be raised if the URL is
        malformed.
        :param url: `str`
            A string form of the URL, which must be in a stanard format for
            files, http resources, ftp resources, etc.
        """
        if self.validate_url(url):
            self.__url = url

    @property
    def data(self) -> dict:
        """
        A property accessor for the data managed by the object.  Regardless of
        the input data the returned data structure will be a dict-type for use
        with CanvasXpress.
        :returns: `dict`
            A dictionary representing a data map suitable for use with a chart.
        """
        components = urlparse(self.url)
        return components._asdict()

    @data.setter
    def data(self, data: dict) -> None:
        """
        Sets the URL using a data dict with the following attributes:
        `scheme`, `netloc`, `path`, `query`, `fragment`, `username`,
        `password`, `hostname`, `port`, `params`. `ValueError` will be
        raised if the URL is malformed.
        :param data: `dict`
            The URL as broken into a dict with the above attributes set to a
            valid string for the topic or an empty string.
        """
        if not data:
            raise ValueError("data cannot be None.")

        if not isinstance(data, dict):
            raise TypeError("data must be a type of dict")

        candidate = tuple(data)
        self.url = urlunparse(candidate)

    def get_raw_dict_form(self) -> dict:
        """
        Provides a simple dict perspective of the data with no metadata or other
        contextual transformations performed.  For example, if the data is
        natively in `dict` form then it would be passed-through with no
        modification or enhancement.
        :returns: `dict`
            The `dict` perspective of the data with as little modification or
            interpretation as is reasonable.
        """
        return {"raw": self.url}

    def render_to_dict(self, **kwargs) -> dict:
        """
        Converts the object into a dict representation.
        :returns: `dict`
            A dictionary representation of the object, such as what might be
            needed for a JSON export.
        """
        return self.get_raw_dict_form()

    @classmethod
    def validate_url(cls, url: str, detail_errors: bool = True) -> bool:
        """
        Validates that the URL conforms to a recognized standard.  URLs must
        begin with a valid scheme such as `file://` or `http://`.
        :param url: `str`
            The string form of the URL to be validated.
        :param detail_errors: `bool`
            True (default) if an exception should be raised with information
            detailing issues or errors, or `False` if the method should
            return `False` upon encountering issues.
        :returns: `bool`
            `True` if the URL is valid, or `False` if issues are found in the
             URL.  If `detail_errors` is `True` then a ValueError will instead
             be raised with information pertaining to the rejection.
        """
        try:
            components = urlparse(url)
            if not components.scheme:
                raise ValueError(
                    "URLs must specify a scheme (e.g., file://, http://, etc.)."
                )

        except ValueError as ve:
            if detail_errors:
                raise ve
            else:
                return False

        return True

    def __init__(self, data: str) -> None:
        """
        Initializes the CXUrlData object with a valid URL.  URLs must begin with
        a valid scheme such as `file://` or `http://`.  `ValueError` will be
        raised if the URL is malformed.
        :param data: `str`
            A string form of the URL, which must be in a stanard format for
            files, http resources, ftp resources, etc.
        """
        super().__init__(data)
        self.url = data
