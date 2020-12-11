from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from p4_mininet import P4Switch, P4Host

import argparse
import threading
import time
import os

os.system("sudo mn -c")

parser = argparse.ArgumentParser(description='Mininet demo')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", default="/home/poi/Desktop/P4_INT_Ver2/bmv2_model/simple_switch")
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", default="/home/poi/Desktop/P4_INT_Ver2/p4_source_code/basic.json")
parser.add_argument('--c_sw_num', help='The number of core switches',
                    type=int, action="store", default=0)
parser.add_argument('--t_sw_num', help='The number of tor switches',
                    type=int, action="store", default=1)
parser.add_argument('--h_num', help='The number of hosts linked with each tor switch',
                    type=int, action="store", default=2)
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)

args = parser.parse_args()

c_sw_list = []
t_sw_list = []
h_list = []
h_ip_list = []
h_mac_list = []


class ToR(Topo):

    def __init__(self, sw_path, thrift_port, json_path, c_sw_num, t_sw_num, h_num, pcap_dump, **opts):

        Topo.__init__(self, **opts)

        for c_sw_no in xrange(c_sw_num):
            c_sw = self.addSwitch('c_sw%d' % (c_sw_no + 1),
                                  sw_path=sw_path,
                                  json_path=json_path,
                                  thrift_port=thrift_port + c_sw_no,
                                  pcap_dump=pcap_dump)
            c_sw_list.append(c_sw)

        for t_sw_no in xrange(t_sw_num):
            t_sw = self.addSwitch('t_sw%d' % (t_sw_no + 1),
                                  sw_path=sw_path,
                                  json_path=json_path,
                                  thrift_port=thrift_port + c_sw_num + t_sw_no,
                                  pcap_dump=pcap_dump)
            t_sw_list.append(t_sw)

            for c_sw in c_sw_list:
                self.addLink(c_sw, t_sw)

            for h_no in xrange(h_num):
                h = self.addHost('h%d' % (h_num * t_sw_no + h_no + 1),
                                 ip="10.0.0.%d/24" % (h_num *
                                                      t_sw_no + h_no + 1),
                                 mac='00:04:00:00:00:%02x' % (h_num * t_sw_no + h_no + 1))
                h_list.append(h)
                h_ip_list.append("10.0.0.%d" % (h_num * t_sw_no + h_no + 1))
                h_mac_list.append('00:04:00:00:00:%02x' %
                                  (h_num * t_sw_no + h_no + 1))
                self.addLink(t_sw, h)


def main():

    c_sw_num = args.c_sw_num
    t_sw_num = args.t_sw_num
    h_num = args.h_num

    topo = ToR(args.behavioral_exe,
               args.thrift_port,
               args.json,
               c_sw_num,
               t_sw_num,
               h_num,
               args.pcap_dump)
    net = Mininet(topo=topo,
                  host=P4Host,
                  switch=P4Switch,
                  controller=None)

    net.start()

    #os.system("sh /home/poi/Desktop/P4_INT/int_test/topology/command.sh")

    for h_no in xrange(t_sw_num * h_num):
        h = net.get(h_list[h_no])
        h.describe()
        h.setDefaultRoute("dev eth0")
        for i in [x for x in xrange(t_sw_num * h_num) if x != h_no]:
            h.setARP(h_ip_list[i], h_mac_list[i])
            # print("ARP TABLE")
            # print(h_ip_list[i], h_mac_list[i])
        # h.cmd("sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        # h.cmd("sysctl -w net.ipv6.conf.default.disable_ipv6=1")
        # h.cmd("sysctl -w net.ipv6.conf.lo.disable_ipv6=1")
        # h.cmd("python /home/poi/Desktop/P4_INT/int_test/pkt/receiver.py >/dev/null &")
        # h.cmd("python /home/poi/Desktop/P4_INT/int_test/pkt/send_int_probe.py >/dev/null &")
    
    # for h_no in xrange(t_sw_num * h_num):
    #     h = net.get(h_list[h_no])
    #     h.cmd("python /home/poi/Desktop/P4_INT/int_test/pkt/send_int_probe.py >/dev/null &")

    print "INT Ready!"

    # for h_no in xrange(t_sw_num * h_num):
    #     h = net.get(h_list[h_no])
    #     h.cmd("python /home/poi/Desktop/P4_INT/int_test/pkt/pkt.py >/dev/null &")
    
    # print "Sending UDP packets......"

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
