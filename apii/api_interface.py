from typing import Any, Dict, Optional

import sys

from apii.caller import Caller
from apii.sdi_calls import SDICalls
from authorizer.authorizer import Authorizer
from database.apii_interface import APIIInterface
from database.db import Database


def printnonl(msg: str) -> None:
    sys.stdout.write(msg)
    sys.stdout.flush()


class APIInterface:
    """
    APII class interacts with the driver and database to prepare calls to the Cypherpath SDI OS API.
    The calls themselves are handled by the rest of the subsystem, accessed via the authorizer and sdi_calls objects.

    Creates the caller and sdi_calls object to prepare the subsystem for future calls.
    """

    def __init__(self, authorizer: Authorizer, database: Database) -> None:
        self.__caller = Caller(authorizer)
        self.__sdi_calls = SDICalls(self.__caller)
        self.__database = APIIInterface(database)

    def __make_call(self, api_call: str, args: Dict[str, Any] = {}) -> Optional[Any]:
        """
        Private method to pass responsibility to sdi_calls.
        """
        return self.__sdi_calls.make_call(api_call, args)

    def start(self, username: str, description: str) -> None:
        """
        Start method to prepare an SDI. Gets the user defined by the username argument, then creates an SDI based on
        previously-generated runs.
        """
        users = self.__make_call("storage_general")
        if len(users) == 1:
            user_pk = users[0]["user"]
        else:
            users = self.__make_call("get_users")
            user_pk = 0  # Initial value always overwritten, as the user was authorized.
            for user in users:
                if user["username"] == username:
                    user_pk = user["pk"]
                    break
        sdis = self.__make_call("get_sdis", {"user_pk": user_pk}) or []
        sdi_num = 0
        for sdi in sdis:
            if "PCAP_SDI" in sdi["name"]:
                sdi_num += 1  # Ensures no two SDIs are named identically for that user.

        self.__make_call("create_sdi", {"user_pk": user_pk, "name": "PCAP_SDI_{}".format(sdi_num), "description": description})

    def add_machines(self) -> None:
        """
        Method to add machines to the SDI. Retrieves a list of machines from the database, each of which is a list of IPs
        used by that machine. Each machine is created and saved in the database. The information is then used to create
        network interfaces for each IP corresponding to that machine. The new interface is also saved.
        """
        machine_list = self.__database.get_machines()
        if machine_list:
            printnonl("Adding machines... ")

        for i, machine in enumerate(machine_list):                                                 # Machines default to workstations.
            printnonl("{} ".format(len(machine_list) - i))
            new_sdi_machine = self.__make_call("create_machine", {"name": "machine{}".format(i + 1), "role": "workstation"})

            if new_sdi_machine is not None:
                self.__database.insert_machine_id(machine[0][0], new_sdi_machine["id"], new_sdi_machine["name"])
                for ip, vlan in machine:                                                 # Interfaces initially unplugged.
                    new_machine_interface = self.__make_call("create_machine_interface", {"machine_id": new_sdi_machine["id"], "network": None, "nic": "e1000"})

                    if new_machine_interface is not None:
                        if 0 < vlan < 4095:
                            self.__make_call("delete_machine_vlan", {"machine_id": new_sdi_machine["id"], "interface_id": new_machine_interface["id"], "vlan_id": 1})
                            self.__make_call("add_machine_vlan", {"machine_id": new_sdi_machine["id"], "interface_id": new_machine_interface["id"], "vlan": vlan})
                        self.__database.insert_interface_id(new_sdi_machine["id"], new_machine_interface["id"], ip)

        if machine_list:
            print("0")

    def add_networks(self) -> None:
        """
        Method to add networks to the SDI. Retrieves a list of network IPs from the database. Each network is created as a
        switch, which is saved in the database for future reference.
        """
        network_list = self.__database.get_networks()
        if network_list:
            printnonl("Adding networks... ")

        for i, network in enumerate(network_list):
            printnonl("{} ".format(len(network_list) - i))
            new_switch = self.__make_call("create_network", {"name": "Network_{}".format(i + 1), "mode": "switch"})

            if new_switch is not None:
                self.__make_call("delete_service", {"network_id": new_switch["id"], "vid": 1})
                self.__make_call("add_service", {"network_id": new_switch["id"], "vid": network["vlan"]})
                self.__make_call("edit_service", {"network_id": new_switch["id"], "dhcp": True, "vid": network["vlan"], "ip": network["network"], "netmask": network["mask"]})
                self.__database.insert_network_id(network["network"], network["vlan"], new_switch["id"], new_switch["name"])

        if network_list:
            print("0")

    def connect(self) -> None:
        """
        Method to connect machines to networks. Retrieves a list of machines from the database as done in add_machines.
        Each IP is then passed to the database to return machine, interface, and network ids, saved from the earlier
        calls. These are used to edit machine interfaces to connect them to the right network.
        """
        machine_list = self.__database.get_machines()
        if machine_list:
            printnonl("Connecting machines to networks... ")

        for i, machine in enumerate(machine_list):
            printnonl("{} ".format(len(machine_list) - i))
            for ip, vlan in machine:
                connection = self.__database.get_connections(ip, vlan)
                if connection is not None:
                    self.__make_call("edit_machine_interface", {"machine_id": connection["machine_id"], "interface_id": connection["interface_id"], "network": connection["network_id"]})
                    self.__make_call("edit_machine_vlan", {"machine_id": connection["machine_id"], "interface_id": connection["interface_id"], "vlan_id": vlan, "ip": ip})

        if machine_list:
            print("0")

    def specify_machines(self) -> None:
        """
        Method to define routers in the SDI. Retrieves a list of machine IDs from the database, each of which is a
        router. The API is then called to convert those workstations to routers.
        """
        router_list = self.__database.get_routers()
        for router in router_list:
            self.__make_call("edit_machine", {"machine_id": router, "role": "router"})

    def print_success(self) -> None:
        domain = self.__caller.get_domain()
        sdi_id = self.__sdi_calls.get_sdi_id()
        print("nic1 has finished! View your SDI at {}/sdi/{}/topology_view/".format(domain, sdi_id))
