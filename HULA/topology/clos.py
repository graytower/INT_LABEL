from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from p4_mininet import P4Switch, P4Host

import redis
import argparse
import time
import os


BW=100
MAX_Q_Size=5 #MAX queue size of switch

os.system("sudo mn -c")

parser = argparse.ArgumentParser(description='CLOS architecture topology')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", default="/home/fnl/P4/behavioral-model/targets/simple_switch/simple_switch")
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", default="../p4_source_code/my_int.json")
parser.add_argument('--nodes-list', help='Number of spine, leaf, tor, host, pod',
                    nargs='*', default=[2,2,2,2,2])
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)
args = parser.parse_args()


class clos(Topo):

    def __init__(self, behavioral_exe, thrift_port, json, nodes_list, pcap_dump, **opts):

        Topo.__init__(self, **opts)

        spine_num = nodes_list[0]
        set_num = nodes_list[1]
        leaf_num = nodes_list[1]
        tor_num = nodes_list[2]
        h_num = nodes_list[3]
        pod_num = nodes_list[4]

        self.spine_sw_list = []
        self.leaf_sw_list = []
        self.tor_sw_list = []
        self.h_list = []

        device_id=0
        for i in xrange(set_num):
            self.spine_sw_list.append([])
            for j in xrange(spine_num):
                sw = self.addSwitch('s%d_s%d' % (i + 1, j + 1),
                                    sw_path=behavioral_exe,
                                    json_path=json,
                                    thrift_port=thrift_port,
                                    nanolog="ipc:///tmp/bm-%d-log.ipc"%device_id,
                                    device_id=device_id,
                                    pcap_dump=pcap_dump)
                self.spine_sw_list[i].append(sw)
                thrift_port+= 1
                device_id+=1

        for i in xrange(pod_num):
            self.leaf_sw_list.append([])
            for j in xrange(leaf_num):
                sw = self.addSwitch('p%d_l%d' % (i + 1, j + 1),
                                    sw_path=behavioral_exe,
                                    json_path=json,
                                    thrift_port=thrift_port,
                                    nanolog="ipc:///tmp/bm-%d-log.ipc"%device_id,
                                    device_id=device_id,
                                    pcap_dump=pcap_dump)
                self.leaf_sw_list[i].append(sw)
                thrift_port = thrift_port + 1
                device_id+=1

        for i in xrange(pod_num):
            self.tor_sw_list.append([])
            for j in xrange(tor_num):
                sw = self.addSwitch('p%d_t%d' % (i + 1, j + 1),
                                    sw_path=behavioral_exe,
                                    json_path=json,
                                    thrift_port=thrift_port,
                                    nanolog="ipc:///tmp/bm-%d-log.ipc"%device_id,
                                    device_id=device_id,
                                    pcap_dump=pcap_dump)
                self.tor_sw_list[i].append(sw)
                thrift_port = thrift_port + 1
                device_id+=1

        for i in xrange(pod_num):
            self.h_list.append([])
            for j in xrange(tor_num):
                self.h_list[i].append([])
                for k in xrange(h_num):
                    h = self.addHost('p%d_t%d_%d' % (i + 1, j + 1,k+1),ip="10.%d.%d.%d"%(i+1,j+1,k+1),mac="00:00:00:%s:%s:%s" % (hex(i+1)[2:],hex(j+1)[2:],hex(k+1)[2:]))
                    self.h_list[i][j].append(h)

        for i in xrange(set_num):
            for j in xrange(spine_num):
                for k in xrange(pod_num):
                    self.addLink(self.spine_sw_list[i][j], self.leaf_sw_list[k][i],max_queue_size=MAX_Q_Size,bw=BW)

        for i in xrange(pod_num):
            for j in xrange(leaf_num):
                for k in xrange(tor_num):
                    self.addLink(self.leaf_sw_list[i][j], self.tor_sw_list[i][k],max_queue_size=MAX_Q_Size,bw=BW)

        for i in xrange(pod_num):
            for j in xrange(tor_num):
                for k in xrange(h_num):
                    self.addLink(self.h_list[i][j][k], self.tor_sw_list[i][j])


def main():
    os.system('sh ../p4_source_code/run.sh')

    r4 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=3) # data database
    r4.flushall()
    
    r4.set('send',0)
    r4.set('receive',0)

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
                  controller=None,
                  link=TCLink)

    net.start()

    os.system("sh ../flow_table/command.sh")


    for i in xrange(nodes_list[4]):
        for j in xrange(nodes_list[2]):
            for k in xrange(nodes_list[3]):
                h=net.get(topo.h_list[i][j][k])
                h.cmd("python ../packet/receive/receive.py >/dev/null &")


    for i in xrange(nodes_list[4]):
        for j in xrange(nodes_list[2]):
            for k in xrange(nodes_list[3]):
                h=net.get(topo.h_list[i][j][k])
                #h.cmd("python /home/poi/Desktop/P4_INT_Ver4/packet/receive/receive.py >/dev/null &")
                h.cmd("python ../packet/send/send_int_probe.py >/dev/null &")
    #            h.cmd("python /home/poi/Desktop/P4_INT_Ver4/controller/host.py >/dev/null &")


    for i in xrange(nodes_list[4]):
        for j in xrange(nodes_list[2]):
            for k in xrange(nodes_list[3]):
                h=net.get(topo.h_list[i][j][k])
                for ii in xrange(5):
                    h.cmd("python ../packet/send/send_data.py >/dev/null &")


    # time.sleep(10)

    # for h_name in topo.h_list:
    #     h = net.get(h_name)
    #     h.cmd("python /home/poi/Desktop/P4_INT_Ver2/packet/send/send_udp.py >/dev/null &")

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
