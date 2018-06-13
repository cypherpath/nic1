from typing import Any, Dict, Iterator


class Capture: ...
class FileCapture(Capture):
    def __init__(self,
            input_file: str=None,
            keep_packets: bool=True,
            display_filter: str=None,
            only_summaries: bool=False,
            decryption_key: str=None,
            encryption_type: str="wpa-pwk",
            decode_as: Dict[str, Any]=None,
            disable_protocol: bool=None,
            tshark_path: str=None,
            override_prefs: Dict[str, Any]=None,
            use_json: bool=False,
            output_file: str=None,
            include_raw: bool=None) -> None: ...

    def __iter__(self) -> Iterator[Any]: ...


# vim: filetype=python :
