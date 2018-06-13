from typing import Optional

"""
Data Packets:
These will behave mostly like structs as they are used to
store the granular data fields of different network packets
which will be parsed out by the parser
"""

class IPPacket:
    """
    Class Name: IPPacket
    Responsibility: Store data from ip packets
    """

    source_port = None  # type: Optional[int]
    dest_port = None  # type: Optional[int]
    vlan_id = None  # type: Optional[int]
    host = None  # type: Optional[str]
    user_agent = None  # type: Optional[str]
    server = None  # type: Optional[str]

    def __init__(self, source_ip: str, dest_ip: str, source_mac: str, dest_mac: str) -> None:
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_mac = source_mac
        self.dest_mac = dest_mac

class DHCPPacket:
    """
    Class Name: DHCPPacket
    Responsibility: Store data from dhcp packets
    """

    client_ip = None  # type: Optional[str]
    client_mac = None  # type: Optional[str]
    server_ip = None  # type: Optional[str]
    server_mac = None  # type: Optional[str]
    request = False
