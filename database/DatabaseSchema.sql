CREATE TABLE Macs
(
	mac_pk INTEGER PRIMARY KEY,
	mac TEXT UNIQUE
);

CREATE TABLE IPs
(
	ip_pk INTEGER PRIMARY KEY,
	ip TEXT UNIQUE,
	vlan    INTEGER DEFAULT 1,
	network_fk INTEGER,
	machine_fk INTEGER,
	FOREIGN KEY(network_fk) REFERENCES Networks(network_pk),
	FOREIGN KEY(machine_fk) REFERENCES Machines(machine_pk)
);


CREATE TABLE Networks
(
    network_pk INTEGER PRIMARY KEY,
    network TEXT,
    vlan INTEGER,
    mask    TEXT
);

CREATE TABLE Machines
(
    machine_pk INTEGER PRIMARY KEY,
    mac TEXT,
    machine_confidence INTEGER DEFAULT 100,
    router_confidence INTEGER DEFAULT 0
);

CREATE TABLE Traits
(
    traits_pk INTEGER PRIMARY KEY,
    os  TEXT,
    machine_fk INTEGER,
    FOREIGN KEY(machine_fk) REFERENCES Machines(machine_pk)
);

CREATE TABLE Services
(
    service_pk  INTEGER PRIMARY KEY,
    packet_fk INTEGER,
    req_res_flag INTEGER,
    service TEXT
);

CREATE TABLE Hosts
(
    host_pk INTEGER PRIMARY KEY,
    host    TEXT UNIQUE
);

CREATE TABLE User_Agents
(
    user_agent_pk INTEGER PRIMARY KEY,
    user_agent TEXT UNIQUE
);

CREATE TABLE Servers
(
    server_pk INTEGER PRIMARY KEY,
    server TEXT UNIQUE
);

CREATE TABLE Packets
(
    packet_pk INTEGER PRIMARY KEY,
    source_ip_fk INTEGER,
    dest_ip_fk INTEGER,
    source_mac_fk INTEGER,
    dest_mac_fk INTEGER,
    source_port INTEGER,
    dest_port INTEGER,
    packet_type_fk  INTEGER,
    host_fk INTEGER,
    user_agent_fk INTEGER,
    server_fk   INTEGER,
    protocol    TEXT,
    FOREIGN KEY(source_ip_fk) REFERENCES IPs(ip_pk),
    FOREIGN KEY(dest_ip_fk) REFERENCES IPs(ip_pk),
    FOREIGN KEY(source_mac_fk) REFERENCES Macs(mac_pk),
    FOREIGN KEY(dest_mac_fk) REFERENCES Macs(mac_pk),
    FOREIGN KEY(packet_type_fk) REFERENCES Packet_Types(packet_type_pk),
    FOREIGN KEY(host_fk) REFERENCES Hosts(host_pk),
    FOREIGN KEY(user_agent_fk) REFERENCES User_Agents(user_agent_pk),
    FOREIGN KEY(server_fk) REFERENCES Servers(server_pk)
);

CREATE TABLE Network_ID
(
    network_id_pk INTEGER PRIMARY KEY,
    network_fk INTEGER,
    id TEXT,
    name TEXT,
    FOREIGN KEY(network_fk) REFERENCES Networks(network_pk)
);

CREATE TABLE SDI_Machines
(
    sdi_machine_pk INTEGER PRIMARY KEY,
    machine_fk  INTEGER,
    machine_id  TEXT,
    name    TEXT,
    FOREIGN KEY(machine_fk) REFERENCES Machines(machine_pk)
);

CREATE TABLE SDI_Interfaces
(
    sdi_interface_pk    INTEGER PRIMARY KEY,
    sdi_machine_fk  INTEGER,
    ip_fk INTEGER,
    interface_id    TEXT,
    FOREIGN KEY(ip_fk) REFERENCES IPs(ip_pk),
    FOREIGN KEY(sdi_machine_fk) REFERENCES SDI_Machines(sdi_machine_pk)
);

CREATE TABLE Packet_Types
(
    packet_type_pk  INTEGER PRIMARY KEY,
    type    TEXT
);

INSERT INTO Packet_Types(type)
VALUES('IP');

INSERT INTO Packet_Types(type)
VALUES('DHCP');
