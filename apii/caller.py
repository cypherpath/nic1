"""
Caller class interacts with the SDI OS API directly, returning responses to the requester.
"""

from typing import Any, Dict, Optional

from apii.api_calls import CALLS, Method
from authorizer.authorizer import Authorizer


class Caller:
    def __init__(self, authorizer: Authorizer) -> None:
        """
        Uses the passed-in Authorizer to connect to the SDI API, then sets default values.
        """
        self.__authorizer = authorizer
        self.__session = authorizer.connect()
        self.__domain = authorizer.get_domain()

    def get_domain(self) -> str:
        return self.__domain[:-4]

    def make_call(self, command: str, extensions: Dict[str, Any], api_args: Dict[str, Any]) -> Optional[Any]:
        """
        This method makes a request to the Cypherpath SDI OS API. It finds the call required via the APICalls dictionary.
        It then constructs the URL based upon this and the extensions argument. The remaining data is then reformed into
        the body of the coming HTTP request. Finally, based upon the request type of the call needed, a request is made to
        the SDI OS API. The response is formatted and returned to the requester, or an error is generated if the HTTP
        request failed.
        """
        self.__session = self.__authorizer.refresh_tokens()
        command_info = CALLS[command]
        extension = command_info.path.format(**extensions)
        request_type = command_info.method

        body = {key: val for key, val in api_args.items()
                if key in command_info.args}

        url = "{}{}".format(self.__domain, extension)

        if request_type == Method.GET:
            response = self.__session.get(url)
        elif request_type == Method.POST:
            response = self.__session.post(url, data=body)
        elif request_type == Method.PUT:
            response = self.__session.put(url, data=body)
        elif request_type == Method.DELETE:
            response = self.__session.delete(url, data=body)
        else:
            return None

        if not response.ok:
            print("Error response connecting to {}".format(url))
            print("Error code: {}".format(response.status_code))
            print("Response: {}".format(response.text))
            return None

        if response.headers.get("content-type") == "application/json":
            return response.json()

        return response.text
