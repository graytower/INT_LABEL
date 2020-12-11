import socket

server_addr="/tmp/server.sock"

sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
sock.bind(server_addr)
sock.listen(5)

while True:
    conn,clintAddr=sock.accept()
    while True:
        data=conn.recv(100)
        print(data)
	conn.sendall(data)
