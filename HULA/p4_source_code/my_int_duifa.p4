/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

header ethernet_t {  
    bit<48>   dstAddr;
    bit<48>   srcAddr;
}

header type_1_t {
    bit<16>   type;    // 0x700:sr; 0x701:int
}

header sr_t {   
    bit<1>    type;     // 0:not last sr; 1:last sr
    bit<7>    rsvd;
    bit<8>    next_port;
}

header type_2_t {   
    bit<16>   type;     // 0x701:int; 0x800:ipv4
}

header int_option_t {   // len = 1B
    bit<1>    type;     // 0 = int probe; 1 = specific flow
    bit<7>    rsvd;          
    bit<8>    int_num;         
}

header inthdr_t {   // len = 28B
    bit<8>    sw_id;
    bit<8>    ingress_port;
    bit<8>    egress_port;
    bit<8>    rsvd;
}

struct headers {
    ethernet_t      ethernet; 
    type_1_t[1]     type_1;
    sr_t[5]         sr;
    type_2_t        type_2;
    int_option_t    int_option;
    inthdr_t        inthdr;
}

struct metadata {
}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition parse_type_1;
    }

    state parse_type_1 {
        packet.extract(hdr.type_1[0]);
        transition select(hdr.type_1[0].type) {
            0x700: parse_sr;
            0x701: parse_int_option;
        }
    }

    state parse_sr {
        packet.extract(hdr.sr.next);
        transition select(hdr.sr.last.type) {
            0: parse_sr;
            1: parse_type_2;
        }
    }

    state parse_type_2 {
        packet.extract(hdr.type_2);
        transition select(hdr.type_2.type) {
            0x701: parse_int_option;
            0x800: accept;
        }
    }

    state parse_int_option {
        packet.extract(hdr.int_option);
        transition accept;
    }
}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply {  }
}

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
    action drop() {
        mark_to_drop();
    }

    action do_sr() {
        standard_metadata.egress_spec = (bit<9>)hdr.sr[0].next_port;
        hdr.sr.pop_front(1);
    }

    action do_sr_final() {
        hdr.type_1.pop_front(1);
    }

    action do_mcast(bit<16> mcast_grp) {
        standard_metadata.mcast_grp = mcast_grp;
    }

    table mcast_table {
        key = {
            standard_metadata.ingress_port: exact;
        }
        actions = {
            do_mcast;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }
    
    apply {
        if(hdr.sr[0].isValid()) {
            if(hdr.sr[0].type==1) {
                do_sr_final();
            }
            do_sr();
        }
        else {
            mcast_table.apply();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {  
    action drop() {
        mark_to_drop();
    }  

    action do_int(bit<8> sw_id) {

        hdr.inthdr.setValid();
        hdr.inthdr.sw_id = sw_id;
        hdr.inthdr.ingress_port=(bit<8>)standard_metadata.egress_port;
        hdr.inthdr.egress_port=(bit<8>)standard_metadata.ingress_port;
        hdr.int_option.int_num = hdr.int_option.int_num + 1;
    }

    action do_spec_int(bit<8> sw_id) {
        hdr.inthdr.setValid();
        hdr.inthdr.sw_id = sw_id;
        hdr.inthdr.ingress_port=(bit<8>)standard_metadata.ingress_port;
        hdr.inthdr.egress_port = (bit<8>)standard_metadata.egress_port;
        hdr.int_option.int_num = hdr.int_option.int_num + 1;
    }

    table int_table {
        actions = {
            do_int;
            NoAction;
        }
        default_action = NoAction();
    }

    table spec_int_table {
        actions = {
            do_spec_int;
            NoAction;
        }
        default_action = NoAction();
    }
    
    apply {
        if (hdr.int_option.isValid()) {
            if (hdr.int_option.type==0) {
                if(standard_metadata.ingress_port == standard_metadata.egress_port) {
                    drop();
                }
                else {
                    int_table.apply();
                }
            }
            else {
                spec_int_table.apply();
            }
        }
        else {
            NoAction();
        }
    }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
    apply {}
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.type_1);
        packet.emit(hdr.sr);
        packet.emit(hdr.type_2);
        packet.emit(hdr.int_option);
        packet.emit(hdr.inthdr);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
