import socket
import pickle
import sys


HOST = "127.0.0.1"
PORT = 65432

f_name = input()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(pickle.dumps(("download", f_name)))
gateway, ha = pickle.loads(s.recv(1024))

PORT = int(sys.argv[1])
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((HOST, PORT))

print(gateway, ha)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(gateway)
s.send(pickle.dumps(("downloading", ha, (HOST, PORT), 0, 0)))

s1.listen()
conn, addr = s1.accept()
if conn.recv(2) == b'ok':
	data = conn.recv(1024)
	f = open(f_name, 'wb')
	while data != bytes(''.encode()):
		print(data)
		f.write(data)
		print("waiting")
		data = conn.recv(1024)
		print("recieved")
		print("written")
	f.close()