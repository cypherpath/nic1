import pyshark

from database.db import Database
from database.parser_interface import ParserInterface
from nicparser.dhcp_parser import DHCPParser
from nicparser.ip_parser import IPParser
from nicparser.vlan_parser import VlanParser

class Parser:
    """
    name: Parser
    responsibility: This class parses pcap files and inputs packet information into the database
                    It uses pyshark to do most of the heavy lifting, with the exception of DHCP
                    parameter request lists.
    """
    def __init__(self, database: Database) -> None:
        interface = ParserInterface(database)

        self.__ip_parser = IPParser(interface)
        self.__vlan_parser = VlanParser(interface)
        self.__dhcp_parser = DHCPParser(interface)

    def parse_file(self, file_str: str) -> None:
        """
        name: parse_file
        purpose: Takes in a pcap file and delagates, packet by packet to one of the
                 concrete stategy classes.

        """
        capture = pyshark.FileCapture(file_str)

        for packet in capture:
            layers = [layer.layer_name for layer in packet.layers]

            if "bootp" in layers:
                self.__dhcp_parser.parse_interface(packet)
            elif "vlan" in layers:
                self.__vlan_parser.parse_interface(packet)
            elif "ip" in layers:
                self.__ip_parser.parse_interface(packet)
