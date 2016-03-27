#!/usr/bin/env python

"""
Determine a host's IP address given its MAC address and an IP address
range to scan for it.

I created this to discover a WLAN printer (which dynamically gets an IP
address assigned via DHCP) on the local network.

Calls Nmap_ to ping hosts and return their MAC addresses (requires root
privileges).

Requires Python_ 2.7+ or 3.3+.

.. _Nmap: http://nmap.org/
.. _Python: http://python.org/

:Copyright: 2014 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 05-Jul-2014 (original release: 25-Jan-2014)
:License: MIT
"""

try:
    from future_builtins import filter
except ImportError:
    pass  # Neither available nor necessary on Python 3.
import subprocess
import xml.etree.ElementTree as ET


def scan_for_hosts(ip_range):
    """Scan the given IP address range using Nmap and return the result
    in XML format.
    """
    nmap_args = ['nmap', '-n', '-sP', '-oX', '-', ip_range]
    return subprocess.check_output(nmap_args)


def find_ip_address_for_mac_address(xml, mac_address):
    """Parse Nmap's XML output, find the host element with the given
    MAC address, and return that host's IP address.
    """
    host_elems = ET.fromstring(xml).iter('host')
    host_elem = find_host_with_mac_address(host_elems, mac_address)
    return get_ip_address(host_elem)


def find_host_with_mac_address(host_elems, mac_address):
    """Return the first host element that contains the MAC address."""
    for host_elem in host_elems:
        if host_has_mac_address(host_elem, mac_address):
            return host_elem


def host_has_mac_address(host_elem, mac_address):
    """Return true if the host has the given MAC address."""
    mac_address_found = get_address_of_type(host_elem, 'mac')
    return mac_address_found.lower() == mac_address.lower()


def get_ip_address(host_elem):
    """Return the host's IP address."""
    return get_address_of_type(host_elem, 'ipv4')


def get_address_of_type(host_elem, type_):
    """Return the host's address of the given type, or `None` if there
    is no address element of that type.
    """
    address_elem = host_elem.find('./address[@addrtype="{}"]'.format(type_))
    if address_elem is not None:
        return address_elem.get('addr')


if __name__ == '__main__':
    mac_address = '00:33:66:99:cc:ff'
    ip_range = '192.168.1.1-255'

    xml = scan_for_hosts(ip_range)
    ip_address = find_ip_address_for_mac_address(xml, mac_address)

    print('Found IP address {} for MAC address {}.'
          .format(ip_address, mac_address))
