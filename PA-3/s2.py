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

HOST = '127.0.0.1'  
PORT = 65432        

server_dict = {}
json_dict = {}
threads = []


class Food(Object):
	def __init__(self, char = "*"):
		self.x = randint(1, MAX_X)
		self.y = randint(1, MAX_Y)
		self.char = char

	def reset(self):
		self.x = randint(1, MAX_X)
		self.y = randint(1, MAX_Y)

food = Food()

def left(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(1)-1)
	else:
		food.reset()
		server_dict['food'] = (food.x, food.y)
	if l[0][0] <= 1:
		l = [(MAX_X,l[0][1])] + l
	else:
		l = [(l[0][0] - 1,l[0][1])] + l
	server_dict[player] = l
	
	for key in json_dict:
		server_dict[key][player].append('left')


def right(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(1)-1)
	else:
		food.reset()
		server_dict['food'] = (food.x, food.y)
	if l[0][0] >= MAX_X:
		l = [(0,l[0][1])] + l
	else:
		l = [(l[0][0] + 1,l[0][1])] + l
	server_dict[player] = l

	for key in json_dict:
		server_dict[key][player].append('right')


def up(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(1)-1)
	else:
		food.reset()
		server_dict['food'] = (food.x, food.y)
	if l[0][1] <= 1:
		l = [(l[0][0], MAX_Y)] + l
	else:
		l = [(l[0][0], l[0][1]-1)] + l
	server_dict[player] = l

	for key in json_dict:
		server_dict[key][player].append('up')


def down(player):
	l = json_dict[player]
	if not l[0] == (food.x, food.y):
		l.pop(len(1)-1)
	else:
		food.reset()
		server_dict['food'] = (food.x, food.y)
	if l[0][0] >= MAX_Y:
		l = [(l[0][0], 0)] + l
	else:
		l = [(l[0][0], l[0][1] + 1)] + l
	server_dict[player] = l

	for key in json_dict:
		server_dict[key][player].append('down')


def listen(conn, q):
	while True:
		data = conn.recv(1024):
		if not data:
			break
		temp = json.loads(data)
		if temp['move'] == 'left':
			q.put((temp['player'], 'left', conn))
		if temp['move'] == 'right':
			q.put((temp['player'], 'right', conn))
		if temp['move'] == 'up':
			q.put((temp['player'], 'up', conn))
		if temp['move'] == 'down':
			q.put((temp['player'], 'down', conn))

def con(q):
	init_dict = {}
	init_dict ['window'] = [HEIGHT, WIDTH, TIMEOUT, MAX_Y, MAX_X]
	s.bind((HOST, PORT))
	s.listen()
	players = 0
	print("listening")
	while True:
		conn, addr = s.accept()
		init_dict['player'] = players
		conn.sendall(json_dict(init_dict).encode())
		while True:
			x = randint(4, MAX_X)
			y = randint(4, MAX_Y)
			found = false
			for key in json_dict:
				if (x, y) in json_dict[key]:
					found = True
					break
				if (x - 1, y) in json_dict[key]:
					found = True
					break
				if (x - 2, y) in json_dict[key]:
					found = True
					break
			if found == False:
				break
		json_dict[players] = [(x, y), (x - 1, y), (x - 2, y)]

		for key in server_dict:
			server_dict[key][players] = json_dict[players]

		t = threading.Thread(target = listen, args = (conn, q))
		threads.append(t)
		t.start()
		conn.sendall(json.dumps(json_dict).encode())
		players += 1

q = queue.Queue()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cons = threading.Thread(target = con, args = (q,))
cons.start()

while True:
	move = q.get()

	if move[0] in json_dict:
		if move[1] == 'left':
			left(move[0])
		elif move[1] == 'right':
			right(move[0])
		elif move[1] == 'up':
			up(move[0])
		elif move[1] == 'down':
			down(move[0])


	col1 = False
	col2 = False
	hit = -1

		for player in json_dict:
			if player == move[0]:
				l = json_dict[move[0]]
				p = l[0]
				for i, body in enumerate(l):
					if i > 3:
						if body == p:
							a = True
							break
			else:
				l = json_dict[player]
				p = json_dict[move[0]][0]
				if l != None:
					for i,body in enumerate(l):
						if bodt == p:
							a = True
							if i == 0:
								b = True
								hit = player
							break

			if a == True:
				break
		if a:
			json_dict.pop(move[0])
			server_dict.pop(move[0])
			for key in server_dict:
				server_dict[key].pop()
		if b:
			json_dict.pop(hit)
			server_dict.pop(hit)
		move[2].sendall(json.dumps(server_dict[move[0]]).encode())
	else:
		move[2].sendall(json.dumps(server_dict[move[0]]).encode())
	server_dict.pop(move[0])
	threads = [t for t in threads if not t.isAlive()]