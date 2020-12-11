import socket
import parse
# import processor
import redis

from scapy.all import get_if_addr


class receive():
    def sniff(self):
        s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW,
                          socket.htons(0x0003))
        r4 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=3)
        src_ip = get_if_addr("eth0")
        parse1 = parse.parse()

        while True:
            data = s.recv(2048)
            if not data:
                print ("Client has exist")
                break
            rs = parse1.filter(data)
            # rs= dip,dmac,port1,port2,port3,delta_time
            if rs != None:
                if rs==1:
                    r4.incr('receive')
                # port=map(str,rs[2])
                # fmt=[src_ip,rs[0],rs[1]]+map(str,rs[2])
                # key="+".join(fmt)
                # value=rs[3]
                # r.set(key,value)
                #r.pexpire(key,1000)
        s.close()


if __name__ == "__main__":
    receive1 = receive()
    receive1.sniff()
