"""Custom :class:`requests.HTTPAdapter` for :mod:`bitex-framework`."""
# Third-party
from requests.adapters import HTTPAdapter
from requests.cookies import extract_cookies_to_jar
from requests.structures import CaseInsensitiveDict
from requests.utils import get_encoding_from_headers
from urllib3.response import HTTPResponse

# Home-brew
from bitex.plugins import list_loaded_plugins
from bitex.request import BitexPreparedRequest
from bitex.response import BitexResponse


class BitexHTTPAdapter(HTTPAdapter):
    """Custom HTTP Adapter for :mod:`Bitex`.

    It replaces :class:`requests.Response` as the default response class when
    building the response, with either an adequate plugin-supplied class or
    :mod:`bitex-framework` 's own default :class:`BitexResponse` class.
    """

    def build_response(self, req: BitexPreparedRequest, resp: HTTPResponse) -> BitexResponse:
        """Build a :class:`BitexResponse` from the given `req` and `resp`.

        The method is largely identical to :meth:`HTTPAdapter.build_response`,
        and only differs in the class type used when constructing a response.

        This class is taken firstly from any valid plugin that supplies an
        adequate class for the exchange that was queried (as stated in
        :attr:`BitexPreparedRequest.exchange`), or :mod:`bitex-framework` 's own default
        :class:`BitexResponse` class.

        :param BitexPreparedRequest req:
            The :class:`BitexPreparedRequest` used to generate the response.
        :param HTTPResponse resp: The urllib3 response object.
        """
        if req.exchange in list_loaded_plugins():
            response = list_loaded_plugins()[req.exchange]["Response"]()
        else:
            response = BitexResponse()

        # Fallback to None if there's no status_code, for whatever reason.
        response.status_code = getattr(resp, "status", None)

        # Make headers case-insensitive.
        response.headers = CaseInsensitiveDict(getattr(resp, "headers", {}))

        # Set encoding.
        response.encoding = get_encoding_from_headers(response.headers)
        response.raw = resp
        response.reason = response.raw.reason

        if isinstance(req.url, bytes):
            response.url = req.url.decode("utf-8")
        else:
            response.url = req.url

        # Add new cookies from the server.
        extract_cookies_to_jar(response.cookies, req, resp)

        # Give the Response some context.
        response.request = req
        response.connection = self

        return response
