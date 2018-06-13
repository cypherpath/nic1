from pyshark.packet.packet import Packet

from database.data_packets import IPPacket
from database.parser_interface import ParserInterface
from nicparser.parse import Parse

class IPParser(Parse):
    """
    name: IPParser
    responsibility: Concrete stategy for parsing ip packets
                   This class takes a pyshark packet and inserts
                   an IPPacket into the database
    """

    def __init__(self, interface_object: ParserInterface, vlan_id: int = 1) -> None:
        self.__interface_obj = interface_object
        self.__vlan_id = vlan_id

    # first enumerate packet layers
    # then check up from ethernet layer
    def parse_interface(self, this_packet: Packet) -> None:
        """"
        name: parse_interface
        purpose: Concrete IP parser

        """

        # Get layers typs in packet for checking packet type
        layers = [layer.layer_name for layer in this_packet.layers]

        # This only supports IP over Ethernet.
        if "ip" not in layers or "eth" not in layers:
            return

        packet = IPPacket(this_packet["ip"].src, this_packet["ip"].dst, this_packet["eth"].src, this_packet["eth"].dst)

        # If packet is a TCP packet grab tcp port
        if "tcp" in layers:
            try:
                packet.source_port = this_packet["tcp"].srcport
                packet.dest_port = this_packet["tcp"].dstport
            except AttributeError:
                packet.source_port = None
                packet.dest_port = None

        # If packet is UDP grab port
        if "udp" in layers:
            try:
                packet.source_port = this_packet["udp"].srcport
                packet.dest_port = this_packet["udp"].dstport
            except AttributeError:
                packet.source_port = None
                packet.dest_port = None

        if "http" in layers:
            try:
                if "user_agent" in this_packet.http.field_names:
                    packet.user_agent = this_packet.http.user_agent
                else:
                    packet.user_agent = None

                if "server" in this_packet.http.field_names:
                    packet.server = this_packet.http.server
                else:
                    packet.server = None

                if "host" in this_packet.http.field_names:
                    packet.host = this_packet.http.host
                else:
                    packet.host = None
            except AttributeError:
                packet.host = None
                packet.server = None
                packet.user_agent = None

        packet.vlan_id = self.__vlan_id

        self.__interface_obj.insert_ip_packet(packet)
