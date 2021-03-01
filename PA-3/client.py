import socket
import pickle
import sys


HOST = '127.0.0.1'
PORT = 65432

f_name = input()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(pickle.dumps(("store", f_name)))
gateway, h = pickle.loads(s.recv(1024))

PORT = int(sys.argv[1])
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((HOST, PORT))

print(h)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(gateway)
s.send(pickle.dumps(("storing", h, (HOST, PORT), 0, 0)))


s1.listen()
conn, addr = s1.accept()
conn.recv(2)


print("sent", conn)

print("sending")
conn.send(pickle.dumps(f_name))
with open(f_name, 'rb') as f:
	data = f.read(1024)
	conn.send(data)
	while data != bytes(''.encode()):
		print(data)
		data = f.read(1024)
		conn.send(data)
conn.close()