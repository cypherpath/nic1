from typing import Any, Dict, Optional

from apii.machine_calls import Caller, MachineCalls


class SDICalls:
    """
    SDI_Calls class is the first link in the chain or responsibility. Retrieving calls from the APII, it either prepares
    those calls for the Caller or passes it to the Machine_Calls class. Calls prepared here change the SDI settings.
    """

    def __init__(self, caller: Caller) -> None:
        """
        Sets and passes the Caller reference, as well as defines the API calls that this class is responsible for.
        """
        self.__caller = caller
        self.__machine_calls = MachineCalls(caller)
        self.__known_calls = ["get_users", "get_sdis", "create_sdi", "edit_sdi", "run_sdi", "configure_sdi"]

    def get_sdi_id(self) -> str:
        return self.__machine_calls.get_sdi_id()

    def make_call(self, api_call: str, args: Dict[str, Any] = {}) -> Optional[Any]:
        """
        The make_call method, called by the APII, prepares arguments for the Caller. If the API call needed is to be
        handled here, the argument list is converted from a single dict to two dictionaries, for URL extensions and
        API arguments. These are then passed to the caller for API interaction. If an SDI is created, the id is saved in
        the Machine_Calls class. If the call is not known by this class, it is passed to the next class in the chain.
        """
        if api_call in self.__known_calls:
            extension_dict = dict()
            other_dict = dict()
            for arg, val in args.items():
                if arg == "user_pk" or arg == "sdi_id":  # URL extensions only need these two params.
                    extension_dict[arg] = val
                else:                                  # Everything else passed as arguments.
                    other_dict[arg] = val
            response = self.__caller.make_call(api_call, extension_dict, other_dict)
            if api_call == "create_sdi" and response is not None:
                self.__machine_calls.set_sdi_id(response["sdi_id"])
            return response
        else:
            return self.__machine_calls.make_call(api_call, args)
