import socket
import json
from random import randint
import threading
import queue
import time

HEIGHT = 30	
WIDTH = 120
MAX_X = WIDTH-2
MAX_Y = HEIGHT-2
TIMEOUT = 95

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

json_dict = {}

init_dict = {}
init_dict['window'] = [HEIGHT, WIDTH, TIMEOUT, MAX_Y, MAX_X]

threads = []

class Food(object):
	def __init__(self, char='*'):
		self.x = randint(1, MAX_X)
		self.y = randint(1, MAX_Y)
		self.char = char

	def reset(self):
		self.x = randint(1, MAX_X)
		self.y = randint(1, MAX_Y)

food = Food('*')

json_dict['food'] = (food.x, food.y)

def left(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(l)-1)
	else: 
		food.reset()
		json_dict['food'] = (food.x, food.y)
	if l[0][0] <= 1:
		l = [(MAX_X, l[0][1])] + l
	else:
		l = [(l[0][0] - 1, l[0][1])] + l
	json_dict[player] = l

def right(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(l)-1)
	else: 
		food.reset()
		json_dict['food'] = (food.x, food.y)
	if l[0][0] >= MAX_X:
		l = [(0, l[0][1])] + l
	else:
		l = [(l[0][0] + 1, l[0][1])] + l
	json_dict[player] = l

def up(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(l)-1)
	else: 
		food.reset()
		json_dict['food'] = (food.x, food.y)
	if l[0][1] <= 1:
		l = [(l[0][0], MAX_Y)] + l
	else:
		l = [(l[0][0] , l[0][1] - 1)] + l
	json_dict[player] = l

def down(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(l)-1)
	else: 
		food.reset()
		json_dict['food'] = (food.x, food.y)
	if l[0][1] >= MAX_Y:
		l = [(l[0][0], 0)] + l
	else:
		l = [(l[0][0] , l[0][1]+1)] + l
	json_dict[player] = l

def listen(conn,q):
	while True:
   		data = conn.recv(1024)
   		if not data:
   			break
   		temp = json.loads(data)
   		if temp['move'] == 'left':
   			q.put((temp['player'], 'left', conn))
   		elif temp['move'] == 'right':
   			q.put((temp['player'], 'right', conn))
   		elif temp['move'] == 'up':
   			q.put((temp['player'], 'up', conn))
   		elif temp['move'] == 'down':
   			q.put((temp['player'], 'down', conn))

def con(q):
	s.bind((HOST, PORT))
	s.listen()
	players = 0
	print("listening")
	while True:
		conn, addr = s.accept()
		while True:
			x = randint(4, MAX_X)
			y = randint(4, MAX_Y)
			found = False
			for key in json_dict:
				if (x, y) in json_dict[key]:
					found = True
					break
				if (x - 2, y) in json_dict[key]:
					found = True
					break
				if (x - 1, y) in json_dict[key]:
					found = True
					break
			if found == False:
				break
		json_dict[players] = [(x, y), (x-1, y), (x-1, y)]
		init_dict['player'] = players
		t = threading.Thread(target = listen, args = (conn,q))
		threads.append(t)
		conn.sendall(json.dumps(init_dict).encode())		
		conn.sendall(json.dumps(json_dict).encode())
		t.start()
		players += 1


q = queue.Queue()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cons = threading.Thread(target = con, args = (q,))
cons.start()

while True:
	
	move = q.get()
	
	if move[0] in json_dict.keys():
		if move[1] == 'left':
			left(move[0])
		elif move[1] == 'right':
			right(move[0])
		elif move[1] == 'down':
			down(move[0])
		elif move[1] == 'up':
			up(move[0])
		
		b = False
		a = False
		hit = 0

		if move[0] in json_dict.keys():
			for player in json_dict:
				if player != move[0]:
					l = json_dict[player]
					p = json_dict[move[0]]
					if l != None:
						for i, body in enumerate(l):
							if body ==  p[0]:
								a = True
								if i == 0:
									b = True
									hit = player
								break
				else:
					l = json_dict[move[0]]
					p = json_dict[move[0]][0]
					for i, body in enumerate(l):
						if i > 3:
							if body == p:
								a = True
								break
				if b == True:
					break
			if a:
				json_dict.pop(move[0])
			if b:
				json_dict.pop(hit)
				
		b = json.dumps(json_dict)
		move[2].sendall(b.encode())
	else:
		b = json.dumps(json_dict)
		move[2].sendall(b.encode())

	threads = [t for t in threads if not t.isAlive()]