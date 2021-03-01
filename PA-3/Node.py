import socket
import sys
import threading
import math
import pickle
import time

HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

PORT = int(sys.argv[1])
m = int(sys.argv[2])
num = int(math.log(m,2))

s.send(pickle.dumps(("join", (HOST, PORT))))
temp = s.recv(1024)
hash_value, gateway = pickle.loads(temp)

print(hash_value)

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print((HOST, PORT))
s1.bind((HOST, PORT))

def fingers(h):
	List = []
	n = int(math.log(m, 2))
	i = 1
	sub = 0
	for x in range(0,n):
		if sub == 0 and (h + i - sub) > m:
			sub = m 
		List.append(h+i-sub)
		i = i*2
	return List 

class stop(threading.Thread):

	def __init__(self, node, t1, t2, t3):
		threading.Thread.__init__(self) 
		self.n = node
		self._stop_event = threading.Event()
		self.t1 = t1
		self.t2 = t2
		self.t3 = t3

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	def run(self):
		choice = ''
		while(choice != 's'):
			print("Enter 's' to leave: ")
			choice = input()
		t3.stop()
		if self.n.succ[0][0] != self.n.addr:		
			for x in self.n.files.keys():
				s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s2.connect(self.n.succ[0][0])
				s2.send(pickle.dumps(("leaving", n.suxx[0][0], n.hash[0][1], 0, 0)))
				s2.recv(2)
				f_name = self.n.files[x]
				s2.send(pickle.dumps((f_name, x)))
				with open(f_name, 'rb') as f:
					data = f.read(1024)
					s2.send(data)
					while data != bytes(''.encode()):
						print(data)
						data = f.read(1024)
						s2.send(data)
				s2.close()

			for x in range(0, len(self.n.succ)):
				if self.n.succ[x][0] != self.n.addr:
					s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s2.connect(self.n.succ[x][0])
					s2.send(pickle.dumps(("left", self.n.pred, self.n.addr, 0, 0)))	
					s2.close()
			
			if self.n.pred[0] != self.n.addr:
				s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s2.connect(self.n.succ[0][0])
				s2.send(pickle.dumps(("left", self.n.succ[0], self.n.addr, 0, 0)))	
				s2.close()
			t3.stop()
			s.send(pickle.dumps(("leaving", self.n.hash)))
			time.sleep(30)
			

class find_sucessors(threading.Thread):

	def __init__(self, node):
		threading.Thread.__init__(self) 
		self.n = node
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	def run(self):
		print("looking")
		if gateway != self.n.addr:
			for x in range(0,num):
				s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s2.connect(gateway)
				s2.send(pickle.dumps(("join", self.n.fingers[x], self.n.addr, self.n.hash, x)))
				n.succ[x] = pickle.loads(s2.recv(1024))

class refresh(threading.Thread):

	def __init__(self, node):
		threading.Thread.__init__(self) 
		self.n = node
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	def run(self):
		while(not self.stopped()):
			time.sleep(10)
			print("refreshing")
			for x in range(0,num):
				if self.n.succ[x][0] != self.n.addr:
					s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
					s2.connect(self.n.succ[x][0])
					s2.send(pickle.dumps(("refresh", self.n.fingers[x], self.n.addr, self.n.hash, x)))
					self.n.succ[x] = pickle.loads(s2.recv(1024))

				else:
					if self.n.pred[0] != self.n.addr:
						a = self.n.pred[1] - self.n.fingers[x]
						b = self.n.hash - self.n.fingers[x]
						if self.n.fingers[x] > self.n.hash:
							b += m
						if self.n.fingers[x] > self.n.pred[1]:
							a += m
						if a < b:
							self.n.succ[x] = self.n.pred
							s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
							s2.connect(self.n.succ[x][0])
							s2.send(pickle.dumps(("refresh", self.n.fingers[x], self.n.addr, self.n.hash, x)))
							self.n.succ[x] = pickle.loads(s2.recv(1024))
		
			for x in range(0,num):
				print(self.n.fingers[x], self.n.succ[x])
			print(self.n.pred)
class join(threading.Thread):

	def __init__(self, node):
		threading.Thread.__init__(self) 
		self.n = node
		self._stop_event = threading.Event()

	def stop(self):
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set()

	def run(self):
		print("listening")
		s1.listen()
		while(not self.stopped()):
			conn, Addr = s1.accept()
			pur, h, addr, ha, pos = pickle.loads(conn.recv(1024))
			if pur == "join":

				a = self.n.pred[1]
				b = self.n.hash

				if h > a:
					a += m - h 
				if h > b: 
					b += m - h

				if a >= b:
					if pos == 0:
						self.n.pred = (addr, ha)
					conn.send(pickle.dumps((self.n.addr, self.n.hash)))
				else:
					passed = True
					
					pos = 0
					for x in range(num-1, -1, -1):
						a = self.n.fingers[pos]
						b = self.n.fingers[x]
						if a > b:
							if h < a or (h < m and h > b):
								s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								s2.connect(self.n.succ[x][0])
								s2.send(pickle.dumps((pur, h, addr, ha, pos)))
								print("send to", self.n.succ[x][0])
								temp = s2.recv(1024)
								conn.send(temp)
								break		
						else:
							if h < a and h > b:
								s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								s2.connect(self.n.succ[x][0])
								s2.send(pickle.dumps((pur, h, addr, ha, pos)))
								print("send to", self.n.succ[x][0])								
								temp = s2.recv(1024)
								conn.send(temp)
								break
						pos -= 1		

						# if h > self.n.succ[x][1]:
						# 	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						# 	s2.connect(self.n.succ[x][0])
						# 	s2.send(pickle.dumps((pur, h, addr, ha, pos)))
						# 	print("passed on")
						# 	passed = False
						# 	temp = s2.recv(1024)
						# 	conn.send(temp)
						# 	break
						# if passed:
						# 	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						# 	s2.connect(self.n.succ[9][0])
						# 	s2.send(pickle.dumps((pur, h, addr, ha, pos)))
						# 	print("passed on to last")
						# 	passed = False
						# 	temp = s2.recv(1024)
						# 	conn.send(temp)							
				conn.close()

			if pur == "refresh":

				a = self.n.pred[1] - h
				b = self.n.hash - h
				
				if h > self.n.hash:
					b += m
				if h > self.n.pred[1]:
					a += m
				
				if b < a:
					if pos == 0:
						self.n.pred = (addr, ha)
					conn.send(pickle.dumps((self.n.addr, self.n.hash)))
				else:
					conn.send(pickle.dumps(self.n.pred))

			if pur == "leaving":
				conn.send(b'ok')
				conn.recv(2)
				file_name, h = pickle.loads(conn.recv(1024))	
				data = conn.recv(1024)
				f = open(file_name, 'wb')
				while data != bytes(''.encode()):
					print(data)
					f.write(data)
					print("waiting")
					data = conn.recv(1024)
					print("recieved")
					print("written")
				f.close()
				conn.send(b'ok')
				self.n.files[h] = file_name

			if pur == "left":
				if addr == self.n.pred:
					for x in range(0,num):
						if self.n.succ[x][0] == addr:
							self.n.succ[x] = (self.n.addr ,self.n.hash)
				
				for x in range(0,num):
					if self.n.succ[x][0] == addr:
						self.n.succ[x] = h
			if pur == "downloading":
				print(pur, h, addr, ha, pos)
				a = self.n.pred[1] - h
				b = self.n.hash - h
				
				if h > self.n.hash:
					b += m
				if h > self.n.pred[1]:
					a += m

				print(a, b)
				if a >= b:
					s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s2.connect(addr)
					if h not in self.n.files.keys():
						s2.send(b'no')
					else:
						s2.send(b'ok')

						file_name = self.n.files[h]	
						with open(file_name, 'rb') as f:
							data = f.read(1024)
							s2.send(data)
							while data != bytes(''.encode()):
								print(data)
								data = f.read(1024)
								s2.send(data)
						s2.close()

				else:
					passed = True
					
					pos = 0
					for x in range(num-1, -1, -1):
						a = self.n.fingers[pos]
						b = self.n.fingers[x]
						if a > b:
							if h < a or (h < m and h > b):
								s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								s2.connect(self.n.succ[x][0])
								s2.send(pickle.dumps((pur, h, addr, ha, pos)))
								print("send to", self.n.succ[x][0])
								break		
						else:
							if h < a and h > b:
								s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								s2.connect(self.n.succ[x][0])
								s2.send(pickle.dumps((pur, h, addr, ha, pos)))
								print("send to", self.n.succ[x][0])								
								break
						pos -= 1		


			if pur == "storing":
				print(pur, h, addr, ha, pos)
				a = self.n.pred[1] - h
				b = self.n.hash - h
				
				if h > self.n.hash:
					b += m
				if h > self.n.pred[1]:
					a += m


				print(a, b)
				if a < b:
					s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s2.connect(addr)
					s2.send(b'ok')

					file_name = pickle.loads(s2.recv(1024))	
					data = s2.recv(1024)
					f = open(file_name, 'wb')
					while data != bytes(''.encode()):
						print(data)
						f.write(data)
						print("waiting")
						data = s2.recv(1024)
						print("recieved")
						print("written")
					f.close()
					s2.send(b'ok')
					self.n.files[h] = file_name

				else:
					passed = True
					
					pos = 0
					for x in range(num-1, -1, -1):
						a = self.n.fingers[pos]
						b = self.n.fingers[x]
						if a > b:
							if h < a or (h < m and h > b):
								s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								s2.connect(self.n.succ[x][0])
								s2.send(pickle.dumps((pur, h, addr, ha, pos)))
								print("send to", self.n.succ[x][0])
								break		
						else:
							if h < a and h > b:
								s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
								s2.connect(self.n.succ[x][0])
								s2.send(pickle.dumps((pur, h, addr, ha, pos)))
								print("send to", self.n.succ[x][0])								
								break
						pos -= 1		


class Node(object):
	def __init__(self, hash_value):
		self.hash = hash_value
		self.addr = (HOST, PORT)
		self.succ = []
		self.files = {}
		self.fingers = fingers(self.hash)
		for i in range(0, num):
			self.succ.append((self.addr, self.hash))
		self.pred = ((self.addr, self.hash + 1))

n = Node(hash_value)

t1 = join(n)
t2 = find_sucessors(n)
t3 = refresh(n)
t4 = stop(n, t1, t2, t3)
t1.start()
t2.start()
t3.start()
t4.start()
t4.join()
print("here")
t1.stop()
t2.stop()
t3.stop()
t1.join()
t2.join()
t3.join()
print("\n\n\n\n\n We are done")