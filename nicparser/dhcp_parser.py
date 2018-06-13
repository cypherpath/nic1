from pyshark.packet.packet import Packet
from pyshark.packet.fields import LayerField

from database.data_packets import DHCPPacket
from database.parser_interface import ParserInterface
from nicparser.parse import Parse


DHCPREQUEST = "3"
DHCPACK = "5"
DHCPINFORM = "8"


class DHCPParser(Parse):
    """
    name: DHCPParser
    responsibility: This class takes a pyshark packet and dives into dhcp options. It will take in a bootp
                    packet and search for dhcp option 55, request parameters.  It will check packet
                    type, if packet is DHCPREQUEST then it will insert client mac, and request parameter
                    list. If packet is DHCPACK then it insert client ip, dhcp server ip, and subnet
                    mask.
    """

    def __init__(self, interface_object: ParserInterface) -> None:
        self.__interface_obj = interface_object

    def parse_interface(self, this_packet: Packet) -> None:
        if "dhcp" not in this_packet.bootp.field_names:
            return

        try:
            packet = DHCPPacket()

            if this_packet.bootp.option_dhcp == DHCPREQUEST or this_packet.bootp.option_dhcp == DHCPINFORM:
                packet.server_ip = None
                packet.server_mac = None
                packet.client_ip = this_packet["ip"].src
                packet.client_mac = this_packet["eth"].src
                packet.request = True

            elif this_packet.bootp.option_dhcp == DHCPACK:
                if "option_dhcp_server_id" in this_packet.bootp.field_names:
                    packet.server_ip = this_packet.bootp.option_dhcp_server_id

                if "ip_your" in this_packet.bootp.field_names:
                    packet.client_ip = this_packet.bootp.ip_your

                # Insert DHCP packet into database.
                packet.client_mac = this_packet["eth"].dst
                packet.server_mac = this_packet["eth"].src
                packet.request = False

            self.__interface_obj.insert_dhcp_packet(packet)
        except Exception as e:
            print("Exception Raised", e)
