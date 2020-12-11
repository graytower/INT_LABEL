from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
from p4_mininet import P4Switch, P4Host

import argparse
import time
import os
import redis

os.system("sudo mn -c")

parser = argparse.ArgumentParser(description='CLOS architecture topology')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", default="/home/ng/behavioral-model/targets/simple_switch/simple_switch")
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", default="../p4_source_code/my_int.json")
parser.add_argument('--nodes-list', help='Number of spine, leaf, tor, host, pod',
                    nargs='*', default=[2, 2, 2, 2, 2])
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)
args = parser.parse_args()

TIME_OUT=2*10 #2*20ms
Loss=0 # %
BW=1000
MAX_Q_SIZE=100

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

        device_id = 0
        for i in xrange(set_num):
            self.spine_sw_list.append([])
            for j in xrange(spine_num):
                sw = self.addSwitch('s%d_s%d' % (i + 1, j + 1),
                                    sw_path=behavioral_exe,
                                    json_path=json,
                                    thrift_port=thrift_port,
                                    nanolog="ipc:///tmp/bm-%d-log.ipc" % device_id,
                                    device_id=device_id,
                                    pcap_dump=pcap_dump)
                self.spine_sw_list[i].append(sw)
                thrift_port += 1
                device_id += 1

        for i in xrange(pod_num):
            self.leaf_sw_list.append([])
            for j in xrange(leaf_num):
                sw = self.addSwitch('p%d_l%d' % (i + 1, j + 1),
                                    sw_path=behavioral_exe,
                                    json_path=json,
                                    thrift_port=thrift_port,
                                    nanolog="ipc:///tmp/bm-%d-log.ipc" % device_id,
                                    device_id=device_id,
                                    pcap_dump=pcap_dump)
                self.leaf_sw_list[i].append(sw)
                thrift_port = thrift_port + 1
                device_id += 1

        for i in xrange(pod_num):
            self.tor_sw_list.append([])
            for j in xrange(tor_num):
                sw = self.addSwitch('p%d_t%d' % (i + 1, j + 1),
                                    sw_path=behavioral_exe,
                                    json_path=json,
                                    thrift_port=thrift_port,
                                    nanolog="ipc:///tmp/bm-%d-log.ipc" % device_id,
                                    device_id=device_id,
                                    pcap_dump=pcap_dump)
                self.tor_sw_list[i].append(sw)
                thrift_port = thrift_port + 1
                device_id += 1

        for i in xrange(pod_num):
            self.h_list.append([])
            for j in xrange(tor_num):
                self.h_list[i].append([])
                for k in xrange(h_num):
                    h = self.addHost('p%d_t%d_%d' % (
                        i + 1, j + 1, k+1), ip="10.%d.%d.%d" % (i+1, j+1, k+1), mac="00:00:00:%s:%s:%s" % (hex(i+1)[2:],hex(j+1)[2:],hex(k+1)[2:]))
                    self.h_list[i][j].append(h)

        for i in xrange(set_num):
            for j in xrange(spine_num):
                for k in xrange(pod_num):
                    self.addLink(
                        self.spine_sw_list[i][j], self.leaf_sw_list[k][i],loss=Loss,bw=BW,max_queue_size=MAX_Q_SIZE)

        for i in xrange(pod_num):
            for j in xrange(leaf_num):
                for k in xrange(tor_num):
                    self.addLink(
                        self.leaf_sw_list[i][j], self.tor_sw_list[i][k],loss=Loss,bw=BW,max_queue_size=MAX_Q_SIZE)

        for i in xrange(pod_num):
            for j in xrange(tor_num):
                for k in xrange(h_num):
                    self.addLink(self.h_list[i][j][k], self.tor_sw_list[i][j])


def database_init(r,r2,r4,nodes_list=[2,2,2,2,2]):
    r2.flushall()
    
    r4.set('send',0) # num of sending (data packet)
    r4.set('receive',0) # num of receiving (data packet)
    r4.set('int',0) # num of packet with int info
    r4.set('all',0) # num of int info
    r4.set('extra',0) # num of redundancy probing
    r4.set('0',0) # num of packets with 0 INT info 
    r4.set('1',0) # num of packets with 1 INT info 
    r4.set('2',0) # num of packets with INT info 
    r4.set('3',0) # num of packets with INT info 
    r4.set('4',0) # num of packets with INT info 
    r4.set('5',0) # num of packets with INT info 
    
    spine_num = nodes_list[0]
    set_num = nodes_list[1]
    leaf_num = nodes_list[1]
    tor_num = nodes_list[2]
    h_num = nodes_list[3]
    pod_num = nodes_list[4]
    
    d={}
    t=0
    keys=[]
    for i in range(set_num*spine_num):
        d[str(t)]=pod_num
        t+=1
    
    for i in range(pod_num*leaf_num):
        d[str(t)]=spine_num+tor_num
        t+=1
    
    for i in range(pod_num*tor_num):
        d[str(t)]=leaf_num+h_num
        t+=1

    for k,v in d.items():
        for i in range(v):
            keys.append(k+'-'+str(i+1))
    
    for key in keys:
        r2.lpush(key,-1,-1)
        r.lpush(key,-1,-1)
        r.pexpire(key,TIME_OUT)



def main():
    os.system('sh ../p4_source_code/run.sh')
    
    r = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390)       # aging database
    r2 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=1) # persist database
    r4 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=3) # data database
    # database_init(r,r2,r4)
    # os.system('python ../controller/coverage.py >/dev/null &')    #calculate the coverage
    
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

    database_init(r,r2,r4)

    for i in xrange(nodes_list[4]):
        for j in xrange(nodes_list[2]):
            for k in xrange(nodes_list[3]):
                h=net.get(topo.h_list[i][j][k])
                h.cmd("python ../packet/receive/receive.py >/dev/null &")

    for i in xrange(nodes_list[4]):
        for j in xrange(nodes_list[2]):
            for k in xrange(nodes_list[3]):
                h=net.get(topo.h_list[i][j][k])
                for ii in xrange(20):
                    h.cmd("python ../packet/send/send_int_probe.py >/dev/null &")
    


    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
