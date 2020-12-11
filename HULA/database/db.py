import redis
import time

r = redis.Redis(host='127.0.0.1', port=0)
r.flushdb()
a1=('10.0.0.1','aa:aa:aa:aa:aa:aa',[(5,4,2,0,0,0,0,0,0),(2,2,1,0,0,0,0,0,0),(4,2,4,0,0,0,0,0,0)])
r.rpush(1,a1[0],a1[1])
for i in range(3):
    for j in range(9):
        r.rpush(1,a1[2][i][j])
rs=r.lrange(1,0,28)
print(r.keys)

 # /var/run/redis/redis.sock
