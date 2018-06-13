from typing import Any, Dict, Optional

from apii.network_calls import Caller, NetworkCalls


class MachineCalls:
    """
    Machine_Calls class is the second link in the chain or responsibility. Retrieving calls from the SDI_Calls, it either
    prepares those calls for the Caller or passes it to the Network_Calls class.
    """

    def __init__(self, caller: Caller) -> None:
        """
        Sets and passes the Caller reference, as well as defines the API calls that this class is responsible for.
        """
        self.__sdi_id = ""
        self.__caller = caller
        self.__network_calls = NetworkCalls(caller)
        self.__known_calls = ["get_machines", "create_machine", "edit_machine", "get_machine_interfaces",
                              "create_machine_interface", "edit_machine_interface", "delete_machine_interface",
                              "add_machine_vlan", "edit_machine_vlan", "delete_machine_vlan",
                              "get_drives", "attach_drive", "edit_disk", "remove_disk", "reorder_drives"]

    def set_sdi_id(self, sdi: str) -> None:
        """
        Sets the SDI_id for this object and the Network_Calls object, for use in all calls.
        """
        self.__sdi_id = sdi
        self.__network_calls.set_sdi_id(sdi)

    def get_sdi_id(self) -> str:
        return self.__sdi_id

    def make_call(self, api_call: str, args: Dict[str, Any] = {}) -> Optional[Any]:
        """
        The make_call method, called by the SDI_Calls, prepares arguments for the Caller. If the API call needed is to
        be handled here, the argument list is converted from a dictionary to two dictionaries, for URL extensions
        and API arguments. These are then passed to the caller for API interaction. If the call is not known by
        this class, it is passed to the next class in the chain.
        """
        if api_call in self.__known_calls:
            extension_dict = {
                # Needed for all URLs handled by this class.
                "sdi_id": self.__sdi_id,
            }
            other_dict = {}
            for arg, val in args.items():                                                # URL extensions only need these params.
                if (arg == "machine_id") or (arg == "interface_id") or (arg == "disk_slot") or (arg == "vlan_id" and api_call != "add_machine_vlan"):
                    extension_dict[arg] = val
                else:                                                          # Everything else passed as arguments.
                    other_dict[arg] = val
            return self.__caller.make_call(api_call, extension_dict, other_dict)
        return self.__network_calls.make_call(api_call, args)
