import struct
import socket
import redis


class parse():

    def filter(self, pkt_raw):
        pkt_len = len(pkt_raw)
        pkt = struct.unpack("!14s%ds" % (pkt_len-14), pkt_raw)
        ethernet = self.parse_ethernet(pkt[0])
        if ethernet[2] == 2048:
            return 1
        else:
            return 0
            # pkt = struct.unpack("!2s%ds" % (pkt_len-14-2), pkt[1])
            # int_option = self.parse_int_option(pkt[0])
            # if int_option[0] == 0:
            #     data = self.int_process(pkt_raw)
            #     return data

    def int_process(self, pkt_raw):
        pkt_len = len(pkt_raw)
        pkt = struct.unpack("!14s2s%ds" % (pkt_len-14-2), pkt_raw)
        ethernet = self.parse_ethernet(pkt[0])
        int_option = self.parse_int_option(pkt[1])
        if int_option[1] != 0:     # not received from locol
            pkt = pkt[2]  # int+data
            fmt = "!"
            for i in range(int_option[1]):
                fmt = fmt+"4s"
            pkt = struct.unpack(fmt+"2s20s", pkt)
            int_list = []
            for i in range(len(pkt[:-2])):
                int_list.append(self.parse_int(pkt[i]))
            ip = self.parse_ipv4(pkt[-1])
            # return ip[10],ethernet[1],sw_list,int_list
            sw_port_list = []
            for i in int_list:
                sw_port_list.append("sw_%d-%d"%(i[0],i[1]))
                sw_port_list.append("sw_%d-%d"%(i[0],i[2]))
            print(sw_port_list)

            # delta_time=int_list[0][7]+int_list[1][7]+int_list[2][7]
            delta_time = 0
            # return ip[10], ethernet[1], int_list[0][2], int_list[1][2], int_list[2][2], delta_time
            return ip[10], ethernet[1], sw_port_list, delta_time

    # B: unsigned char 1B; H: unsigned short 2B; I: unsigned int 4B

    def parse_ethernet(self, pkt):
        ethernet = struct.unpack("!6B6BH", pkt)
        ethernet_str = []
        for i in range(12):
            temp = ethernet[i]
            temp = (hex(temp))[2:]
            if len(temp) == 1:
                temp = "0"+temp
            ethernet_str.append(temp)

        dstAddr = "%s:%s:%s:%s:%s:%s" % (
            ethernet_str[0], ethernet_str[1], ethernet_str[2], ethernet_str[3], ethernet_str[4], ethernet_str[5])  # 1
        srcAddr = "%s:%s:%s:%s:%s:%s" % (
            ethernet_str[6], ethernet_str[7], ethernet_str[8], ethernet_str[9], ethernet_str[10], ethernet_str[11])  # 2
        etherType = ethernet[12]  # 3
        return dstAddr, srcAddr, etherType

    def parse_ipv4(self, pkt):
        ipv4 = struct.unpack("!BBHHHBBH4s4s", pkt)
        version = (ipv4[0] & 0xf0) >> 4  # 1
        ihl = ipv4[0] & 0x0f  # 2
        diffserv = ipv4[1]  # 3
        totalLen = ipv4[2]  # 4
        identification = ipv4[3]  # 5
        flags = (ipv4[4] & 0xe000) >> 13  # 6
        fragOffset = ipv4[4] & 0x1fff  # 7
        ttl = ipv4[5]  # 8
        protocol = ipv4[6]  # 9
        hdrChecksum = ipv4[7]  # 10
        srcAddr = ipv4[8]  # 11
        dstAddr = ipv4[9]  # 12
        srcAddr = socket.inet_ntoa(srcAddr)
        dstAddr = socket.inet_ntoa(dstAddr)
        return version, ihl, diffserv, totalLen, identification, flags, fragOffset, ttl, protocol, hdrChecksum, srcAddr, dstAddr

    def parse_int_option(self, pkt):
        int_option = struct.unpack("!BB", pkt)
        int_type = (int_option[0] & 0x80) >> 7  # 1
        int_num = int_option[1]  # 2
        return int_type, int_num

    def parse_int(self, pkt):
        inthdr = struct.unpack("!BBBs", pkt)
        sw_id = inthdr[0]
        ingress_port = inthdr[1]
        egress_port = inthdr[2]
        return sw_id, ingress_port, egress_port


if __name__ == "__main__":
    pass
