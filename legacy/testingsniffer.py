import packetparser
from scapy.all import *


def handler(pkt):
	logic = packetparser.ParseFilter("IS ICMP OR IS ARP OR dport == 80")
	print packetparser.FilterCheck(logic[0], pkt)

sniff(prn=handler, store=0)
