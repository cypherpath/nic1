from typing import Any
from pyshark.packet.common import Pickleable


class Layer(Pickleable):
    def __getattr__(self, item: str) -> Any: ...


# vim: set filetype=python :
