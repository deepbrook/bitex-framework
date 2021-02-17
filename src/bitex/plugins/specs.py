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
