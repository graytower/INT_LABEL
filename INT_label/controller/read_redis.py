import redis
import numpy as np
import time

    

def read_coverage(r=redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=4)):
    keys=r.keys()
    t=r.lrange('coverage',0,-1)
    t=map(float,t)
    # print(t[0:100])
    # print(r.lrange('time',0,-1))
    t=np.array(t)
    # print(t.mean())
    print(t[0:100].mean())
    # print(t[0])
    # print(r.llen('coverage'),r.llen('time'))
    
    
def read3(r):
    keys=r.keys()
    for key in keys:
        print(key,r.get(key))

def read_loss(r3 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=3)):
    send=int(r3.get('send'))
    rece=int(r3.get('receive'))
    print((send-rece)*1.0/send)
    
def read2(r):
    keys=r.keys()
    for key in keys:
        print(key,r.lrange(key,0,-1))

def read_data(r = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=1)):
    keys=r.keys()
    l=[]
    for i in range(50):
        a=0
        num=0
        for key in keys:
            if r.lrange(key,0,-1)[0]!='-1':
                a+=float(r.lindex(key,1))
                num+=1
        l.append(a/num)
        time.sleep(0.1)
    l=np.array(l)
    print(l.mean())
    print(l.std())

def read_redundancy(r = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=3)):
    rece=int(r.get('receive'))
    intP=int(r.get('int'))
    print('INT packet rate:',intP*1.0/rece)

    intN=int(r.get('all'))
    extra=int(r.get('extra'))
    print('int info rate:',intN*1.0/rece)

def read_distribution(r = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=3)):
    rece=int(r.get('receive'))
    num0=int(r.get('0'))
    num1=int(r.get('1'))
    num2=int(r.get('2'))
    num3=int(r.get('3'))
    num4=int(r.get('4'))
    num5=int(r.get('5'))
    print(num0*1.0/rece)
    print(num1*1.0/rece)
    print(num2*1.0/rece)
    print(num3*1.0/rece)
    print(num4*1.0/rece)
    print(num5*1.0/rece)
    
    
if __name__ == '__main__':
    r2 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=1)
    r3 = redis.Redis(unix_socket_path='/var/run/redis/redis-server.sock',port=6390,db=3)
    # read2(r2)
    # time.sleep(20)
    # read3(r3)
    # read_distribution()
    # read_data()
    read_redundancy()
    # read_coverage()
    # for i in range(50):
    #     read_coverage()
    #     time.sleep(0.1)
    # read_loss()
   
    
    