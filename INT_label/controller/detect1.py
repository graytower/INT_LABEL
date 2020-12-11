import os
import redis

r = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390)
r3= redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=2)
pubsub=r.pubsub()
pubsub.psubscribe('__keyevent@0__:expired')

with open('../TIME_OUT','r') as f:
    TIME_OUT=int(f.readline())

# error=None
i=0
os.system('sudo pwd')
while(True):
    message=pubsub.get_message() 
    if(message!=None):
        if i==0:
            i+=1
            continue
        data=message['data']
        sw_id,egress_port=data.split('-')
        with open("./flow_table_ctrl/switch%s.txt" % (sw_id), "w") as f:
            f.write('table_modify set_flag_table set_flag %d => 1'%(int(egress_port)-1))
        os.system('sudo ../flow_table/simple_switch_CLI --thrift-port %d < ./flow_table_ctrl/switch%s.txt' % (int(sw_id)+9090,sw_id))
        r3.set(data,-1)
        r3.pexpire(data,10*TIME_OUT)

