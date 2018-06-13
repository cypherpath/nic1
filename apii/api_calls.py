import enum

class Method(enum.Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"

class Call:
    def __init__(self, path: str, method: Method, *args: str) -> None:
        self.path = path
        self.method = method
        self.args = args

CALLS = {
    "get_users":                Call("accounts/users", Method.GET),
    "get_sdis":                 Call("sdis/{user_pk}", Method.GET),
    "create_sdi":               Call("sdis/{user_pk}", Method.POST, "name", "description"),
    "edit_sdi":                 Call("sdis/{sdi_id}", Method.PUT, "user", "name", "description"),
    "run_sdi":                  Call("sdis/{sdi_id}/start", Method.POST),
    "configure_sdi":            Call("sdis/{sdi_id}/settings", Method.PUT, "start_machines", "default_persistence",
                                     "max_run_time", "default_routing", "datetime", "default_oui", "snap_to_grid"),
    "get_machines":             Call("sdis/{sdi_id}/machines", Method.GET),
    "create_machine":           Call("sdis/{sdi_id}/machines", Method.POST, "name", "description", "memory",
                                     "sockets", "cores", "threads", "boot_priority", "role", "image_persist", "datetime",
                                     "boot_device", "boot_menu", "CPU_type", "video_card"),
    "edit_machine":             Call("sdis/{sdi_id}/machines/{machine_id}", Method.PUT, "name", "description", "memory",
                                     "sockets", "cores", "threads", "boot_priority", "role", "image_persist", "datetime",
                                     "boot_device", "boot_menu", "CPU_type", "video_card"),
    "get_machine_interfaces":   Call("sdis/{sdi_id}/machines/{machine_id}/interfaces", Method.GET),
    "create_machine_interface": Call("sdis/{sdi_id}/machines/{machine_id}/interfaces", Method.POST, "network",
                                     "nic", "mac", "hostname", "vlan_mode", "vlan_pvid"),
    "edit_machine_interface":   Call("sdis/{sdi_id}/machines/{machine_id}/interfaces/{interface_id}",
                                     Method.PUT, "network", "nic", "mac", "hostname", "vlan_mode", "vlan_pvid"),
    "delete_machine_interface": Call("sdis/{sdi_id}/machines/{machine_id}/interfaces/{interface_id}", Method.DELETE),
    "add_machine_vlan":         Call("sdis/{sdi_id}/machines/{machine_id}/interfaces/{interface_id}/vlans",
                                     Method.POST, "vlan", "ip", "ipv6"),
    "edit_machine_vlan":        Call("sdis/{sdi_id}/machines/{machine_id}/interfaces/{interface_id}/vlans/{vlan_id}",
                                     Method.PUT, "ip", "ipv6"),
    "delete_machine_vlan":      Call("sdis/{sdi_id}/machines/{machine_id}/interfaces/{interface_id}/vlans/{vlan_id}",
                                     Method.DELETE),
    "get_drives":               Call("sdis/{sdi_id}/machines/{machine_id}/drives", Method.GET),
    "attach_drive":             Call("sdis/{sdi_id}/machines/{machine_id}/drives", Method.POST, "master_id", "bus"),
    "edit_disk":                Call("sdis/{sdi_id}/machines/{machine_id}/drives/{disk_slot}", Method.PUT, "master_id", "bus"),
    "remove_disk":              Call("sdis/{sdi_id}/machines/{machine_id}/drives/{disk_slot}", Method.DELETE),
    "reorder_drives":           Call("sdis/{sdi_id}/machines/{machine_id}/drives/order", Method.PUT, "order"),
    "get_networks":             Call("sdis/{sdi_id}/networks", Method.GET),
    "create_network":           Call("sdis/{sdi_id}/networks", Method.POST, "name", "mode", "link", "services"),
    "edit_network":             Call("sdis/{sdi_id}/networks/{network_id}", Method.PUT,
                                     "name", "description", "mode", "link", "services"),
    "get_services":             Call("sdis/{sdi_id}/networks/{network_id}/services", Method.GET),
    "add_service":              Call("sdis/{sdi_id}/networks/{network_id}/services", Method.POST, "vid"),
    "edit_service":             Call("sdis/{sdi_id}/networks/{network_id}/services/{vid}", Method.PUT, "vid", "ip", "netmask",
                                     "dhcp", "dns", "defaultgateway", "ipv6", "slaac", "defaultgatewayv6"),
    "delete_service":           Call("sdis/{sdi_id}/networks/{network_id}/services/{vid}", Method.DELETE)
}
