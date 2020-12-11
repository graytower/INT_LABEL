import socket
import parse
# import processor
import redis
import os

from scapy.all import get_if_addr
# time_out=1*10 #2*20ms
with open(os.path.abspath(os.path.join(os.getcwd(), ".."))+'/TIME_OUT','r') as f:
    TIME_OUT=int(f.readline())

class receive():
    def sniff(self):
        s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
        r = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390)       # aging database
        r2 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=1) # persist database
        r4 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=3) # data database
        src_ip = get_if_addr("eth0")
        parse1 = parse.parse()
        while True:
            data = s.recv(2048)
            if not data:
                print ("Client has exist")
                continue         
            
            rs = parse1.filter(data)    # []: without INT data; False: not data packet
            
            # rs= dip,dmac,port1,port2,port3,delta_time
            # print(rs)
            if rs!=False: # data packet
                r4.incr('receive')
                if len(rs)!=0: # data packet with int info
                    r4.incr('int')
                    r4.incr(str(len(rs)))
                else:
                    r4.incr('0')
                    continue             
                for int_info in rs:
                    # print(int_info)
                    r4.incr('all')
                    key=str(int_info[0])+'-'+str(int_info[1])
                    # value=[int_info[2],int_info[3]]
                    if r2.exists(key)==True: # find this key
                        v=int(r2.lindex(key,0))
                        if v<int_info[2]:
                            r2.lset(key,0,int_info[2])
                            r2.lset(key,1,int_info[3])
                            if r.exists(key)==True: # redundancy probing
                                # r.persist(key)
                                r4.incr('extra')
                                try:
                                    r.lset(key,0,int_info[2])
                                    r.lset(key,1,int_info[3])
                                    r.pexpire(key,TIME_OUT)
                                except: # no such key
                                    r.lpush(key,int_info[2],int_info[3])
                                    r.pexpire(key,TIME_OUT)
                            else:
                                # print(key)
                                r.lpush(key,int_info[2],int_info[3])
                                r.pexpire(key,TIME_OUT)
                    else: #not find this key
                        r2.lpush(key,int_info[2],int_info[3])
                        r.lpush(key,int_info[2],int_info[3])
                        r.pexpire(key,TIME_OUT)

        s.close()


if __name__ == "__main__":
    receive1 = receive()
    receive1.sniff()
