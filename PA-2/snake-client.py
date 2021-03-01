import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import socket
import json
import time

HOST = '192.168.100.7'
PORT = 65432

client_dict = {'player' : 0, 'move' : ''}

direction = KEY_RIGHT
dir_map = {KEY_UP : 'up', KEY_RIGHT : 'right', KEY_LEFT : 'left', KEY_DOWN : 'down'}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

temp = s.recv(1024)

server_dict = json.loads(temp)
player_no = server_dict['player']
client_dict['player'] = player_no 
client_dict['move'] = dir_map[KEY_RIGHT]

HEIGHT = server_dict['window'][0]
WIDTH = server_dict['window'][1]
MAX_X = server_dict['window'][4]
MAX_Y = server_dict['window'][3]
TIMEOUT = server_dict['window'][2]

REV_DIR_MAP = {
		KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
		KEY_LEFT:KEY_RIGHT, KEY_RIGHT:KEY_LEFT,
	}

class Snake(object):

	def __init__(self, l, window, player):
		self.player = player
		self.body_list = l
		self.window = window
		self.timeout = TIMEOUT
		self.window.timeout(self.timeout)
		self.direction = KEY_RIGHT
		self.last_head_coor = l[0]

	def render(self):
		for body in range(len(self.body_list)):
			self.window.addstr(self.body_list[body][1], self.body_list[body][0], "=")
		self.window.addstr(self.body_list[0][1], self.body_list[0][0], self.player)

if __name__ == '__main__':
	curses.initscr()
	curses.beep()
	curses.beep()

	window = curses.newwin(HEIGHT, WIDTH, 0, 0)
	window.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	window.border(0)
	while True:
		b = json.dumps(client_dict)
		s.send(b.encode())
		temp = s.recv(1024)
		server_dict = json.loads(temp)
		window.clear()
		window.border(0)
		if not str(player_no) in server_dict.keys():
			print("u ded son")
			break
		for key in server_dict:
			if key != 'food':
				snek = Snake(server_dict[key], window, key)
				snek.render()


		window.addstr(server_dict['food'][1], server_dict['food'][0], '*')

		event = window.getch()
		if event in [KEY_UP, KEY_RIGHT, KEY_LEFT, KEY_DOWN]:
			if event != REV_DIR_MAP[direction]:
					direction = event
					client_dict['move'] = dir_map[event]

		if event == 27:
			break

		if event == 32:
			key = -1
			while(key != 32):
				key = window.getch()

		time.sleep(0.05)
	curses.endwin()
