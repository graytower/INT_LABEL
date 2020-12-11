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
    bit<16>   type;    // 0x700:sr; else:find route table
}

header sr_hdr_t {
    bit<1>    next_hdr;
    bit<7>    rsvd;
    bit<8>    sr_length;
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
    bit<8>    rsvd0;
    bit<48>   ingress_global_timestamp;
    bit<48>   egress_global_timestamp;
    bit<32>   enq_timestamp;
    bit<8>    rsvd1;
    bit<24>   enq_qdepth;
    bit<32>   deq_timedelta;
    bit<8>    rsvd2;
    bit<24>   deq_qdepth;
}

header last_egress_global_timestamp_md_t {
    bit<48>   last_egress_global_timestamp;
}

header int_sampling_flag_md_t {
    bit<8>   int_sampling_flag;    // 0: sampling; 1: all
}

header int_number_md_t {
    bit<8>   int_num;    
}


struct headers {
    ethernet_t      ethernet; 
    type_1_t[1]     type_1;
    sr_hdr_t[1]     sr_hdr;
    sr_t[5]         sr;
    type_2_t        type_2;
    int_option_t    int_option;
    inthdr_t        inthdr;
}

struct metadata {
    last_egress_global_timestamp_md_t last_egress_global_timestamp_md;
    int_sampling_flag_md_t int_sampling_flag_md;
    int_number_md_t int_num_md;
}

register<bit<48>>(960) last_egress_global_timestamp;
register<bit<48>>(960) T1_value;

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
        transition parse_sr_hdr;
    }

    state parse_sr_hdr {
        packet.extract(hdr.sr_hdr[0]);
        transition parse_sr;
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
        meta.int_num_md.int_num=hdr.int_option.int_num;
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
        hdr.sr_hdr.pop_front(1);
    }
    
    apply {
        if(hdr.sr[0].type==1) {
            do_sr_final();
        }
        do_sr();
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

    action set_flag(bit<8> flag){
        meta.int_sampling_flag_md.int_sampling_flag = flag;    
    }

    action do_int(bit<8> sw_id) {
        hdr.inthdr.setValid();

        hdr.inthdr.sw_id = sw_id;
        hdr.inthdr.ingress_port=(bit<8>)standard_metadata.ingress_port;
        hdr.inthdr.egress_port=(bit<8>)standard_metadata.egress_port;
        hdr.inthdr.ingress_global_timestamp=(bit<48>)standard_metadata.ingress_global_timestamp;
        hdr.inthdr.egress_global_timestamp=(bit<48>)standard_metadata.egress_global_timestamp;
        hdr.inthdr.enq_timestamp=(bit<32>)standard_metadata.enq_timestamp;
        hdr.inthdr.enq_qdepth=(bit<24>)standard_metadata.enq_qdepth;
        hdr.inthdr.deq_timedelta=(bit<32>)standard_metadata.deq_timedelta;
        hdr.inthdr.deq_qdepth=(bit<24>)standard_metadata.deq_qdepth;

        hdr.int_option.int_num = hdr.int_option.int_num + 1;
    }

    table set_flag_table {
        key = {
            standard_metadata.egress_port: exact;
        }
        actions = {
            set_flag;
            NoAction;
        }
        default_action = NoAction();
    }

    table int_table {
        actions = {
            do_int;
            NoAction;
        }
        default_action = NoAction();
    }

    table int_table_sampling {
        actions = {
            do_int;
            NoAction;
        }
        default_action = NoAction();
    }

    table int_table_sampling2 {
        actions = {
            do_int;
            NoAction;
        }
        default_action = NoAction();
    }
    
    apply {
        if (hdr.int_option.isValid()) {
            set_flag_table.apply();
            if(meta.int_sampling_flag_md.int_sampling_flag==1){
                int_table.apply();
                last_egress_global_timestamp.write((bit<32>)standard_metadata.egress_port, standard_metadata.egress_global_timestamp);
            }
            else{
                bit<48> T=50000;
                bit<48> T1=T*0/100;
                T1_value.write(1, (bit <48>) T1);
                bit<48> MAX_hop=5; // for fattree topology
                bit<48> a=1; // weights for P_num
                bit<48> b=0; // weights for P_time
                last_egress_global_timestamp.read(meta.last_egress_global_timestamp_md.last_egress_global_timestamp, (bit<32>)standard_metadata.egress_port);
                if(standard_metadata.egress_global_timestamp - meta.last_egress_global_timestamp_md.last_egress_global_timestamp >T)
                {
                    int_table_sampling.apply();
                    last_egress_global_timestamp.write((bit<32>)standard_metadata.egress_port, standard_metadata.egress_global_timestamp);
                }
                else if(standard_metadata.egress_global_timestamp - meta.last_egress_global_timestamp_md.last_egress_global_timestamp >T1){
                    bit<8> int_num_val=meta.int_num_md.int_num;
                    if(int_num_val>3){
                        int_num_val=(bit <8>) MAX_hop;
                    }
                    bit<48> rand_val;
                    random(rand_val,0,a*(T-T1)+b*(T-T1));
                    if(rand_val<a*(bit <48>) int_num_val*((T-T1)/MAX_hop)+b*(standard_metadata.egress_global_timestamp - meta.last_egress_global_timestamp_md.last_egress_global_timestamp-T1)){
                        int_table_sampling2.apply();
                        last_egress_global_timestamp.write((bit<32>)standard_metadata.egress_port, standard_metadata.egress_global_timestamp);
                    }
                }
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
        packet.emit(hdr.sr_hdr);
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
