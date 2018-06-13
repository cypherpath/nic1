from typing import Any, Dict, List, Callable

from requests import Session
from oauthlib.oauth2 import Client


class OAuth2Session(Session):
    def __init__(self,
            client_id: str=None,
            client: Client=None,
            auto_refresh_url: str=None,
            auto_refresh_kwargs: Dict[Any, Any]=None,
            scope: List[Any]=None,
            redirect_uri: str=None,
            token: Dict[Any, Any]=None,
            state: str=None,
            token_updater: Callable[[str], None]=None,
            **kwargs: Any) -> None: ...

    def fetch_token(self,
            token_url: str,
            code: str=None,
            authorization_response: str=None,
            body: str="",
            auth: Any=None,
            username: str=None,
            password: str=None,
            method: str="POST",
            timeout: int=None,
            headers: Dict[Any, Any]=None,
            verify: bool=True,
            proxies: Any=None,
            **kwargs: Any) -> Dict[Any, Any]: ...

    def refresh_token(self,
            token_url: str,
            refresh_token: Any=None,
            body: str="",
            auth: Any=None,
            timeout: int=None,
            headers: Any=None,
            verify: bool=True,
            proxies: Any=None,
            **kwargs: Any) -> Dict[Any, Any]: ...


# vim: filetype=python :
