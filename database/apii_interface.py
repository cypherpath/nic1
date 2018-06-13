from typing import Any, Dict, List, Optional, Tuple

from database.db import Database

class APIIInterface:
    """
    Class Name: APIIInterface
    Purpose: Provide an interface to the database for the APII module
    """

    def __init__(self, database: Database) -> None:
        self.__database = database

    def get_networks(self) -> List[Dict[str, Any]]:
        """
        Method Name: get_networks
        Purpose: return a list of "interpreted" networks stored in the database
        """
        return self.__database.get_networks()

    def insert_network_id(self, ip: str, vlan: int, network_id: str, network_name: str) -> None:
        """
        Method Name: insert_network_id
        Purpose: insert unique network id returned from cypherpaths SDIOS restful
        """
        self.__database.insert_network_id(ip, vlan, network_id, network_name)

    def insert_interface_id(self, machine_id: str, interface_id: str, ip: str) -> None:
        """
        Method Name: insert_interface_id
        Purpose: Insert interface id passed from APII module into the database
        """
        self.__database.insert_interface_id(machine_id, interface_id, ip)

    def get_machines(self) -> List[List[Tuple[str, int]]]:
        """
        Method Name: get_machines
        Purpose: Return a list of all "interpreted" machines stored in the Database
        """
        return self.__database.get_machines()

    def insert_machine_id(self, ip: str, machine_id: str, machine_name: str) -> None:
        """
        Method Name: insert_machine_id
        Purpose: insert machine id passed from APII module into the database
        """
        self.__database.insert_machine_id(ip, machine_id, machine_name)

    def get_connections(self, ip: str, vlan: int) -> Optional[Dict[str, Any]]:
        """
        Method Name: get_connections
        Purpose: Return network id that machine at ip is connected to
        """
        return self.__database.get_connections(ip, vlan)

    def get_routers(self) -> List[str]:
        """
        Method Name: get_routers
        Purpose: return a list of ip that have been "interpreted" to be routers
        """
        return self.__database.get_routers()
