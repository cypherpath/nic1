from database.data_packets import DHCPPacket, IPPacket
from database.db import Database
from database.flagger import Flagger

class ParserInterface:
    """
    Class Name: ParserInterface
    Purpose: Provide an interface to the database for the Parser module
    """

    def __init__(self, database: Database) -> None:
        self.__database = database

    def insert_ip_packet(self, packet: IPPacket) -> bool:
        """
        Method Name: insert_ip_packet
        Purpose: Insert specified ip packet into the database (granulate packet data)
        Notes:     This method utilizes the Flagger object to check the packet for redundancy
                If a packet is found to be redundant, it is not inserted
        """

        # Initialize flagger, all tests must be true to pass
        flagger = Flagger()

        # If vlan is specified
        if packet.vlan_id is not None:
            # Insert vlan along with source and dest ip
            flagger.test(self.__database.insert_ip(packet.source_ip, packet.vlan_id))
            flagger.test(self.__database.insert_ip(packet.dest_ip, packet.vlan_id))
        # If vlan is not specified
        else:
            # Insert source and dest ip
            flagger.test(self.__database.insert_ip(packet.source_ip))
            flagger.test(self.__database.insert_ip(packet.dest_ip))

        # Insert granularized packet data
        flagger.test(self.__database.insert_mac(packet.source_mac))
        flagger.test(self.__database.insert_mac(packet.dest_mac))
        flagger.test(self.__database.insert_host(packet.host))
        flagger.test(self.__database.insert_user_agent(packet.user_agent))
        flagger.test(self.__database.insert_server(packet.server))

        # If the packet is not redundant
        if not flagger.all_false():
            # Insert packet into table
            self.__database.insert_ip_packet(packet)
        else:
            return False

        return True

    def insert_dhcp_packet(self, packet: DHCPPacket) -> None:
        """
        Method Name: insert_dhcp_packet
        Purpose: Insert specified DHCP packet into the database (granulate packet data)
        Notes:     This method utilizes the Flagger object to check the packet for redundancy
                If a packet is found to be redundant, it is not inserted
        """

        # Initialize flagger, all tests must be true to pass
        flagger = Flagger()

        # If packet is a request
        if packet.request and packet.client_mac is not None:
            flagger.test(self.__database.insert_mac(packet.client_mac))
        # If packet is a response
        elif not packet.request and packet.client_ip is not None and packet.server_ip is not None and packet.client_mac is not None and packet.server_mac is not None:
            flagger.test(self.__database.insert_ip(packet.client_ip))
            flagger.test(self.__database.insert_ip(packet.server_ip))
            flagger.test(self.__database.insert_mac(packet.client_mac))
            flagger.test(self.__database.insert_mac(packet.server_mac))

        # If packet is not redundant
        if not flagger.all_false():
            # Insert packet into table
            self.__database.insert_dhcp_packet(packet)
