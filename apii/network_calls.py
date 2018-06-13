from typing import Any, Dict, Optional

from apii.caller import Caller


class NetworkCalls:
    """
    Network_Calls is the last link in the chain of responsibility. Retrieving calls from the Machine_Calls,
    it prepares them for the Caller.

    This last bit of behaviour should probably be changed to an exception, but basic functionality first...
    """

    def __init__(self, caller: Caller) -> None:
        """
        Sets the Caller reference, as well as defines the API calls that this class is responsible for.
        """
        self.__sdi_id = ""
        self.__caller = caller
        self.__known_calls = ["get_networks", "create_network", "edit_network", "get_services", "add_service",
                              "edit_service", "delete_service"]

    def set_sdi_id(self, sdi: str) -> None:
        """
        Sets the SDI_id for this object, for use in all calls.
        """
        self.__sdi_id = sdi

    def make_call(self, api_call: str, args: Dict[str, Any] = {}) -> Optional[Any]:
        """
        The make_call method, called by the Machine_Calls, prepares arguments for the Caller. The argument list is converted
        from a dictionary to two dictionaries, for URL extensions and API arguments. These are then passed to the
        caller for API interaction. If the call is not known by this class, nothing is returned.
        """
        if api_call in self.__known_calls:
            extension_dict = {
                # Needed for all URLs handled by this class.
                "sdi_id": self.__sdi_id,
            }
            other_dict = {}
            for arg, val in args.items():
                if arg == "network_id" or (arg == "vid" and api_call != "add_service"):  # URL extensions only need these two parameters.
                    extension_dict[arg] = val
                else:                                  # Everything else passed as arguments.
                    other_dict[arg] = val
            return self.__caller.make_call(api_call, extension_dict, other_dict)
        return None
