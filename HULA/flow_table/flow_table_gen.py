import os

class flow_table():
    def flow_table_gen(self, nodes_list):

        spine_num = nodes_list[0]
        set_num = nodes_list[1]
        leaf_num = nodes_list[1]
        tor_num = nodes_list[2]
        h_num = nodes_list[3]
        pod_num = nodes_list[4]

        thrift_port = 9090

        with open("../flow_table/command.sh", "w") as f:
            f.write("")

        # spine
        for i in xrange(set_num):
            for j in xrange(spine_num):
                with open("../flow_table/flow_table/s%d_s%d.txt" % (i+1, j+1), "w") as f:
                    for k in xrange(pod_num):
                        f.write(
                            "table_add mcast_table do_mcast %d => %d\n" % (k+1, k+1))
                        f.write("mc_mgrp_create %d\n" % (k+1))

                        mcast_list = [n+1 for n in xrange(pod_num)]
                        mcast_list.remove(k+1)
                        mcast_list = tuple(mcast_list)
                        f.write("mc_node_create %d" % (k))
                        for m in mcast_list:
                            f.write(" %d" % m)
                        f.write("\n")
                        f.write("mc_node_associate %d %d\n" % (k+1, k))
                        f.write("\n")
                    f.write("table_add int_table do_int => %d\n" %
                            (i*spine_num+j))
                    f.write("table_add spec_int_table do_spec_int => %d" %
                            (i*spine_num+j))

                with open("../flow_table/command.sh", "a") as f:
                    f.write("sudo ../flow_table/simple_switch_CLI --thrift-port %d <../flow_table/flow_table/s%d_s%d.txt\n"%(thrift_port,i+1,j+1))
                    thrift_port+=1
        # leaf
        for i in xrange(pod_num):
            for j in xrange(leaf_num):
                with open("../flow_table/flow_table/p%d_l%d.txt" % (i+1, j+1), "w") as f:
                    for k in xrange(spine_num):
                        f.write(
                            "table_add mcast_table do_mcast %d => 1\n" % (k+1))
                    temp = 2
                    for k in xrange(spine_num, spine_num+tor_num):
                        f.write(
                            "table_add mcast_table do_mcast %d => %d\n" % (k+1, temp))
                        temp += 1
                    f.write("\n")

                    f.write("mc_mgrp_create 1\n")
                    mcast_list = [
                        n+1 for n in xrange(spine_num, spine_num+tor_num)]
                    mcast_list = tuple(mcast_list)
                    f.write("mc_node_create 0")
                    for m in mcast_list:
                        f.write(" %d" % m)
                    f.write("\n")
                    f.write("mc_node_associate 1 0\n")
                    f.write("\n")

                    temp = 2
                    for k in xrange(spine_num, spine_num+tor_num):
                        f.write("mc_mgrp_create %d\n" % temp)
                        mcast_list = [n+1 for n in xrange(spine_num+tor_num)]
                        mcast_list.remove(k+1)
                        mcast_list = tuple(mcast_list)
                        f.write("mc_node_create %d" % (temp-1))
                        for m in mcast_list:
                            f.write(" %d" % m)
                        f.write("\n")
                        f.write("mc_node_associate %d %d\n" % (temp, temp-1))
                        f.write("\n")
                        temp += 1

                    f.write("table_add int_table do_int => %d\n" %
                            (set_num*spine_num+i*leaf_num+j))
                    f.write("table_add spec_int_table do_spec_int => %d" %
                            (set_num*spine_num+i*leaf_num+j))
                
                with open("../flow_table/command.sh", "a") as f:
                    f.write("sudo ../flow_table/simple_switch_CLI --thrift-port %d <../flow_table/flow_table/p%d_l%d.txt\n"%(thrift_port,i+1,j+1))
                    thrift_port+=1

        # tor
        for i in xrange(pod_num):
            for j in xrange(tor_num):
                with open("../flow_table/flow_table/p%d_t%d.txt" % (i+1, j+1), "w") as f:
                    for k in xrange(leaf_num):
                        f.write(
                            "table_add mcast_table do_mcast %d => 1\n" % (k+1))
                    temp = 2
                    for k in xrange(leaf_num, leaf_num+h_num):
                        f.write(
                            "table_add mcast_table do_mcast %d => %d\n" % (k+1, temp))
                        temp += 1
                    f.write("\n")

                    f.write("mc_mgrp_create 1\n")
                    mcast_list = [
                        n+1 for n in xrange(leaf_num, leaf_num+h_num)]
                    mcast_list = tuple(mcast_list)
                    f.write("mc_node_create 0")
                    for m in mcast_list:
                        f.write(" %d" % m)
                    f.write("\n")
                    f.write("mc_node_associate 1 0\n")
                    f.write("\n")

                    temp = 2
                    for k in xrange(leaf_num, leaf_num+h_num):
                        f.write("mc_mgrp_create %d\n" % temp)
                        mcast_list = [n+1 for n in xrange(leaf_num+h_num)]
                        mcast_list.remove(k+1)
                        mcast_list = tuple(mcast_list)
                        f.write("mc_node_create %d" % (temp-1))
                        for m in mcast_list:
                            f.write(" %d" % m)
                        f.write("\n")
                        f.write("mc_node_associate %d %d\n" % (temp, temp-1))
                        f.write("\n")
                        temp += 1

                    f.write("table_add int_table do_int => %d\n" %
                            (set_num*spine_num+pod_num*leaf_num+i*tor_num+j))
                    f.write("table_add spec_int_table do_spec_int => %d" %
                            (set_num*spine_num+pod_num*leaf_num+i*tor_num+j))
                
                with open("../flow_table/command.sh", "a") as f:
                    f.write("sudo ../flow_table/simple_switch_CLI --thrift-port %d <../flow_table/flow_table/p%d_t%d.txt\n"%(thrift_port,i+1,j+1))
                    thrift_port+=1


if __name__ == "__main__":
    flow_table1 = flow_table()
    flow_table1.flow_table_gen([2,2,2,2,2])
