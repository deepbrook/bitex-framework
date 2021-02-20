"""Customized :class:`requests.Response` class for the :mod:`bitex-framework` framework."""
# Built-in
from typing import List
import time
# Third-party
from requests.models import Response

# Home-brew
from bitex.types import KeyValuePairs, Triple


class BitexResponse(Response):
    """Custom :class:`requests.Response` class.

    Supplies additional format outputs of the underlying `JSON` data, as returned
    by :meth:`.json`.
    """

    def __init__(self):
        self.received = str(time.time())
        super(BitexResponse, self).__init__()

    def __repr__(self):
        """Extend original class's __repr__."""
        return f"<{self.__class__.__qualname__} [{self.status_code}]>"

    def triples(self) -> List[Triple]:
        """Return the data of the response in three-column layout.

        Data is returned as a list of 3-item tuples::

            [
                (<timestamp>, <label>, <value>),
                (<timestamp>, <label>, <value>),
                ...
            ]

        There are certain rows which should be always present (and are encouraged to be implemented
        by exchange plugin developers):

        - `pair`: denotes the crytpo pair a colelction of triples belongs to
        - `received`: denotes the timestamp at the time of creation of this Response, specifically, when
                the instance's :meth:`BitexResponse.__init__` method was first called.

        Also note, that the `timestamp` field in the above example **should** be the ts of the data as given by the
        exchange and is ** should not** be the timestamp of reception (i.e. instantiation of the response instance).
        The time of reception is always found at the `received` key.

        ..admonition::Disclaimer

            As these formatter functions are implemented by plugin developers, we cannot fully guarantee that the
            presented fields above are in fact **always** present. It's your duty to double-check the exchange plugin
            documentation and/or code to make sure the fields are present.

        """
        raise NotImplementedError

    def key_value_dict(self) -> KeyValuePairs:
        """Return the data of the response in a flattened dict.

        This provides the data as a dict of key-value pairs, which is ready for
        consumption by libraries such as pandas::

            {
                <label>: <value>,
                <label>: <value>,
                ...
            }

        There are certain keys which should be always present (and are encouraged to be implemented
        by exchange plugin developers):

        - `pair`: denotes the crytpo pair a colelction of kv dictionaries belongs to
        - `received`: denotes the timestamp at the time of creation of this Response, specifically, when
                the instance's :meth:`BitexResponse.__init__` method was first called.

        ..admonition::Disclaimer

            As these formatter functions are implemented by plugin developers, we cannot fully guarantee that the
            presented fields above are in fact **always** present. It's your duty to double-check the exchange plugin
            documentation and/or code to make sure the fields are present.
        """
        raise NotImplementedError
