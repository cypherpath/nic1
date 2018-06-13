from pyshark.packet.packet import Packet

class Parse:
    """"
    name: Parse
    responsibility: Strategy Interface for parsing of various types of packets

    """
    def parse_interface(self, this_packet: Packet) -> None:
        raise NotImplementedError("Parse.parse_interface not implemented")
