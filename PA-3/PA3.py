import mmh3
import socket
import threading
import pickle

HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


def h(string):
	return mmh3.hash(string, signed = False) % 1000

table = {}

def listen():
	print("listening")
	s.listen()
	while(True):
		conn, addr = s.accept()
		pur, addr = pickle.loads(conn.recv(1024))
		if pur == "join":
			host, port = addr
			h_value = h(host + str(port))
			gateway = addr
			
			for x in table.keys():
				gateway = table[x][1]
				break

			conn.send(pickle.dumps((h_value, gateway)))
			table[h_value] = (conn, addr)
		
		if pur == "store":
			for x in table.keys():
				gateway = table[x][1]
				break
			conn.send(pickle.dumps((gateway, h(addr))))
		if pur == "download":
			for x in table.keys():
				gateway = table[x][1]
				break
			conn.send(pickle.dumps((gateway, h(addr))))
		if pur == "leaving":
			print(table.pop(addr))

t1 = threading.Thread(target = listen, args = (),)
t1.start()