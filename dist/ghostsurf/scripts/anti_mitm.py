#!/usr/bin/python3

from os import system
from scapy.all import Ether, ARP, srp, sniff, conf

def get_mac(ip):
    """A which takes an IP address as an argument. It creates an Ethernet packet with the destination MAC address set to the broadcast address (ff:ff:ff:ff:ff:ff) and an ARP packet with the specified IP address as the source IP. It then sends the packet using srp (send and receive packet) and captures the response. Finally, it returns the MAC address (hwsrc) from the first received response."""
    
    # Creating an ethernet packet and an arp package
    p = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip)

    # Sending the packet and capturing the result
    result = srp(p, timeout=3, verbose=False)[0]

    # Returning the result
    return result[0][1].hwsrc


def process(packet):
    """A function which takes a packet as an argument. It is called for each packet captured by the sniff function. Inside the function, it checks if the packet has an ARP layer. If it does, it further checks if the operation code (op) of the ARP packet is 2, which indicates an ARP reply. If it is an ARP reply, it tries to get the real MAC address of the packet's source IP using the get_mac function. It also extracts the MAC address from the packet itself. If the real MAC address and the response MAC address are different, it executes a system command to block the MAC address using iptables (a Linux command for managing firewall rules)."""

    # Checking if the package has a ARP layer
    if packet.haslayer(ARP):

        # Checking if the operation code of this layer is equal to 2
        if packet[ARP].op == 2:

            # Trying to executing the code inside the try block without error
            try:                

                # Getting the real MAC address of the packet's source IP using the get_mac function.
                real_mac = get_mac(packet[ARP].psrc)

                # Extracting the MAC address from the packet itself
                response_mac = packet[ARP].hwsrc

                # Checking if the real MAC address and the response MAC address are different
                if real_mac != response_mac:
                    
                    # Executing a system command to block the MAC address using iptables
                    system("iptables -A INPUT -m mac --mac-source " + response_mac + " -j DROP")

            # Handling IndexError
            except IndexError:
                
                # Skipping without doing anything
                pass


sniff(store=False, prn=process)