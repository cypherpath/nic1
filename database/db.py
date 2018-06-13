from typing import Any, Dict, List, Optional, Set, Tuple

import sqlite3

from database.data_packets import DHCPPacket, IPPacket


class Database:
    """
    Class Name: Database
    Responsibility: Provide database bookkeeping operations to house data.
    """

    def __init__(self) -> None:
        """
        Method Name: __init__
        Purpose: Load database schema, initialize database.
        """

        # Store database instance in memory
        self.__database = sqlite3.connect(":memory:")
        self.__cursor = self.__database.cursor()

        # Read in database schema and execute, initializing database
        with open("database/DatabaseSchema.sql") as f:
            self.__cursor.executescript(f.read())

    #=================================================================================================
    # Data Access Methods
    #=================================================================================================

    def print_all_tables(self) -> None:
        """
        Method Name: print_all_tables
        Purpose:    Print the entire contents of the database
        Notes:        It is useful to track vlan info, so this method
                    provides additional information regarding vlans
        """

        # Select all table names from database
        # For each table name, call __print_table
        # Count vlans
        for row in self.__database.execute("SELECT * FROM sqlite_master WHERE type='table';"):
            self.__print_table(str(row[1]))

        # Print vlan data
        print("vlans:\n[vlan, count]")
        vlan_num = 0
        for row in self.__cursor.execute("SELECT vlan, COUNT(vlan) FROM IPs GROUP BY vlan"):
            if row[0] != 1:
                print(row)
                vlan_num = vlan_num + 1

        print("\ntotal vlans: {}".format(vlan_num))

    def __print_table(self, table_name: str) -> None:
        """
        Method Name: __print_table
        Purpose: Print the entire contents of the specified table
        """

        # Print table name
        display = "{}: ".format(table_name)
        print(display)

        # Get table information
        # Store and print col names
        col_names = [row[1] for row in self.__cursor.execute("PRAGMA table_info({})".format(table_name))]
        print(col_names)

        # Select table data
        # Print table data
        rows = self.__cursor.execute("SELECT * FROM {}".format(table_name))
        for row in rows:
            print(row)
        print()

    def get_networks(self) -> List[Dict[str, Any]]:
        """
        Method Name: get_networks
        Purpose:
        """

        return [{"network": row[0], "mask": row[1], "vlan": row[2]}
                for row in self.__cursor.execute("SELECT network, mask, vlan FROM Networks")]

    def get_routers(self) -> List[str]:
        """
        Method Name: get_routers
        Purpose: Get a list of router machine ids from the SDI_Machines table
        """

        machine_id_query = """
        SELECT machine_id, machine_fk
        FROM SDI_Machines
        """

        router_query = """
        SELECT machine_pk
        FROM Machines
        WHERE router_confidence > machine_confidence
        """

        # Collect set of routers
        router_pk_set = {row[0] for row in self.__cursor.execute(router_query)}

        # Collect list of routers
        router_list = [row[0] for row in self.__cursor.execute(machine_id_query)
                       if row[1] in router_pk_set]

        return router_list

    def __get_server_fk(self, server: Optional[str]) -> int:
        """
        Method Name: get_server_fk
        Purpose: Get the foreign key of the specified server from the Servers table
        """

        # Get server fk matching specified server
        server_fk = self.__cursor.execute("SELECT server_pk FROM Servers WHERE server=?", (str(server),)).fetchone()[0]

        return server_fk

    def __get_user_agent_fk(self, user_agent: Optional[str]) -> int:
        """
        Method Name: get_user_agent_fk
        Purpose: Get the foreign key of the specified user_agent from the User_Agents Table
        """

        # Get user agent fk matching specified user agent
        user_agent_fk = self.__cursor.execute("SELECT user_agent_pk FROM User_Agents WHERE user_agent=?", (str(user_agent),)).fetchone()[0]

        return user_agent_fk

    def __get_host_fk(self, host: Optional[str]) -> int:
        """
        Method Name: get_host_fk
        Purpose: Get the foreign key of the specified host from the Hosts table
        """

        # get host fk matching specified host
        host_fk = self.__cursor.execute("SELECT host_pk FROM Hosts WHERE host=?", (str(host),)).fetchone()[0]

        return host_fk


    def __get_packet_type_fk(self, packet_type_name: str) -> int:
        """
        Method Name: __get_packet_type_fk
        Purpose: Get the foreign key of the specified packet type from the Packets table
        """

        # Get packet type fk matching specified packet type name
        packet_type_fk = self.__cursor.execute("SELECT packet_type_pk FROM Packet_Types WHERE type=?", (packet_type_name,)).fetchone()[0]

        return packet_type_fk

    def __get_ip_fk(self, ip: Optional[str]) -> Optional[int]:
        """
        Method Name: get_ip_fk
        Purpose: Get the foreign key of the specified ip from the IPs table
        """

        if ip is None:
            return None

        try:
            # Get ip fk from IPs table
            ip_pk = self.__cursor.execute("SELECT ip_pk FROM IPs WHERE ip=?", (ip,)).fetchone()[0]
        except TypeError:
            # If ip was not found
            return None

        return ip_pk

    def get_macs(self) -> List[str]:
        """
        Method Name: get_macs
        Purpose: Return the list of mac addresses from the Macs table
        """

        # Collect all macs from Macs table
        mac_list = [row[0] for row in self.__cursor.execute("SELECT mac FROM Macs")]

        return mac_list

    def __get_mac_fk(self, mac: Optional[str]) -> Optional[int]:
        """
        Method Name: get_mac_fk
        Purpose: Get the foreign key of the specified mac from the Macs table
        """

        if mac is None:
            return None

        try:
            # Get mac pk from Macs table
            mac_pk = self.__cursor.execute("SELECT mac_pk FROM Macs WHERE mac=?", (mac,)).fetchone()[0]
        except TypeError:
            # If mac was not found
            return None

        return mac_pk

    def get_ips(self) -> List[Dict[str, Any]]:
        """
        Method Name: get_ips
        Purpose: Return a list of dictionary values containing the ip and vlan info for each ip in the IPs table. Only used for IP packets
        """

        packet_type_fk = self.__get_packet_type_fk("IP")

        # Select source and destination packets from Packets table
        # only for IP packets
        ip_pk_set = set()  # type: Set[int]

        # Collect ip fks
        for row in self.__cursor.execute("SELECT source_ip_fk, dest_ip_fk FROM Packets WHERE packet_type_fk=?", (packet_type_fk,)):
            ip_pk_set.update(set(row))

        dict_list = []

        # Collect ip and vlan data, zip into a dictionary
        for ip_pk in ip_pk_set:
            for row in self.__cursor.execute("SELECT ip, vlan FROM IPs WHERE ip_pk=?", (ip_pk,)):
                dict_list.append({"ip": row[0], "vlan": row[1]})

        return dict_list

    def get_ip_for_mac(self, mac: str) -> List[str]:
        """
        Method Name: get_ip_for_mac
        Purpose: Get a list of ips associated with the specified mac
        """

        # Collect mac pk
        mac_pk = self.__cursor.execute("SELECT mac_pk FROM Macs WHERE mac=?", (mac,)).fetchone()[0]

        sql_query_src = """
        SELECT source_ip_fk
        FROM Packets
        WHERE source_mac_fk=?
        """

        sql_query_dst = """
        SELECT dest_ip_fk
        FROM Packets
        WHERE dest_mac_fk=?
        """

        ip_pk_set = {row[0] for row in self.__cursor.execute(sql_query_src, (mac_pk,))
                     if row[0] is not None}

        ip_pk_set.update(row[0] for row in self.__cursor.execute(sql_query_dst, (mac_pk,))
                         if row[0] is not None)

        ip_list = [self.__cursor.execute("SELECT ip FROM IPs WHERE ip_pk=?", (ip_pk,)).fetchone()[0]
                   for ip_pk in ip_pk_set]

        return ip_list

    def get_machines(self) -> List[List[Tuple[str, int]]]:
        """
        Method Name: get_machines
        Purpose: Get a list of ips associated with unique machines in the Machines table
        """

        machine_list = []
        ip_list = []

        ip_sql_query = """
            SELECT ip, vlan
            FROM IPs
            WHERE machine_fk=?
            """

        machine_pk_sql_query = """
            SELECT machine_pk
            FROM Machines
            """
        # Nested cursors are required for the following queries
        temp_cursor = self.__database.cursor()

        # Collect machine list
        for machine_pk in self.__cursor.execute(machine_pk_sql_query):
            for ip, vlan in temp_cursor.execute(ip_sql_query, (machine_pk[0],)):
                ip_list.append((ip, vlan))
            if len(ip_list) > 0:
                machine_list.append(list(ip_list))
            ip_list.clear()

        return machine_list

    def get_connections(self, ip: str, vlan: int) -> Optional[Dict[str, Any]]:
        """
        Method Name: get_connections
        Purpose: Resolves network connection for machine
        """

        try:
            # Collect ip_pk and network_fk
            res = self.__cursor.execute("SELECT ip_pk, network_fk FROM IPs WHERE ip=?", (ip,)).fetchone()
        except Exception:
            # If matching ip not found
            return None

        ip_pk = res[0]
        network_pk = res[1]

        try:
            # Collect interface_id and sdi_machine_fk
            res = self.__cursor.execute("SELECT interface_id, sdi_machine_fk FROM SDI_Interfaces WHERE ip_fk=?", (ip_pk,)).fetchone()
        except Exception:
            # If no matching ip_pk was found
            return None

        interface_id = res[0]
        sdi_machine_pk = res[1]

        try:
            # Collect machine_id
            machine_id = self.__cursor.execute("SELECT machine_id FROM SDI_Machines WHERE sdi_machine_pk=?", (sdi_machine_pk,)).fetchone()[0]
        except Exception:
            # If no matching sdi_machine_pk was found
            return None

        try:
            # Collect ids
            network_id = self.__cursor.execute("SELECT id FROM Network_ID WHERE network_fk=?", (network_pk,)).fetchone()[0]
        except Exception:
            # If no matching network_pk was found
            return None

        self.__database.commit()

        return {"network_id": network_id, "interface_id": interface_id, "machine_id": machine_id}

    #=================================================================================================
    # Data Insertion Methods
    #=================================================================================================

    def insert_interface_id(self, machine_id: str, interface_id: str, ip: str) -> bool:
        """
        Method Name: insert_interface_id
        Purpose: insert give interface_id into the database, setting relations to ip and SDI_machine_id tables
        """

        # Collect ip pk
        ip_pk = self.__cursor.execute("SELECT ip_pk FROM IPs WHERE ip=?", (ip,)).fetchone()[0]

        try:
            # Collect sdi machine pk
            entry = self.__cursor.execute("SELECT sdi_machine_pk FROM SDI_Machines WHERE machine_id=?", (machine_id,)).fetchone()[0]
        except TypeError:
            # If no matching machine_id was found
            return False

        # Enter specified entry, interface_id, and ip_pk into SDI_Interfaces
        self.__cursor.execute("INSERT INTO SDI_Interfaces(sdi_machine_fk, interface_id, ip_fk) VALUES(?, ?, ?)", (entry, interface_id, ip_pk))
        self.__database.commit()

        return True

    def insert_entry_ip_table(self, ip: str, network: Optional[str], machine_pk: int) -> None:
        """
        Method Name: insert_entry_ip_table
        Purpose: Insert given ip into IPs table setting relations to network and machine tables
        """

        # Collect network pk
        network_pk = self.__cursor.execute("SELECT network_pk FROM Networks WHERE network=?", (str(network),)).fetchone()[0]

        # Insert specified ip, network_pk, and machine_pk into IPs
        self.__cursor.execute("INSERT INTO IPs(ip, network_fk, machine_fk) VALUES(?, ?, ?)", (ip, network_pk, machine_pk))
        self.__database.commit()

    def update_ip_table(self, ip_list: List[str], machine_pk: int) -> None:
        """
        Method Name: update_ip_table
        Purpose: Update relation to machine in ip table for specified ip
        """

        # Update each ip row with ip in ip_list, inserting specified machine_pk into row
        for ip in ip_list:
            self.__cursor.execute("UPDATE IPs SET machine_fk=? WHERE ip=?", (machine_pk, ip))

        self.__database.commit()

    def insert_machine(self, mac: str, machine_confidence: float, router_confidence: float) -> int:
        """
        Method Name: insert_machine
        Purpose: Insert the specified info into the Machines table.
        """

        # Insert specified mac, machine_confidence, and router_confidence into Machines
        self.__cursor.execute("INSERT INTO Machines(mac, machine_confidence, router_confidence) VALUES(?, ?, ?)", (mac, int(machine_confidence), int(router_confidence)))
        self.__database.commit()

        return self.__cursor.lastrowid

    def insert_machine_id(self, ip: str, machine_id: str, machine_name: str) -> None:
        """
        Method Name: insert_machine_id
        Purpose: Insert the specified machine_id into SDI_Machines, setting relation to Machines
        """

        # Collect machine_pk
        machine_pk = self.__cursor.execute("SELECT machine_fk FROM IPs WHERE ip=?", (ip,)).fetchone()[0]

        # Insert specified machine_pk, machine_id, and machine_name into SDI_Machines
        self.__cursor.execute("INSERT INTO SDI_Machines(machine_fk, machine_id, name) VALUES(?, ?, ?)", (machine_pk, machine_id, machine_name))

        self.__database.commit()

    def insert_network(self, network: str, mask: str, ip: str, vlan: int) -> bool:
        """
        Method Name: insert_network
        Purpose: Insert the specified network information into the Networks table
        """

        # Query if the network vlan pair already exists
        # Store pk of network vlan pair if found (should never find more than 1) into a list
        red_pk_list = [row[0] for row in self.__cursor.execute("SELECT network_pk FROM Networks WHERE network=? AND vlan=?", (network, vlan))]
        # If the pair was unique
        if len(red_pk_list) == 0:
            # Insert it into the database
            # Ensure that we don't break any table constraints with the insert (should never except)
            try:
                self.__cursor.execute("INSERT INTO Networks(network, mask, vlan) VALUES(?, ?, ?)", (network, mask, vlan))
                # Store the pk of the inserted row (used for updating row values later)
                network_pk = self.__cursor.lastrowid
            except sqlite3.IntegrityError:
                return False
        else:
            # If the pair was redundant, grab the pk out of the list
            network_pk = red_pk_list[0]

        # Update the table with network_fk
        # Ensure we don't break any database constraints upon insert
        try:
            self.__cursor.execute("UPDATE IPs SET network_fk=? WHERE ip=? AND vlan=?", (network_pk, ip, vlan))
        except sqlite3.IntegrityError:
            return False

        return True

    def insert_network_id(self, ip: str, vlan: int, network_id: str, network_name: str) -> None:
        """
        Method Name: insert_network_id
        Purpose: Insert the specified network id and network name into the Network_ID table.
        """

        try:
            # Collect network_pk from Networks table
            network_pk = self.__cursor.execute("SELECT network_pk FROM Networks WHERE network=? AND vlan=?", (ip, vlan)).fetchone()[0]
        except TypeError:
            # If no matching ip and vlan combination was found
            network_pk = None

        if network_pk is not None:
            # Insert specified network_pk, network_id, and network_name into Network_ID table
            self.__cursor.execute("INSERT INTO Network_Id(network_fk, id, name) VALUES(?, ?, ?)", (network_pk, network_id, network_name))
            self.__database.commit()

    def insert_host(self, host: Optional[str]) -> bool:
        """
        Method Name: insert_host
        Purpose: Insert the specified host into the Hosts table
        """

        try:
            # Insert specified host into Hosts table
            self.__cursor.execute("INSERT INTO Hosts(host) VALUES(?)", (str(host),))
        except sqlite3.IntegrityError:
            # If host is already in the table
            return False

        self.__database.commit()

        return True

    def insert_user_agent(self, user_agent: Optional[str]) -> bool:
        """
        Method Name: insert_user_agent
        Purpose: Insert the specified user agent into the User_Agents table
        """

        try:
            # Insert specified user agent into User_Agents table
            self.__cursor.execute("INSERT INTO User_Agents(user_agent) VALUES(?)", (str(user_agent),))
        except sqlite3.IntegrityError:
            # If user_agent is already in the table
            return False

        self.__database.commit()

        return True

    def insert_server(self, server: Optional[str]) -> bool:
        """
        Method Name: insert_server
        Purpose: Insert the specified server into the Servers table
        """

        try:
            # Insert specified server into Servers table
            self.__cursor.execute("INSERT INTO Servers(server) VALUES(?)", (str(server),))
        except sqlite3.IntegrityError:
            # If server is already in the table
            return False

        self.__database.commit()

        return True

    def insert_ip(self, ip: str, vlan: int = 0) -> bool:
        """
        Method Name: insert_ip
        Purpose: Insert specified ip address and vlan (default 0) into the database
        Notes: Redundant ips will not be inserted due to the UNIQUE attribute in the database schema
        """

        try:
            # Insert specified ip and vlan data into IPs table
            self.__cursor.execute("INSERT INTO IPs(ip, vlan) VALUES(?, ?)", (ip, vlan))
        except sqlite3.IntegrityError:
            # If ip and vlan combination is already in the table
            return False

        self.__database.commit()

        return True

    def insert_mac(self, mac: str) -> bool:
        """
        Method Name: insert_mac
        Purpose: Insert specified mac address into the database
        Notes: Redundant ips will not be inserted due to the UNIQUE attribute in the database schema
        """

        try:
            # Insert specified mac into the Macs table
            self.__cursor.execute("INSERT INTO Macs(mac) VALUES(?)", (mac,))
        except sqlite3.IntegrityError:
            # If mac is already in the table
            return False

        self.__database.commit()

        return True

    def insert_ip_packet(self, packet: IPPacket) -> None:
        """
        Method Name: insert_ip_packet
        Purpose:Insert a unique ip packet into the database
        """

        # Get fks for packet data values
        source_ip_fk = self.__get_ip_fk(packet.source_ip)
        dest_ip_fk = self.__get_ip_fk(packet.dest_ip)
        source_mac_fk = self.__get_mac_fk(packet.source_mac)
        dest_mac_fk = self.__get_mac_fk(packet.dest_mac)
        host_fk = self.__get_host_fk(packet.host)
        user_agent_fk = self.__get_user_agent_fk(packet.user_agent)
        server_fk = self.__get_server_fk(packet.server)

        packet_query = """
            INSERT INTO Packets(    source_ip_fk, dest_ip_fk, source_mac_fk, dest_mac_fk,
                                    source_port, dest_port, packet_type_fk, host_fk,
                                    user_agent_fk, server_fk)
            VALUES(?, ?, ?, ?,
                   ?, ?, ?, ?,
                   ?, ?)
            """
        packet_values = (source_ip_fk, dest_ip_fk, source_mac_fk, dest_mac_fk,
                         packet.source_port, packet.dest_port, self.__get_packet_type_fk("IP"), host_fk,
                         user_agent_fk, server_fk)

        # Insert data into Packets table
        self.__cursor.execute(packet_query, packet_values)

        self.__database.commit()

    def insert_dhcp_packet(self, packet: DHCPPacket) -> None:
        """
        Method Name: insert_dhcp_packet
        Purpose: insert a dhcp_packet into packet table
        Notes: If we are inserting packet, it has passed redundancy check
        """

        # Get fks for packet data values
        source_ip_fk = self.__get_ip_fk(packet.client_ip)
        dest_ip_fk = self.__get_ip_fk(packet.server_ip)
        source_mac_fk = self.__get_mac_fk(packet.client_mac)
        dest_mac_fk = self.__get_mac_fk(packet.server_mac)

        packet_query = """
        INSERT INTO Packets(source_ip_fk, dest_ip_fk, source_mac_fk, dest_mac_fk, packet_type_fk)
        VALUES(?, ?, ?, ?, ?)
        """
        packet_data = (source_ip_fk, dest_ip_fk, source_mac_fk, dest_mac_fk,
                       self.__get_packet_type_fk("DHCP"))

        # Insert data into packets table
        self.__cursor.execute(packet_query, packet_data)
        # Collect row id of inserted packet
        _id = self.__cursor.lastrowid

        # Insert id and packet.request into Services table
        self.__cursor.execute("INSERT INTO Services( packet_fk, req_res_flag) VALUES(?, ?)", (_id, packet.request))
        self.__database.commit()
