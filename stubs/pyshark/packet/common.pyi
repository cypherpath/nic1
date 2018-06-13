from typing import Any, Dict, Generic, List


class Pickleable:
    def __getstate__(self) -> Dict[Any, Any]: ...
    def __setstate__(self, data: Dict[Any, Any]) -> None: ...


class SlotsPickleable:
    __slots__ = [] # type: List[Any]

    def __getstate__(self) -> Dict[Any, Any]: ...
    def __setstate__(self, data: Dict[Any, Any]) -> None: ...


# vim: filetype=python :
