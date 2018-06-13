"""nic1 Settings"""

# Current NIC1 version
VERSION = "0.5"

# Domain of the SDI OS server
# Example "172.16.1.12" or "www.mydomain.com"
SDIOS_DOMAIN = "www.mydomain.com"

# SDI OS API version
# Can also be set to None to use the most current version number by not
# setting the Accept header.
SDIOS_API_VERSION = None

# Flag whether to verify the ssl certificate (default should be true).
# This requires SDI OS setup with a signed certificate otherwise you can use
# False to skip verification during development
SDIOS_VERIFY_SSL = False

### SDI OS Super user API credentials
SDIOS_CREDS = {
    "username": "",
    "password": "",
    "client_id": "",
    "client_secret": ""
}
