import socket
import curses
import time

HOST = '127.0.0.1'
PORT = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST, PORT))

curses.initscr()
window = curses.newwin(HEIGHT, WIDTH, 0, 0)
window.keypad(1)
curses.noecho()
curses.curs_set(0)
window.border(0)
event = window.getch()
if event == 32:
	key = -1
	while(key != 32):
		key = window.getch()		
time.sleep(5)
curses.endwin()