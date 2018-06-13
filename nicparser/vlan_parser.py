from pyshark.packet.packet import Packet

from database.parser_interface import ParserInterface
from nicparser.ip_parser import IPParser
from nicparser.parse import Parse

VLAN_IPV4 = 0x800

class VlanParser(Parse):
    """
    name: VlanParser
    purpose:
        Concrete VLAN parser. This takes packets with a VLAN tag and
        parses them.
        Currently it only checks for IPV4 packets.
    """

    def __init__(self, interface_object: ParserInterface) -> None:
        self.__interface_obj = interface_object

    ## first enumerate packet layers
    ## then check up from ethernet layer
    def parse_interface(self, this_packet: Packet) -> None:
        """"
          name: parse_interface
          purpose: Concrete Vlan parser
        """

        try:
            if int(this_packet.vlan.etype, 16) != VLAN_IPV4:
                raise ValueError
        except (AttributeError, ValueError):
            pass
        else:
            IPParser(self.__interface_obj, int(this_packet.vlan.id)).parse_interface(this_packet)
