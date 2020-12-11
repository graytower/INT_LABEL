import redis
import numpy as np
import time

def calculate_coverage(r,keys):
    all_egress_port=['0-2','2-2','3-1','3-2','4-1','4-4','5-1','5-2','5-3','5-4',
                     '6-3','7-2','7-4','8-1','8-2','8-3','8-4','9-3','9-4','10-3',
                     '10-4','11-1','11-2','11-3','11-4']
    num=0
    for key in keys:
        if int(r.lindex(key,0))!=-1:
            num+=1
    return str(num*100.0/len(all_egress_port))+'%'
    

def read_coverage(r=redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=4)):
    keys=r.keys()
    t=r.lrange('coverage',0,-1)
    t=map(float,t)
    # print(t[-320:-20])
    # print(r.lrange('time',0,-1))
    t=np.array(t)
    # print(t.mean())
    print(t[0:100].mean())
    # print(r.llen('coverage'),r.llen('time'))  
    # print(calculate_coverage(r,keys))
    
def read3(r):
    keys=r.keys()
    for key in keys:
        print(key,r.get(key))
    # print(calculate_coverage(r,keys))
    
def read_loss():
    r3 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=3)
    send=int(r3.get('send'))
    rece=int(r3.get('receive'))
    print((send-rece)*1.0/send)

def read2(r):
    keys=r.keys()
    for key in keys:
        print(key,r.lrange(key,0,-1))
    # print(calculate_coverage(r,keys))
    
if __name__ == '__main__':
       # read(r)
    # read_coverage()
    r2 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=0)
    r3 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock',db=3)
    # read2(r2)
    # time.sleep(20)
    read3(r3)
    read_loss()
    # for i in range(50):
    #     read_coverage()
    #     time.sleep(0.1)
   
    
    