#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct
import redis
import random

from scapy.all import sendp, send, get_if_list, get_if_hwaddr,get_if_addr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break
    if not iface:
        print "Cannot find eth0 interface"
        exit(1)
    return iface

def get_route(route_info):
    route_info=route_info.split("+")
    dstip=route_info[1]
    dstmac=route_info[2]
    port_list=route_info[3:]
    sr=""
    for i in range(len(port_list)-1):
        if i%2!=0:
            sr+=struct.pack("!H",int(port_list[i].split("-")[1]))
    sr+=struct.pack("!H",(1<<15)+int(port_list[-1].split("-")[1]))

    return dstip,dstmac,sr

def main():
    src_ip = get_if_addr("eth0")
    r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')
    fmt=src_ip+"*"
    key=r.keys(fmt)
    dst_ip_list=[]
    for i in key:
        dst_ip_list.append((str.split(i,"+"))[1])
    dst_ip_list=set(dst_ip_list)
    dst_ip=random.sample(dst_ip_list,1)
    fmt=src_ip+"+"+dst_ip[0]+"*"
    key=r.keys(fmt)
    route_info=random.sample(key,1)

    dst_ip,dst_mac,sr=get_route(route_info[0])

    iface = get_if()

    pkt =  Ether(src=get_if_hwaddr(iface), dst=dst_mac, type=1792)
    pkt = pkt / sr / '\x08\x00' / IP(dst=dst_ip) / UDP(dport=1234, sport=random.randint(49152,65535)) / "777777777"
    pkt.show2()
    sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    while(True):
        main()
