from typing import Any, Iterable, List
from pyshark.packet.common import Pickleable
from pyshark.packet.layer import Layer


class Packet(Pickleable):
    layers = None # type: Iterable[Layer]

    def __init__(self,
            layers: List[Layer]=None,
            frame_info: Layer=None,
            captured_length: float=None,
            sniff_time: float=None,
            interface_captured: str=None) -> None: ...

    def __getattr__(self, item: str) -> Layer: ...
    def __getitem__(self, item: str) -> Layer: ...


# vim: filetype=python :
