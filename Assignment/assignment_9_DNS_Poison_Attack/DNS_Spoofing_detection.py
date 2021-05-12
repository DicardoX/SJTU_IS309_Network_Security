# DNS_Spoofing_detection.py

from optparse import OptionParser
from scapy.layers.dns import DNSQR, DNS, IP, UDP, DNSRR
from scapy.all import sniff


# DNS Spoofing detector
def detector(pkt):
    if pkt.haslayer(IP) and pkt.haslayer(DNS) and pkt[DNS].qr == 1:
        if pkt[DNS] == 0 or pkt[DNS].qd is None:
            return
        if pkt[DNS].id in captured and (
                pkt[DNS].qd.qname.rstrip('.') == captured[pkt[DNS].id][DNS].qd.qname.rstrip('.')):
            l1 = []
            l2 = []
            old_pkt = captured[pkt[DNS].id]
            for i in range(pkt['DNS'].ancount):
                dnsrr = pkt['DNS'].an[i]
                if dnsrr.type == 1:
                    l1.append(dnsrr.rdata)

            for i in range(old_pkt['DNS'].ancount):
                dnsrr = old_pkt['DNS'].an[i]
                if dnsrr.type == 1:
                    l2.append(dnsrr.rdata)

            l1 = sorted(l1)
            l2 = sorted(l2)
            if l1 != l2:
                print("")
                print("---------------------------------------------------------------------------------")
                print("DNS Poison Attack Detected!")
                print("TXID %s Request %s" % (pkt[DNS].id, pkt[DNS].qd.qname.rstrip('.')))
                print("Response packet 1:", l1)
                print("Response packet 2:", l2)
                print("---------------------------------------------------------------------------------")
                print("")
        else:
            captured[pkt[DNS].id] = pkt


if __name__ == '__main__':
    captured = {}
    parser = OptionParser()
    parser.set_conflict_handler("resolve")
    parser.add_option('-i', dest="interface")
    parser.add_option('-r', dest="spoofedPacketsFile")
    (options, remainder) = parser.parse_args()
    expression = remainder

    if len(expression) > 0:
        exp = expression[0]
    else:
        exp = ""

    print(" ")
    print("################################################################################")
    print("#                  Begin Detecting for DNS Poison Attack                       #")
    print("################################################################################")
    print(" ")

    if options.spoofedPacketsFile is not None:
        sniff(filter=exp, prn=detector, store=0, offline=options.spoofedPacketsFile)
    else:
        sniff(filter=exp, prn=detector, store=0, iface=options.interface)

