from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from p4_mininet import P4Switch, P4Host

import argparse
import time
import os

os.system("sudo mn -c")

parser = argparse.ArgumentParser(description='CLOS architecture topology')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", default="/home/poi/Desktop/P4_INT_Ver2/bmv2_model/simple_switch")
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", default="/home/poi/Desktop/P4_INT_Ver2/p4_source_code/my_int.json")
parser.add_argument('--nodes-list', help='The scale of the topology',
                    nargs='*', default=[3, 3, 4])
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)
args = parser.parse_args()


class clos(Topo):

    def __init__(self, behavioral_exe, thrift_port, json, pcap_dump, **opts):

        Topo.__init__(self, **opts)

        h0 = self.addHost("h0")
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        h1.
        s1 = self.addSwitch('s1',
                            sw_path=behavioral_exe,
                            json_path=json,
                            thrift_port=9090,
                            pcap_dump=pcap_dump)
        s2 = self.addSwitch('s2',
                            sw_path=behavioral_exe,
                            json_path=json,
                            thrift_port=9091,
                            pcap_dump=pcap_dump)
        s3 = self.addSwitch('s3',
                            sw_path=behavioral_exe,
                            json_path=json,
                            thrift_port=9092,
                            pcap_dump=pcap_dump)

        self.addLink(s1, h0)
        self.addLink(s1, h1)
        self.addLink(s1, s2)
        self.addLink(s2, h2)
        self.addLink(s2, s3)
        self.addLink(s2, h0)
        self.addLink(s3, h3)
        self.addLink(s3, h0)

        self.h_list = [h0, h1, h2, h3]


def main():

    topo = clos(args.behavioral_exe,
                args.thrift_port,
                args.json,
                args.pcap_dump)
    net = Mininet(topo=topo,
                  host=P4Host,
                  switch=P4Switch,
                  controller=None)

    net.start()

    for h_name in topo.h_list:
        h = net.get(h_name)
        h.describe()
        h.setDefaultRoute("dev eth0")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
