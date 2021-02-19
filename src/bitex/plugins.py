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
    from bitex.plugins import hookimpl

    # Home-brew
    from bitex.plugins.uberex.classes import UberExAuth, UberExRequest, UberExResponse

    @hookimpl
    def announce_plugin() -> Union[
        Tuple[str, Type[HTTPBasicAuth], Type[PreparedRequest], Type[Response]], None
    ]:
        return "uberex", UberExAuth, UberExRequest, UberExResponse
"""
# Built-in
from typing import Tuple, Type, Union

# Third-party
import pluggy
from requests import PreparedRequest, Response
from requests.auth import AuthBase, HTTPBasicAuth

hookspec = pluggy.HookspecMarker("bitex")
hookimpl = pluggy.HookimplMarker("bitex")


class AnnouncePluginHookSpec:
    @hookspec
    def announce_plugin(
        self,
    ) -> Union[Tuple[str, Type[AuthBase], Type[PreparedRequest], Type[Response]], None]:
        """Announce plugin classes to :mod:`bitex-framework`.

        The function should return a tuple with the following items:

            * the exchange name this plugin is for
            * the auth class to use when generating authentication signatures for it
            * the prepared request class to use when prepping for transmission
            * the response class to use when generating a response from the exchange.
        """


class AnnouncePluginHookImpl:
    @hookimpl
    def announce_plugin() -> Union[
        Tuple[str, Type[HTTPBasicAuth], Type[PreparedRequest], Type[Response]], None
    ]:
        """Register a plugin's custom classes to :mod:`bitex-framework`.

        By default we return a tuple of :class:`str("base")`, :class:`.HTTPBasicBase`,
        :class:`.PreparedRequest` and :class:`.Response`.
        """
        return "base", HTTPBasicAuth, PreparedRequest, Response


def get_plugin_manager():
    """Fetch pluggy's plugin manager for our library."""
    pm = pluggy.PluginManager("bitex")
    pm.add_hookspecs(AnnouncePluginHookSpec)
    pm.load_setuptools_entrypoints("bitex")
    pm.register(AnnouncePluginHookImpl)
    return pm


pm = get_plugin_manager()

HOOKS = pm.hook

PLUGINS = {
    plugin_name: {"Auth": auth_class, "PreparedRequest": prep_class, "Response": resp_class}
    for plugin_name, auth_class, prep_class, resp_class in pm.hook.announce_plugin()
    if all(callable(cls) for cls in (auth_class, prep_class, resp_class))
}
