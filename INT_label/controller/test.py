import os
import redis

r = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')
r3= redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=2)
pubsub=r.pubsub()
pubsub.psubscribe('__keyevent@0__:expired')

# error=None
i=0
time_out=4*25 #4*25ms 
os.system('sudo pwd')


# data=message['data']
data='8-2'
sw_id,egress_port=data.split('-')
with open("./flow_table_ctrl/switch%s.txt" % (sw_id), "w") as f:
    f.write('table_modify set_flag_table set_flag %d => 1'%(int(egress_port)-1))
os.system('sudo ../flow_table/simple_switch_CLI --thrift-port %d < ./flow_table_ctrl/switch%s.txt' % (int(sw_id)+9090,sw_id))
r3.set(data,-1)
r3.pexpire(data,time_out)