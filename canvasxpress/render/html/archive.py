import base64
from datetime import datetime
import mimetypes
import sys
from typing import Callable
from urllib.parse import quote
from urllib.parse import urljoin
from urllib.parse import urlparse

import bs4
import requests


def get_available_parsers():
    """Return a list of parsers that can be used."""
    available = []
    for p in ["lxml", "html5lib", "html.parser"]:
        try:
            bs4.BeautifulSoup("", p)
        except bs4.FeatureNotFound:
            # Try the next parser
            continue
        else:
            available.append(p)
    return available


def _get_resource(resource_url: str) -> (str, bytes):
    """Download or reads a file (online or local).

    Parameters:
        resource_url (str): URL or path of resource to load
    Returns:
        str, bytes: Tuple containing the resource's MIME type and its data.
    Raises:
        NameError: If an HTTP request was made and ``requests`` is not available.
        ValueError: If ``resource_url``'s protocol is invalid.
    """
    url_parsed = urlparse(resource_url)
    if url_parsed.scheme in ["http", "https"]:
        request = requests.get(resource_url)
        data = request.content
        if "Content-Type" in request.headers:
            mimetype = request.headers["Content-Type"]
        else:
            mimetype = mimetypes.guess_type(resource_url)

    elif url_parsed.scheme == "":
        # '' is local file
        with open(resource_url, "rb") as f:
            data = f.read()
        mimetype, _ = mimetypes.guess_type(resource_url)

    elif url_parsed.scheme == "data":
        raise ValueError("Resource path is a data URI", url_parsed.scheme)

    else:
        raise ValueError("Not local path or HTTP/HTTPS URL", url_parsed.scheme)

    return mimetype, data


def make_data_uri(mimetype: str, data: bytes) -> str:
    """Convert data into an encoded data URI.

    Parameters:
        mimetype (str): String containing the MIME type of data (e.g.
            image/jpeg). If ``None``, will be treated as an empty string,
            equivalent in data URIs to ``text/plain``.
        data (bytes): Raw data to be encoded.
    Returns:
        str: Input data encoded into a data URI.
    """
    mimetype = "" if mimetype is None else mimetype
    if mimetype in ["", "text/css", "application/javascript"]:
        # Text data can simply be URL-encoded
        encoded_data = quote(data.decode())

    else:
        mimetype = mimetype + ";base64"
        encoded_data = base64.b64encode(data).decode()

    return "data:{},{}".format(mimetype, encoded_data)


def convert_page(
    page_text: str,
    parser: str = "auto",
    callback: Callable[[str, str, str], None] = lambda *_: None,
    ignore_errors: bool = False,
    ignore_images: bool = False,
    ignore_css: bool = False,
    ignore_js: bool = False,
) -> str:
    """Take an HTML file or URL and outputs new HTML with resources as data URIs.

    Parameters:
        pageurl (str): URL or path of web page to convert.
    Keyword Arguments:
        parser (str): HTML Parser for Beautiful Soup 4 to use. See
            `BS4's docs. <http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser>`_
            Default: 'auto' - Not an actual parser, but tells the library to
            automatically choose a parser.
        ignore_errors (bool): If ``True`` do not abort on unreadable resources.
            Unprocessable tags (e.g. broken links) will simply be skipped.
            Default: ``False``
        ignore_images (bool): If ``True`` do not process ``<img>`` tags.
            Default: ``False``
        ignore_css (bool): If ``True`` do not process ``<link>`` (stylesheet) tags.
            Default: ``False``
        ignore_js (bool): If ``True`` do not process ``<script>`` tags.
            Default: ``False``
        callback (function): Called before a new resource is processed. Takes
            three parameters: message type ('INFO' or 'ERROR'), a string with
            the category of the callback (usually the tag related to the
            message), and the message data (usually a string to be printed).
    Returns:
        str: The new webpage HTML.
    Raises:
        OSError: Error reading a file
        ValueError: Problem with a path/URL
        requests.exceptions.RequestException: Problem getting remote resource
        NameError: HTMLArk requires Requests to be installed to get resources
            from the web. This error is raised when an external URL is
            encountered.
    Examples:
        A very basic conversion of a local HTML file, using default settings:

        >>> convert_page("webpage.html")
        <Converted page HTML>

        However, that example will fail if there are any problems accessing
        linked resources in the HTML (e.g. a missing image). If you cannot
        verify the validity of links ahead of time (converting a downloaded
        web page, for example) you can disable failing on error:

        >>> convert_page("brokenpage.html", ignore_errors=True)
        <Converted page HTML, tags with broken links untouched>

        You can also skip processing of content types:

        >>> convert_page("webpage.html", ignore_images=True)
        <Converted page HTML, with <img> tags untouched>

        If you want to get feedback on the progress of the conversion, you can
        define a callback function. For example, a callback that prints all
        CSS-related errors to stdout (note that ignore_errors will bypass
        broken links but still report them to the callback):

        >>> def mycallback(message_type, message_category, message):
        ...     if message_type == 'ERROR' and message_category == 'link':
        ...         print(message)
        >>> convert_page("badcss.html", ignore_errors=True, callback=mycallback)
        <Converted page HTML, CSS links untouched, CSS errors printed to screen>
    """
    # so the user can try another when one fails
    if parser == "auto":
        parser = get_available_parsers()[0]
    soup = bs4.BeautifulSoup(page_text, parser)
    callback("INFO", "parser", "Using parser " + parser)

    tags = []

    # Gather all the relevant tags together
    if not ignore_images:
        tags += soup("img")
    if not ignore_css:
        csstags = soup("link")
        for css in csstags:
            if "stylesheet" in css["rel"]:
                tags.append(css)
    if not ignore_js:
        scripttags = soup("script")
        for script in scripttags:
            if "src" in script.attrs:
                tags.append(script)

    # Convert the linked resources
    for tag in tags:
        tag_url = tag["href"] if tag.name == "link" else tag["src"]
        try:
            # BUG: doesn't work if using relative remote URLs in a local file
            fullpath = urljoin(page_path, tag_url)
            tag_mime, tag_data = _get_resource(fullpath)
        except requests.RequestException:
            callback("ERROR", tag.name, "Can't access URL " + fullpath)
            if not ignore_errors:
                raise
        except OSError as e:
            callback(
                "ERROR",
                tag.name,
                "Error reading '{}': {}".format(e.filename, e.strerror),
            )
            if not ignore_errors:
                raise
        except ValueError as e:
            # Raised when a problem with the URL is found
            scheme = e.args[1]
            # Don't need to process things that are already data URIs
            if scheme == "data":
                callback("INFO", tag.name, "Already data URI")
            else:
                # htmlark can only get from http/https and local files
                callback("ERROR", tag.name, "Unknown protocol in URL: " + tag_url)
                if not ignore_errors:
                    raise
        except NameError as e:
            # Requests module is not available
            callback("ERROR", tag.name, str(e))
            if not ignore_errors:
                raise
        else:
            encoded_resource = make_data_uri(tag_mime, tag_data)
            if tag.name == "link":
                tag["href"] = encoded_resource
            else:
                tag["src"] = encoded_resource
            callback("INFO", tag.name, tag_url)
        # Record the original URL so the original HTML can be recovered
        tag.insert_after(bs4.Comment("URL:" + tag_url))

    soup.html.insert_after(
        bs4.Comment(
            "Generated by HTMLArk {}. Original URL {}".format(datetime.now(), page_path)
        )
    )
    return str(soup)
