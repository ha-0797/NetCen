import threading
import socket
import curses
import time

HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

grid = []

HEIGHT = 30	
WIDTH = 50
MAX_X = WIDTH-2
MAX_Y = HEIGHT-2
TIMEOUT = 95

class snake(object):
	def __init__(self, player, body):
		self.player = player
		self.body = body

for x in range(0, 30):
	grid.append([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])


connections = {}

def listen():
	s.listen()
	players = 0
	while(True):
		conn, addr = s.accept()
		connections[player] = conn