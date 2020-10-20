"""Hook Specifications for :mod:`bitex-framework`'s plugin system.

Example
-------

Say you wanted to write a plugin for exchange 'UberEx', and have developed
the following custom classes::

    >bitex/plugins/uberex/classes.py
    from bitex.request import BitexPreparedRequest
    from bitex.auth import BitexAuth
    from bitex.repsonse import BitexResponse

    class UberExRequest(BitexPreparedRequest):
        ...

    class UberExResponse(BitexResponse):
        ...

    class UberExAuth(BitexAuth):
        ...


In order to correctly register these, you'll have to write the following
hook implementation::

    >bitex_uberex/hooks.py
    # Built-in
    from typing import Mapping, Tuple, Type, Union

    # Third-party
    import pluggy

    # Home-brew
    from bitex.plugins.uberex.classes import UberExAuth, UberExRequest, UberExResponse

    hookimpl = pluggy.HookimplMarker("bitex-uberex")

    @hookimpl
    def announce_plugin() -> Union[
        Tuple[str, Type[HTTPBasicAuth], Type[PreparedRequest], Type[Response]], None
    ]:
        return "uberex", UberExAuth, UberExRequest, UberExResponse

If you want to support parsing of bitex shorthand urls, you'll also have to implement
the hook for those::

    ...
    @hookimpl
    def construct_url_from_shorthand(match_dict: Mapping[str, str]) -> Union[str, None]:
        constructed_url = f"https://uberex.com/api/v1/{match_dict[method]}"
        return constructed_url

Where `constructed_url` is obviously a dummy - it's the plugin writers responsibility
to construct an adequate url from the shorthand, factoring in any method, endpoint
and parameters given in it.

"""
# Built-in
from typing import Any, Dict, Mapping, Tuple, Type, Union

# Third-party
import pluggy
from requests import PreparedRequest, Response
from requests.auth import AuthBase

hookspec = pluggy.HookspecMarker("bitex")


@hookspec
def announce_plugin() -> Union[
    Tuple[str, Type[AuthBase], Type[PreparedRequest], Type[Response]], None
]:
    """Announce plugin classes to :mod:`bitex-framework`.

    The function should return a tuple with the following items:

        * the exchange name this plugin is for
        * the auth class to use when generating authentication signatures for it
        * the prepared request class to use when prepping for transmission
        * the response class to use when generating a response from the exchange.
    """


@hookspec
def construct_url_from_shorthand(
    match_dict: Mapping[str, str]
) -> Union[str, Tuple[str, Dict[str, Any]], None]:
    """Construct the proper REST API URL using the given `match_dict`.

    This allows users of your plugin to use the bitex short-hand for exchanges,
    when making requests.

    Note that if the matchdict contains data that needs to be send as part of the
    body, the returned value should be a tuple of `url, body_dict`.
    """


@hookspec
def format_instrument_for(instrument: str, exchange: str) -> Union[str, None]:
    """Convert the given ``instrument`` to a format accepted by ``exchange``.

    If your exchange has a different notation from most other exchanges, this hook
    is where you can ensure the instrument passed to requests made to your exchange
    is valid.
    """


@hookspec
def format_instrument_from(instrument: str, exchange: str) -> Union[str, None]:
    """Convert the given ``instrument`` from a format accepted by ``exchange`` to the bitex format.

    If your exchange has a different notation from most other exchanges, this hook
    is where you can ensure the instrument extracted from responses sent by your exchange
    is compatible with other exchanges.
    """
