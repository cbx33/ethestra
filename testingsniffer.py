import parsercomplete2
from scapy.all import *


def handler(pkt):
	logic = parsercomplete2.ParseFilter("IS ICMP OR IS ARP OR dport == 80")
	print parsercomplete2.FilterCheck(logic[0], pkt)

sniff(prn=handler, store=0)
