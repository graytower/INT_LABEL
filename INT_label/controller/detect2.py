import redis
import os

r3=redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=2)
pubsub=r3.pubsub()
pubsub.subscribe('__keyevent@2__:expired')

i=0
os.system('sudo pwd')
while(True):
    message=pubsub.get_message() 
    if(message!=None):
        if i==0:
            i+=1
            continue
        data=message['data']
        # print(message)
        sw_id,egress_port=data.split('-')
        with open("./flow_table_ctrl/switch%s.txt" % (sw_id), "w") as f:
            f.write('table_modify set_flag_table set_flag %d => 0'%(int(egress_port)-1))
        os.system('sudo ../flow_table/simple_switch_CLI --thrift-port %d < ./flow_table_ctrl/switch%s.txt' % (int(sw_id)+9090,sw_id))
