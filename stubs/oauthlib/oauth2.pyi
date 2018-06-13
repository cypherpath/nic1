from typing import Any, Callable, Dict, List

from oauthlib.common import generate_token


AUTH_HEADER = "auth_header"


class Client:
    def __init__(self,
            default_token_placement: str=AUTH_HEADER,
            token_type: str="Bearer",
            access_token: str=None,
            refresh_token: str=None,
            mac_key: str=None,
            mac_algorithm: str=None,
            token: Dict[str, Any]=None,
            scope: List[Any]=None,
            state: str=None,
            redirect_url: str=None,
            state_generator: Callable[[int, str], str]=generate_token) -> None: ...


class LegacyApplicationClient(Client):
    def __init__(self, client_id: str, **kwargs: Dict[str, Any]) -> None: ...


class RequestValidator: ...
class Server: ...


# vim: filetype=python :
