from typing import Optional, Tuple

import ipaddress

class Classes:
    """
    name: Classes
    responsibility: This class will apply classful masking to an ip and return
                    the network. It is an rudametary way to get a network.

    """

    def __init__(self) -> None:
        self.__class_a_threshold = 2147483647
        self.__class_b_threshold = 3221225471
        self.__class_c_threshold = 3758096383
        self.__class_a_mask = 4278190080
        self.__class_b_mask = 4294901760
        self.__class_c_mask = 4294967040
        self.__default_ip_mask = int(ipaddress.ip_address("0.0.0.0"))

    
    def mask_ip_address(self, ipaddr: str, mask: int) -> int:
        """
        name: mask_ip_address
        purpose: Masks an ip address with the given mask value
        """
        ip_integer = int(ipaddress.ip_address(ipaddr))
        return ip_integer & mask

    
    def get_network(self, ipaddr: str) -> Optional[str]:
        """
        name: get_network
        purpose: Returns the network for a given ip
        """
        masked_ip, _mask_used = self.get_network_with_mask_used(ipaddr)
        return masked_ip


    def get_network_with_mask_used(self, ipaddr: str) -> Tuple[Optional[str], Optional[str]]:
        """
        name: get_network_with_mask_used
        purpose: Returns the network for a given ip,
                 along with the mask used
        """
        ip_integer = int(ipaddress.ip_address(ipaddr))

        if ip_integer < 0 or ip_integer > self.__class_c_threshold:
            return None, None

        # These defaults will be used if the given ipaddr
        # is exactly the value of the class c threshold
        masked_ip = ip_integer
        mask_used = self.__default_ip_mask

        if ip_integer < self.__class_a_threshold:
            masked_ip = ip_integer & self.__class_a_mask
            mask_used = self.__class_a_mask
        elif ip_integer < self.__class_b_threshold:
            masked_ip = ip_integer & self.__class_b_mask
            mask_used = self.__class_b_mask
        elif ip_integer < self.__class_c_threshold:
            masked_ip = ip_integer & self.__class_c_mask
            mask_used = self.__class_c_mask

        # Return the now-masked IP and the mask that was used
        return str(ipaddress.ip_address(masked_ip)), str(ipaddress.ip_address(mask_used))
