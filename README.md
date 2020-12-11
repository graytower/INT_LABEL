# INT-label:Lightweight In-band Network-Wide Telemetry Without Explicitly Using Probe Packets

Fine-grained, network-wide visibility is vital to reliably maintaining and troubleshooting high-density, mega-scale modern data center networks to accommodate heterogeneous mission-critical applications. However, traditional management protocols, such as SNMP, fall short of highresolution monitoring for highly dynamic data center networks due to the inefficient controller-driven, per-device polling mechanism. With end host-launched full-mesh pings, Pingmesh is capable of providing the maximum latency measurement coverage. Pingmesh is excellent but still flawed. It cannot extract hop-by-hop latency or look into the queue depth inside switches for in-depth analysis, but, for network applications such as load balancing, failure localization and management automation, these underlying information is increasingly insightful. In-band Network Telemetry (INT), one of the killer applications of P4, allows probe or data packets to query device-internal states, such as queue depth and queuing latency, when they pass through the data plane pipeline, which is considered promising and has been embedded into several venders’ latest merchant silicon. As a chip-level primitive, INT simply defines the interaction between the incoming packets and the device-internal states for monitoring. For network-wide telemetry, further orchestration on top of INT is needed.

There are two design patterns to achieve network-wide measurement coverage based on INT, that is, distributed probing and centralized probing. HULA follows the distributed probing and adopts the ToR switches to flood the probes into data center network’s multi-rooted topology for measurement coverage. Since each probe sender does not have the global view of the network to make any coordination, one link will be repetitively monitored by many probes simultaneously with huge bandwidth overhead. For high-resolution monitoring, the bandwidth waste will get even worse. To overcome this limitation, centralized probing relies on the SDN controller to make optimized probing path planning. For example, INT-path collects the network topology and generates non-overlapped probing paths that cover the entire network with a minimum path number using an Euler trail-based algorithm. INT-path is theoretically perfect but still has deployment flaws. First, it still explicitly relies on bandwidth-occupying probe packets. Besides, it embeds source routing into the probe packet to specify the route the probe takes. This makes the probe header even bloated especially for a longer probing path. 

![Image text](https://github.com/Ng-95/INT-label/blob/master/INT_label/Architecture.png)

To tackle the above problems, in this work, we propose INT-label, an ultra-lightweight In-band Network-Wide Telemetry architecture. Distinct from previous work, INT-label follows a “probeless” architecture, that is, the INT-label-capable device periodically labels device-internal states onto data packets rather than explicitly introducing probe packets. Specifically, on each outgoing port of the device, the packets will be sampled according to a predefined label interval T and labelled with the instant device-internal states. As a result, INT-label can still achieve network-wide coverage with finegrained telemetry resolution while introducing minor bandwidth overhead. Along the forwarding path consisting of different devices, the same packet will be labelled independently simply according to the local sample decision, that is to say, INT-label is completely stateless without involving any probing path-related dependency. Therefore, there is no need to leverage the SDN controller for conducting centralized path planning. 

INT-label is decoupled from the topology, allowing seamless adaptation to link failures. Like INT, INT-label also relies on the programmability of data plane provided by P4 and the in-network labelling is designed to be transparent to the end hosts. The INT information will be extracted and sent to the SDN controller at the last-hop network device for network-wide telemetry data analysis. To avoid telemetry resolution degradation due to potential loss of labelled packets on some unreliable links, we further design a feedback mechanism to adaptively change the label frequency when the controller gets aware of the packet loss by analyzing the telemetry result.

# Experiment result
Experiment result contains preliminary experimental results data and figures.

## Fig.2
The impact of label interval on coverage rate and bandwidth occupation.

## Fig.3
The number of packet carried INT information under different label interval.

## Fig.4
The data plane label times under different label interval.

## Fig.5
How the relation between label interval and telemetry resolution affects the coverage rate.

## Fig.6
The impact of label interval on coverage rate and INT header bandwidth occupation.

## Fig.7
The impact of data plane label interval on network-wide coverage rate changes over time.

## Fig.8
Different coverage rates under Base A/B and Pro strategies.

## Fig.9 
Network-wide coverage degradation due to loss of packets under Base A/B and Pro strategies.

## Fig.10 
Packet loss rate (due to rate limit) under different label/probe intervals (Base A/B vs HULA).

## Fig.11
Distribution of label times.

## Fig.12.13
### plt.py
The number of vantage servers required under different scale FatTree topologies.
### plt2.py
The bandwidth overhead under different scale FatTree topologies.

# Probability
The result of label times distribution of Base A/B in section Theoretical Analysis.

## poly_simplify.py
The python program for run the results.
If you want to get a specific numerical results, you can run 114-128 lines.

Eza: <a href="https://www.codecogs.com/eqnedit.php?latex=5*k^2*r^5*(k&space;-&space;1)/(4*(k^3/4&space;-&space;1))&space;&plus;&space;5*k^2*r^4*(k&space;-&space;1)*(-r&space;&plus;&space;1)/(k^3/4&space;-&space;1)&space;&plus;&space;15*k^2*r^3*(k&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;5*k^2*r^2*(k&space;-&space;1)*(-r&space;&plus;&space;1)^3/(k^3/4&space;-&space;1)&space;&plus;&space;5*k^2*r*(k&space;-&space;1)*(-r&space;&plus;&space;1)^4/(4*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r^3*(k/2&space;-&space;1)/(2*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r^2*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)/(k^3/4&space;-&space;1)&space;&plus;&space;3*k*r*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;r*(k/2&space;-&space;1)/(k^3/4&space;-&space;1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?5*k^2*r^5*(k&space;-&space;1)/(4*(k^3/4&space;-&space;1))&space;&plus;&space;5*k^2*r^4*(k&space;-&space;1)*(-r&space;&plus;&space;1)/(k^3/4&space;-&space;1)&space;&plus;&space;15*k^2*r^3*(k&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;5*k^2*r^2*(k&space;-&space;1)*(-r&space;&plus;&space;1)^3/(k^3/4&space;-&space;1)&space;&plus;&space;5*k^2*r*(k&space;-&space;1)*(-r&space;&plus;&space;1)^4/(4*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r^3*(k/2&space;-&space;1)/(2*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r^2*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)/(k^3/4&space;-&space;1)&space;&plus;&space;3*k*r*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;r*(k/2&space;-&space;1)/(k^3/4&space;-&space;1)" title="5*k^2*r^5*(k - 1)/(4*(k^3/4 - 1)) + 5*k^2*r^4*(k - 1)*(-r + 1)/(k^3/4 - 1) + 15*k^2*r^3*(k - 1)*(-r + 1)^2/(2*(k^3/4 - 1)) + 5*k^2*r^2*(k - 1)*(-r + 1)^3/(k^3/4 - 1) + 5*k^2*r*(k - 1)*(-r + 1)^4/(4*(k^3/4 - 1)) + 3*k*r^3*(k/2 - 1)/(2*(k^3/4 - 1)) + 3*k*r^2*(k/2 - 1)*(-r + 1)/(k^3/4 - 1) + 3*k*r*(k/2 - 1)*(-r + 1)^2/(2*(k^3/4 - 1)) + r*(k/2 - 1)/(k^3/4 - 1)" /></a>

Pza1: <a href="https://www.codecogs.com/eqnedit.php?latex=5*k^2*r*(k&space;-&space;1)*(-r&space;&plus;&space;1)^4/(4*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;r*(k/2&space;-&space;1)/(k^3/4&space;-&space;1)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?5*k^2*r*(k&space;-&space;1)*(-r&space;&plus;&space;1)^4/(4*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;r*(k/2&space;-&space;1)/(k^3/4&space;-&space;1)" title="5*k^2*r*(k - 1)*(-r + 1)^4/(4*(k^3/4 - 1)) + 3*k*r*(k/2 - 1)*(-r + 1)^2/(2*(k^3/4 - 1)) + r*(k/2 - 1)/(k^3/4 - 1)" /></a>

Pza2: <a href="https://www.codecogs.com/eqnedit.php?latex=5*k^2*r^2*(k&space;-&space;1)*(-r&space;&plus;&space;1)^3/(2*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r^2*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)/(2*(k^3/4&space;-&space;1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?5*k^2*r^2*(k&space;-&space;1)*(-r&space;&plus;&space;1)^3/(2*(k^3/4&space;-&space;1))&space;&plus;&space;3*k*r^2*(k/2&space;-&space;1)*(-r&space;&plus;&space;1)/(2*(k^3/4&space;-&space;1))" title="5*k^2*r^2*(k - 1)*(-r + 1)^3/(2*(k^3/4 - 1)) + 3*k*r^2*(k/2 - 1)*(-r + 1)/(2*(k^3/4 - 1))" /></a>

Pza3: <a href="https://www.codecogs.com/eqnedit.php?latex=5*k^2*r^3*(k&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;k*r^3*(k/2&space;-&space;1)/(2*(k^3/4&space;-&space;1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?5*k^2*r^3*(k&space;-&space;1)*(-r&space;&plus;&space;1)^2/(2*(k^3/4&space;-&space;1))&space;&plus;&space;k*r^3*(k/2&space;-&space;1)/(2*(k^3/4&space;-&space;1))" title="5*k^2*r^3*(k - 1)*(-r + 1)^2/(2*(k^3/4 - 1)) + k*r^3*(k/2 - 1)/(2*(k^3/4 - 1))" /></a>

Pza4: <a href="https://www.codecogs.com/eqnedit.php?latex=5*k^2*r^4*(k&space;-&space;1)*(-r&space;&plus;&space;1)/(4*(k^3/4&space;-&space;1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?5*k^2*r^4*(k&space;-&space;1)*(-r&space;&plus;&space;1)/(4*(k^3/4&space;-&space;1))" title="5*k^2*r^4*(k - 1)*(-r + 1)/(4*(k^3/4 - 1))" /></a>

Pza5: <a href="https://www.codecogs.com/eqnedit.php?latex=k^2*r^5*(k&space;-&space;1)/(4*(k^3/4&space;-&space;1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?k^2*r^5*(k&space;-&space;1)/(4*(k^3/4&space;-&space;1))" title="k^2*r^5*(k - 1)/(4*(k^3/4 - 1))" /></a>

Since the results of Base B are too complicated, we will express these in three parts: gens, monmos, and coefs.
## Ezb.xlsx
The monmos and coef of the E(B).
Ezb.gens: <a href="https://www.codecogs.com/eqnedit.php?latex=(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2),&space;f(3),&space;f(4))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2),&space;f(3),&space;f(4))" title="(r, k, 1/(k^3/4 - 1), f(0), f(1), f(2), f(3), f(4))" /></a>

## Pzb1.xlsx
The monmos and coef of the P(Z<sub>B</sub>=1).
Pzb1.gens: <a href="https://www.codecogs.com/eqnedit.php?latex=(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1))" title="(r, k, 1/(k^3/4 - 1), f(0), f(1))" /></a>

## Pzb2.xlsx
The monmos and coef of the P(Z<sub>B</sub>=2).
Pzb2.gens: <a href="https://www.codecogs.com/eqnedit.php?latex=(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2))" title="(r, k, 1/(k^3/4 - 1), f(0), f(1), f(2))" /></a>

## Pzb3.xlsx
The monmos and coef of the P(Z<sub>B</sub>=3).
Pzb3.gens: <a href="https://www.codecogs.com/eqnedit.php?latex=(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2),&space;f(3))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2),&space;f(3))" title="(r, k, 1/(k^3/4 - 1), f(0), f(1), f(2), f(3))" /></a>

## Pzb4.xlsx
The monmos and coef of the P(Z<sub>B</sub>=4).
Pzb4.gens: <a href="https://www.codecogs.com/eqnedit.php?latex=(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2),&space;f(3),&space;f(4))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(0),&space;f(1),&space;f(2),&space;f(3),&space;f(4))" title="(r, k, 1/(k^3/4 - 1), f(0), f(1), f(2), f(3), f(4))" /></a>

## Pzb5.xlsx
The monmos and coef of the P(Z<sub>B</sub>=5).
Pzb5.gens: <a href="https://www.codecogs.com/eqnedit.php?latex=(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(1),&space;f(2),&space;f(3),&space;f(4))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?(r,&space;k,&space;1/(k^3/4&space;-&space;1),&space;f(1),&space;f(2),&space;f(3),&space;f(4))" title="(r, k, 1/(k^3/4 - 1), f(1), f(2), f(3), f(4))" /></a>

# INT_label
We build an emulation-based network prototype to demonstrate INT-label performance. The hardware configuration is i5-8600k CPU and 32GB memory with Ubuntu 16.04 OS. The prototype is based on Mininet and consists of 1 controller, 4 Spine switches, 4 Leaf switches, 4 ToR switches and 8 servers.
The INT_label include five modules:topology, flow_table, p4_source_code, packet, controller and TIME_OUT.

## topology
Establish a mininet topology and start the packet send&receive process.

### clos.py
First, compile p4 program.
Establish a mininet topology. Here we can control the link bandwidth, delay, maximum queue length, etc.
And initialize the database and start the packet send&receive process.

## flow_table
Initialize the OpenFlow Pipeline of each OVS.

### flow_table_gen.py
Generate the flow table.

### command.sh
Update the flow table.

### flow_table
Include OpenFlow Pipeline.

## p4_source_code
Include p4 source code, implemented SR-based INT function and data plane labelling function of INT-label.

### my_int.p4
Include Headers, Metadatas, parser, deparser and checksum calculator.
SR-based INT function and data plane labelling function are implemented in the program.
If you want to switch from Base A to B, change 0 to 100 in line 250 of my_int.p4.
If you want to change the function $f()$ of Base B algorithm, change line 262-264 and 268 of my_int.p4.

### my_int.json
The json file that compiled from my_int.p4 by p4c compiler.

### run.sh
For compiling the my_int.p4.

## packet
Implement send&receive packet on the server.

### send
Send packet.

#### send_int_probe.py
Based on SR, Server1 and Server8 send data packet to other servers.
Here we can control the traffic rate and forwarding path.

### receive
Receive packet and parse it.

#### parse.py
Extract the INT information.

#### receive.py
Receive packets and parse them using parse.py. And write the latest INT information into the INT database and Aging database (for calculating coverage rate).

## controller 
Implement controller-driven adaptive labelling function and calculate the coverage rate.

### detect1.py
Implement the function of setting int_sampling_flag to 1 for a while.

### detect2.py
Restore the int_sampling_flag to 0 when it is necessary.

### coverage.py
Calculate the coverage rate.

### read_redis.py
Read experimental results.

### flow_table_ctrl
The flow table is used to change the int_sampling_flag, which is modified by the detect1.py and detect2.py.

## TIME_OUT
Store global variable used to control the telemetry resolution.

# How to run INT-label
If you installed the dependencies and configured the database successfully, then you can run the system with commands below:

## Base A/B
```
redis-cli config set notify-keyspace-events KEA
cd controller/
python coverage.py
cd topology/
python clos.py
```
If you want to switch from Base A to B, change 0 to 100 in line 250 of /INT_label/p4_source_code/my_int.p4.

## Pro
```
redis-cli config set notify-keyspace-events KEA
cd controller/
python coverage.py
python detect1.py
python detect2.py
cd topology/
python clos.py
```

You can change bandwidth, max queue size and background traffic rate in clos.py to test INT-label under different conditions.
If you change the topology, you need to modify packet/send/send.py.
You can view the results of the experiment through controller/read_redis.py.

# HULA
We reproduce the code of HULA.
Its the role of each file and usage are similar to those of INT-label.
