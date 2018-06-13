from typing import List, Tuple

import ipaddress

from database.db import Database
from nicparser.ip_classes import Classes


CLASS_A_MASK_INT = 0xff
CLASS_C_MASK_INT = 0xffffff00


class Interpreter:
    """
    Class Name: Interpreter
    Responsibility: Interprets packet data stored in the database into data that will be used by the APII.
    Specifically interpreting IPs/VLANs into networks, and mac addresses/IPs into machines.
    """

    def __init__(self, database: Database) -> None:
        self.__database = database

        # Create an instance of Classes for network masking
        self.__ip_classes = Classes()

        # Set confidence values for machine/router confidence calculations
        self.__max_confidence = 1.0
        self.__min_confidence = 0.0
        self.__confidence_incrementer = 0.16
        self.__max_ip_associations = 10


    def interpret(self) -> None:
        """
        Method Name: interpret
        Purpose: Call the specific interpreter methods
        """
        self.__interpret_networks()
        self.__interpret_machines()


    def __interpret_networks(self) -> None:
        """
        Method Name: interpret_networks
        Purpose: Take IPs stored in the database and mask it based on classful masking
        to get the network IP and network mask. The network table of the database is then
        populated with the network IP, network mask, IP, and VLAN info (if it exists).
        If there is no VLAN associated with the IP then we use the default value of "1".
        """
        # get_ips() returns list of dictionaries with ip and vlan key values
        ip_dict_list = self.__database.get_ips()
        for ip_dict in ip_dict_list:
            # Get network IP (masked_ip) and network mask based on classful masking function in ip_classes.py
            masked_ip, network_mask = self.__ip_classes.get_network_with_mask_used(ip_dict["ip"])

            if masked_ip is not None and network_mask is not None:
                self.__database.insert_network(masked_ip, network_mask, ip_dict["ip"], ip_dict["vlan"])


    def __calculate_confidence(self, mac_ip_list: List[str]) -> Tuple[float, float]:
        """
        Method Name: calculate_confidence
        Purpose: Find the router_confidence and machine_confidence for a given mac IP list.
        Method takes the list of ips associated with a mac address as an input.
        First we start with maximum machine confidence, and then increment the router confidence
        for each IP in the list. The more IPs associated with the mac address, the more confident we are
        that it is a router.
        """
        # A router has been found if the number of IP associates is greater than a specific threshold.
        if len(mac_ip_list) >= self.__max_ip_associations:
            return self.__max_confidence, self.__min_confidence

        # Increase router confidence based on number of IPs associated with the mac address
        router_confidence = len(mac_ip_list) * self.__confidence_incrementer

        # If router confidence exceeds the max confidence, we assume it is a router
        if router_confidence >= self.__max_confidence:
            return self.__max_confidence, self.__min_confidence

        # Calculate machine confidence.
        machine_confidence = self.__max_confidence - router_confidence

        return router_confidence, machine_confidence


    def __interpret_machines(self) -> None:
        """
        Method Name: interpret_machines
        Purpose: For each mac address in the database, determine if it is a router or a regular machine.
        If mac address is a router, find or create the router's IP, then insert the router's IP and all the
        IPs that are associated with the router as a machine into the machine network table. If the mac address
        is a regular machine, then just insert it as a machine into the network table.
        """
        mac_list = self.__database.get_macs()

        for mac_index, mac in enumerate(mac_list):
            mac_ip_list = self.__database.get_ip_for_mac(mac)

            # Determine if the mac is a router or a machine
            router_confidence, machine_confidence = self.__calculate_confidence(mac_ip_list)

            # If the mac address is a regular machine
            if router_confidence <= machine_confidence:
                machine = self.__database.insert_machine(mac, machine_confidence, router_confidence)
                self.__database.update_ip_table(mac_ip_list, machine)
                continue

            # Otherwise we are dealing with a router
            machine = self.__database.insert_machine(mac, machine_confidence, router_confidence)
            ip_list_copy = list(mac_ip_list)

            for ip_index, ip in enumerate(ip_list_copy):
                # Assumption: the router's IP is "#.#.#.1"
                masked_ip = self.__ip_classes.mask_ip_address(ip, CLASS_A_MASK_INT)

                # If masked ip is "1", then we have found "#.#.#.1"
                if masked_ip == 1:
                    # Associate the IP with the machine we created for the mac address
                    self.__database.update_ip_table([ip], machine)

                    # Remove it from the ip list because we already created a machine for it
                    del mac_ip_list[ip_index]
                    break
            else:
                # Take the first IP off of the list, find "#.#.#", and add 1 to get "#.#.#.1"
                masked_ip = self.__ip_classes.mask_ip_address(mac_ip_list[0], CLASS_C_MASK_INT) + 1

                network = self.__ip_classes.get_network(str(ipaddress.ip_address(masked_ip)))
                self.__database.insert_entry_ip_table(str(ipaddress.ip_address(masked_ip)), network or None, machine)

            # Keep track of number of machines associated with the mac address
            for machine_index, ip in enumerate(mac_ip_list):
                # When adding machines, the machine_conf is 1 and router_conf is 0.
                machine = self.__database.insert_machine("{}:{}".format(mac_index, machine_index), 1, 0)
                self.__database.update_ip_table([ip], machine)
