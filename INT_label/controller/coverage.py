import redis
import time
from datetime import datetime
# TIME_OUT=2*10 # 2*100ms

def calculate_coverage(r):
    all_egress_port=['0-2','2-2','3-1','3-2','4-1','4-4','5-1','5-2','5-3','5-4',
                     '6-3','7-2','7-4','8-1','8-2','8-3','8-4','9-3','9-4','10-3',
                     '10-4','11-1','11-2','11-3','11-4']
    t=r.keys()
    result=len(r.keys())*1.0/len(all_egress_port)
    # print(result)
    if result>1:
        return '0.0'
    else: 
        return str(result)
    

    

    
    
if __name__=='__main__':
    with open('../TIME_OUT','r') as f:
        TIME_OUT=int(f.readline())
    r = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390)       # aging database
    r4 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=3) # data database
    r5 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=4) # coverage database
    pubsub=r.pubsub()
    pubsub.psubscribe('__keyevent@0__:l*')
    start = datetime.utcnow()
    
    all_egress_port=['0-2','2-2','3-1','3-2','4-1','4-4','5-1','5-2','5-3','5-4',
                     '6-3','7-2','7-4','8-1','8-2','8-3','8-4','9-3','9-4','10-3',
                     '10-4','11-1','11-2','11-3','11-4']
    num=len(all_egress_port)
    while True:       
        s=datetime.utcnow()
        t=datetime.utcnow()-s
        r_s=set()
        while (t.seconds*1000000+t.microseconds)<TIME_OUT*1000:
            message=pubsub.get_message() 
            
            if(message!=None):
                # if i==0:
                #     i+=1
                # continu
                data=message['data']
                r_s.add(data) 
            t=datetime.utcnow()-s       
        # delta=(datetime.utcnow()-start)
        print(set(all_egress_port)-r_s)
        cover=len(r_s)*1.0/num
        if cover<=1:
            # r5.lpush('time',t.seconds*1000000+t.microseconds)
            r5.lpush('coverage',cover)   
        else:
            # r5.lpush('time',t.seconds*1000000+t.microseconds)
            r5.lpush('coverage',0.0)   
