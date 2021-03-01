import curses

HEIGHT = 30	
WIDTH = 50
MAX_X = WIDTH-2
MAX_Y = HEIGHT-2
TIMEOUT = 95

world = []

for x in range(0,30):
	world.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

class snake(object):
	def __init__(self, window):
		self.window = window
		self.home = home(self, self.window)
class home(object):
	def __init__(self, snek, window):
		self.snake = snek
		self.body = world
		self.window = window
		self.body[10][10] = 1
		self.body[10][11] = 1
		self.body[11][10] = 1
		self.body[11][11] = 1

	def render(self):
		for i, row in enumerate(self.body):
			for j, col in enumerate(row):
				if self.body[i][j] == 1:
					self.window.addstr(j, i, "1")

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
		window.clear()
		window.border(0)

		snek = snake(window)
		snek.home.render()
		event = window.getch()
		
		if event == 27:
			break

		if event == 32:
			key = -1
			while(key != 32):
				key = window.getch()

		time.sleep(0.05)
	curses.endwin()
