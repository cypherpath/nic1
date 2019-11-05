from typing import cast

import time

import requests
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

import settings

# Flag off warnings, including skipping ssl validation
# XXX: This is an untyped function, modifying the requests stubs is the fix.
requests.packages.urllib3.disable_warnings() # type: ignore

class Authorizer:
    """
    The authorizer authenticates with the Cypherpath SDI OS API and keeps the authentication for the remainder of
    program execution. This object is created by the Driver, and passed to the APII subsystem to be used by the Caller.
    """

    def __init__(self) -> None:
        """
        Prepares future variables, and notes the initial authentication time.
        """
        self.__credentials = settings.SDIOS_CREDS
        self.__protocol = "https://"
        self.__redirect = settings.SDIOS_DOMAIN
        self.__auth_time = time.time()
        self.__tokens = {"access_token": "",
                         "token_type": "",
                         "expires_in": 0,
                         "refresh_token": "",
                         "scope": ""}
        self.__domain = "{}{}:{}@{}/api/o/token/".format(self.__protocol, self.__credentials["client_id"], self.__credentials["client_secret"], self.__redirect)
        self.__session = OAuth2Session(client=LegacyApplicationClient(client_id=self.__credentials["client_id"]))

    def connect(self) -> OAuth2Session:
        """
        Connect authenticates with the API for the first time. If no credentials are defined, load is called first
        using default parameters. Libraries are then used to generate the authentication tokens. The session, used to
        make future requests, is returned.
        """
        try:
            self.__tokens = self.__session.fetch_token(token_url=self.__domain, verify=settings.SDIOS_VERIFY_SSL,
                                                       tenancy=self.__credentials["tenancy"],
                                                       username=self.__credentials["username"],
                                                       password=self.__credentials["password"],
                                                       client_id=self.__credentials["client_id"],
                                                       client_secret=self.__credentials["client_secret"])
        except Exception as e:
            print("Error trying to fetch SDI OS token, check SDIOS_CREDS in settings.py: ", e)
            exit(-1)
        self.__auth_time = time.time()  # Saved  for future refreshing.
        return self.__session

    def refresh_tokens(self) -> OAuth2Session:
        """
        The refresh_tokens method re-authenticates using the refresh token provided with the other tokens. If the current
        tokens are valid for two minutes or less, then a new session is created using the refresh token, replacing the
        old one. The current session (new or old) is returned.
        NOTE: This will not succeed (and all future calls will fail) if the tokens were retrieved
        more than 24 hours before this call. Such a case is outside the foreseeable scope of this program.
        """
        expires = cast(int, self.__tokens["expires_in"])

        if (time.time() - self.__auth_time) >= expires - 120:  # Time to refresh!
            self.__tokens = self.__session.refresh_token(self.__domain, self.__tokens["refresh_token"],
                                                         timeout=expires,
                                                         verify=settings.SDIOS_VERIFY_SSL)
            self.__auth_time = time.time()                                    # Saved for future refreshing.
        return self.__session

    def get_domain(self) -> str:
        """
        Returns the first half of the URL for all calls to the SDI OS API, used both internally and by the Caller.
        """
        return "{}{}/api/".format(self.__protocol, self.__redirect)

    def get_username(self) -> str:
        """
        Returns the username used to authenticate. Required to define the user by the Driver and APII.
        """
        return self.__credentials["username"]
