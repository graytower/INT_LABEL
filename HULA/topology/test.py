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
                    type=str, action="store", default="/home/poi/Desktop/P4_INT_Ver2/p4_source_code/basic.json")
parser.add_argument('--nodes-list', help='The scale of the topology',
                    nargs='*', default=[0,1,2])
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)
args = parser.parse_args()


class clos(Topo):

    def __init__(self, behavioral_exe, thrift_port, json, nodes_list, pcap_dump, **opts):

        Topo.__init__(self, **opts)

        self.sw_list = []
        self.h_list = []
        layer_num = len(nodes_list)-1   # layer number of switches

        # Create switches
        for i in xrange(layer_num):
            sw_list_single_layer = []
            for j in xrange(nodes_list[i]):
                sw = self.addSwitch('l%d_%d' % (i+1, j + 1),
                                    sw_path=behavioral_exe,
                                    json_path=json,
                                    thrift_port=thrift_port,
                                    pcap_dump=pcap_dump)
                thrift_port = thrift_port + 1
                sw_list_single_layer.append(sw)
            self.sw_list.append(sw_list_single_layer)

        # Create links between switches
        for i in xrange(layer_num-1):
            for j in self.sw_list[i]:
                for k in self.sw_list[i+1]:
                    self.addLink(j, k)

        # Create hosts
        for i in xrange(nodes_list[-2]*nodes_list[-1]):
            h = self.addHost('h%d' % (i + 1))
            self.h_list.append(h)

        # Create links between switches and hosts
        h_index = 0
        for i in self.sw_list[-1]:
            for j in xrange(nodes_list[-1]):
                self.addLink(i, self.h_list[h_index])
                h_index += 1


def main():

    nodes_list = map(int, args.nodes_list)
    print(nodes_list)
    topo = clos(args.behavioral_exe,
                args.thrift_port,
                args.json,
                nodes_list,
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
