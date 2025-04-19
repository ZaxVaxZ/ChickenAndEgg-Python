import random
import copy
from tkinter import *
from collections import deque
from PIL import ImageTk, Image

Q = deque()
V = []
graph_size = 0

class node:
	def __init__(self, distances):
		global graph_size
		self.id = graph_size
		graph_size += 1
		self.dist = distances
		self.next = []
		for i in range(len(self.dist)):
			self.next.append(node([]))

	def add_node(self, n, dist):
		self.next.append(n)
		self.dist.append(dist)

def BFS(node, target):
	visited.append(node.id)
	Q.append(node.id)
	while(len(Q) > 0):
		curr = Q.popleft()
		for nx in curr.next:
			if nx.id not in visited:
				Q.append(nx.id)

def DFS(node, target):
	global visited
	if node.id in visited:
		return 10e9
	visited.append(visited)
	if node.id == target:
		visited.pop()
		return 0
	mini = 10e9
	for i in range(len(node.next)):
		mini = min(mini, node.dist[i] + DFS(node.next[i], target))
	visited.pop()
	return mini



prev_moves = []
visited = []
off = -1

class Board:
	def __init__(self, x, y):
		self.h = x + 1 if x % 2 != 0 else x
		self.w = y
		self.emp = [-1, -1]
		self.borders = []
		for i in range(self.h//2):
			self.borders.append([])
			for j in range(self.w):
				self.borders[i].append(0)
		self.eggs = []
		for i in range(self.h//2):
			self.eggs.append([])
			for j in range(self.w):
				self.eggs[i].append(0)

	def covering(self, a, b):
		if a is None and b != 0:
			return False
		if a == 3 or a == b or b == 0:
			return True
		return False

	def new_game(self):
		self.emp = [-1, -1]
		self.borders = []
		for i in range(self.h // 2):
			self.borders.append([])
			for j in range(self.w):
				self.borders[i].append(0)
		self.eggs = []
		for i in range(self.h // 2):
			self.eggs.append([])
			for j in range(self.w):
				self.eggs[i].append(0)
		rr = random.randint(0, self.h//2-1)
		rc = random.randint(0, self.w-1)
		self.borders[rr][rc] = None
		self.emp = [rr, rc]
		for i in range(0, self.h//2):
			for j in range(self.w):
				if self.borders[i][j] is not None:
					self.eggs[i][j] = random.randint(0, 3)
					if self.eggs[i][j] > 0:
						rint = random.randint(0, 2)
						if rint == 2:
							self.borders[i][j] = 3
						else:
							self.borders[i][j] = self.eggs[i][j]
		self.eggs[rr][rc] = 0
		shuffled = False
		while not shuffled:
			for i in range(0, self.h // 2 + self.w):
				rind = random.randint(0, len(self.get_valid_moves())-1)
				self.make_move(self.get_valid_moves()[rind], False)
			for i in range(0, self.h // 2):
				if shuffled: break
				for j in range(self.w):
					if not self.covering(self.borders[i][j], self.eggs[i][j]):
						shuffled = True
						break

	def get_uncovered_eggs(self):
		sums = 0
		for i in range(len(self.eggs)):
			for j in range(len(self.eggs[0])):
				if self.eggs[i][j] == 3:
					if self.borders[i][j] != 0:
						sums += 1
					else:
						sums += 2
				elif self.eggs[i][j] == 2:
					if self.borders[i][j] < 2:
						sums += 1
				elif self.eggs[i][j] == 1:
					if self.borders[i][j] != 3 and self.borders[i][j] != 1:
						sums += 1
		return sums

	def get_valid_moves(self):
		mov = []
		if self.emp == [-1, -1]:
			self.new_game()
		if self.emp[0] - 1 >= 0:
			mov.append(0)
		if self.emp[1] - 1 >= 0:
			mov.append(3)
		if self.emp[0] + 1 < self.h//2:
			mov.append(2)
		if self.emp[1] + 1 < self.w:
			mov.append(1)
		return mov

	def get_state(self):
		state = 0
		for i in range(self.h//2):
			for j in range(self.w):
				tmp = 5 if self.borders[i][j] is None else self.borders[i][j]+1
				state += (((i+1)*self.w)+(j+1))*tmp
		return state

	def make_move(self, mv: int, cop: bool):
		if not cop:
			if mv == 0:
				tmp = self.borders[self.emp[0] - 1][self.emp[1]]
				self.borders[self.emp[0] - 1][self.emp[1]] = None
				self.borders[self.emp[0]][self.emp[1]] = tmp
				self.emp = [self.emp[0] - 1, self.emp[1]]
			if mv == 1:
				tmp = self.borders[self.emp[0]][self.emp[1] + 1]
				self.borders[self.emp[0]][self.emp[1] + 1] = None
				self.borders[self.emp[0]][self.emp[1]] = tmp
				self.emp = [self.emp[0], self.emp[1] + 1]
			if mv == 2:
				tmp = self.borders[self.emp[0] + 1][self.emp[1]]
				self.borders[self.emp[0] + 1][self.emp[1]] = None
				self.borders[self.emp[0]][self.emp[1]] = tmp
				self.emp = [self.emp[0] + 1, self.emp[1]]
			if mv == 3:
				tmp = self.borders[self.emp[0]][self.emp[1] - 1]
				self.borders[self.emp[0]][self.emp[1] - 1] = None
				self.borders[self.emp[0]][self.emp[1]] = tmp
				self.emp = [self.emp[0], self.emp[1] - 1]
		else:
			obj = copy.deepcopy(self)
			if mv == 0:
				tmp = obj.borders[obj.emp[0] - 1][obj.emp[1]]
				obj.borders[obj.emp[0] - 1][obj.emp[1]] = None
				obj.borders[obj.emp[0]][obj.emp[1]] = tmp
				obj.emp = [obj.emp[0] - 1, obj.emp[1]]
			elif mv == 1:
				tmp = obj.borders[obj.emp[0]][obj.emp[1] + 1]
				obj.borders[obj.emp[0]][obj.emp[1] + 1] = None
				obj.borders[obj.emp[0]][obj.emp[1]] = tmp
				obj.emp = [obj.emp[0], obj.emp[1] + 1]
			elif mv == 2:
				tmp = obj.borders[obj.emp[0] + 1][obj.emp[1]]
				obj.borders[obj.emp[0] + 1][obj.emp[1]] = None
				obj.borders[obj.emp[0]][obj.emp[1]] = tmp
				obj.emp = [obj.emp[0] + 1, obj.emp[1]]
			elif mv == 3:
				tmp = obj.borders[obj.emp[0]][obj.emp[1] - 1]
				obj.borders[obj.emp[0]][obj.emp[1] - 1] = None
				obj.borders[obj.emp[0]][obj.emp[1]] = tmp
				obj.emp = [obj.emp[0], obj.emp[1] - 1]
			return obj

	def winning(self):
		for i in range(self.h//2):
			for j in range(self.w):
				if not self.covering(self.borders[i][j], self.eggs[i][j]):
					return False
		return True

	def __str__(self):
		return str(self.borders[0]) + "\n" + str(self.borders[1]) + "\n" + \
			str(self.eggs[0]) + "\n" + str(self.eggs[1]) + "\n"

def DFC(b, it=0):
	global prev_moves
	if it >= 900:
		return None
	if b.winning():
		return b
	if b.get_state() in visited:
		return None
	for i in range(len(b.get_valid_moves())):
		if len(prev_moves) > 0 and (prev_moves[-1] == b.get_valid_moves()[i] + 2 or \
				prev_moves[-1] == b.get_valid_moves()[i] - 2):
			continue
		visited.append(b.get_state())
		prev_moves.append(b.get_valid_moves()[i])
		res = DFC(b.make_move(b.get_valid_moves()[i], True), it + 1)
		visited.pop()
		if res is None:
			prev_moves.pop()
			continue
		else:
			if res.winning():
				return res
			else:
				prev_moves.pop()
	return None


def DFC(b, it=0):
	global prev_moves
	if it >= 900:
		return None
	if b.winning():
		return b
	if b.get_state() in visited:
		return None
	for i in range(len(b.get_valid_moves())):
		if len(prev_moves) > 0 and (prev_moves[-1] == b.get_valid_moves()[i] + 2 or \
				prev_moves[-1] == b.get_valid_moves()[i] - 2):
			continue
		visited.append(b.get_state())
		prev_moves.append(b.get_valid_moves()[i])
		res = DFC(b.make_move(b.get_valid_moves()[i], True), it + 1)
		visited.pop()
		if res is None:
			prev_moves.pop()
			continue
		else:
			if res.winning():
				return res
			else:
				prev_moves.pop()
	return None


def Refine(solution):
	if solution is None or solution == []:
		return []
	c = 0
	new_sol = []
	ads = 0
	for i in range(len(solution)):
		if i+ads >= len(solution):
			break
		if i + 4 < len(solution) and solution[i] == solution[i+4]:
			c+=1
		else:
			c = 0
		new_sol.append(solution[i+ads])
		if c == 4:
			tmp = new_sol[-4:]
			new_sol = new_sol[:-4]
			new_sol+=list(reversed(tmp))
			ads += 4
			c = 0
	return new_sol

def NewGame():
	global our_game, grid, result, label_r_top2, visited, prev_moves, off
	off = -1
	visited.clear()
	prev_moves.clear()
	our_game.new_game()
	print("\n", our_game)
	result = DFC(our_game)
	prev_moves = Refine(prev_moves)
	if result is None:
		print(" :( ")
	else:
		print(prev_moves)
	label_r_top2.configure(text=str(len(prev_moves)) + " Moves")
	if len(prev_moves) > 0 and prev_moves[0] == 0:
		label_r_mid.configure(text="UP")
	if len(prev_moves) > 0 and prev_moves[0] == 1:
		label_r_mid.configure(text="RIGHT")
	if len(prev_moves) > 0 and prev_moves[0] == 2:
		label_r_mid.configure(text="DOWN")
	if len(prev_moves) > 0 and prev_moves[0] == 3:
		label_r_mid.configure(text="LEFT")
	if len(prev_moves) == 0:
		label_r_mid.configure(text="- - -")
	Update()

def FullSolution():
	msgbox = Tk()
	msgbox.title('Full Solution')
	msgbox.geometry("300x200")
	txtbox = Label(msgbox, wraplength=290)
	tmpo = ""
	if len(prev_moves) > 0:
		for mov in prev_moves:
			if mov == 0:
				tmpo += "UP "
			if mov == 1:
				tmpo += "RIGHT "
			if mov == 2:
				tmpo += "DOWN "
			if mov == 3:
				tmpo += "LEFT "
	txtbox.configure(text=tmpo)
	txtbox.pack(fill=BOTH, expand=YES)
	msgbox.mainloop(n=1)

def Click(event):
	global our_game, grid, prev_moves, label_r_top, label_r_top2, label_r_mid, off
	if our_game.winning():
		#Update()
		return
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if grid[i][j] is event.widget:
				x = i
				y = j
				break
	xs = x - our_game.emp[0]
	ys = y - our_game.emp[1]
	if xs != 0 and ys != 0:
		return
	move = -1
	if xs == -1:
		move = 0
	if xs == 1:
		move = 2
	if ys == -1:
		move = 3
	if ys == 1:
		move = 1
	our_game.make_move(move, False)
	Update()
	if off == -10:
		label_r_top.configure(text="Off Track")
		label_r_top2.configure(text="?? Moves")
		label_r_mid.configure(text="- - -")
		return
	if len(prev_moves) == 0:
		off = -10
		return
	if move == prev_moves[0]:
		prev_moves = prev_moves[1:]
		if not our_game.winning():
			label_r_top2.configure(text=str(len(prev_moves)) + " Moves")
			if len(prev_moves) > 0 and prev_moves[0] == 0:
				label_r_mid.configure(text="UP")
			if len(prev_moves) > 0 and prev_moves[0] == 1:
				label_r_mid.configure(text="RIGHT")
			if len(prev_moves) > 0 and prev_moves[0] == 2:
				label_r_mid.configure(text="DOWN")
			if len(prev_moves) > 0 and prev_moves[0] == 3:
				label_r_mid.configure(text="LEFT")
		if len(prev_moves) == 0:
			label_r_mid.configure(text="- - -")
	elif off!=-1:
		if off == move+2 or off == move-2:
			off = -1
		else:
			off = -10
	else:
		label_r_top.configure(text="Wrong Input!")
		label_r_top2.configure(text="Off Track")
		label_r_mid.configure(text="- - -")
		off = move

def Update():
	global our_game, grid, result, label_r_top2, visited, prev_moves
	label_r_top.configure(text="Solution")
	for i in range(our_game.h // 2):
		for j in range(our_game.w):
			txt = ""
			if our_game.borders[i][j] is not None and \
					(our_game.borders[i][j] == 2 or our_game.borders[i][j] == 3):
				txt += "C "
			if our_game.eggs[i][j] == 2 or our_game.eggs[i][j] == 3:
				txt += "E"
			txt += "\n\n\n"
			if our_game.borders[i][j] is not None and \
					(our_game.borders[i][j] == 1 or our_game.borders[i][j] == 3):
				txt += "C "
			if our_game.eggs[i][j] == 1 or our_game.eggs[i][j] == 3:
				txt += " E"
			grid[i][j].configure(text=txt)
			if our_game.borders[i][j] is None:
				grid[i][j].configure(bg="white")
			else:
				grid[i][j].configure(bg="chocolate")
	if our_game.winning():
		label_r_top.configure(text="Game Over")
		label_r_top2.configure(text="You Won!!")
		label_r_mid.configure(text="- - -")
		return


visi = []
moves = []

infinity = 1000000000

curr_lowest = infinity


def h_cost(x, m):
	return x.make_move(m, True).get_uncovered_eggs()


def f_cost(m):
	return 10 if m % 2 == 0 else 15


vis_A = []
moves_A = []
total_A = infinity


def AsTAR(b, it, cost):
	global vis_A, total_A, moves_A
	if it >= 750:
		return None
	if b.winning():
		if cost < total_A:
			total_A = cost
			return b
		else:
			return None
	if b.get_state() in vis_A:
		return None
	vis_A.append(b.get_state())
	m_temp = []
	
	for i in range(len(b.get_valid_moves())):
		m_temp.append([f_cost(b.get_valid_moves()[i])+h_cost(b, b.get_valid_moves()[i]), b.get_valid_moves()[i]])
		
	while len(m_temp) > 0:
		x, m_temp = get_min_move(m_temp)
		res = AsTAR(b.make_move(x[1], True), it + 1, cost + x[0])
		if res is None:
			continue
		else:
			moves_A.append(x[1])
	vis_A.pop()
	return b


def get_min_move(arr):
	mini = infinity
	k = 0
	for i in range(len(arr)):
		if arr[i][0] < mini:
			mini = arr[i][0]
			k = i
	u = arr[k]
	p = arr[:k]
	p += arr[k+1:]
	return u, p

if __name__ == "__main__":
	our_game = Board(4, 4)
	our_game.new_game()
	print(our_game)
	print(moves)
	result = DFC(our_game)
	prev_moves = Refine(prev_moves)
	if result is None:
		print(" :( ")
	else:
		print(prev_moves)

	window = Tk()
	window.title('Lonely Eggs')
	window.geometry("600x400")
	window.resizable(height = None, width = None)

	main = PanedWindow(window, sashwidth=7, sashrelief=RIDGE)
	main.pack()

	bgl = ImageTk.PhotoImage(Image.open("HayBack.jpg")) 
	bgr = ImageTk.PhotoImage(Image.open("Wall.jpg")) 

	left = Canvas(main, width=400, height=400)
	left.background = bgl
	bgl = left.create_image(0, 0, anchor=NW, image=bgl)
	grid = []
	for i in range(our_game.h//2):
		grid.append([])
		for j in range(our_game.w):
			grid[i].append(Button(left,width=int(10*(4/our_game.w)),
								height=int(11*(4/our_game.h)))) #, command=lambda:[Click(i, j)]))
			grid[i][j].bind("<Button-1>", Click)
			txt = ""
			if our_game.borders[i][j] is not None and \
					(our_game.borders[i][j] == 2 or our_game.borders[i][j] == 3):
				txt += "C "
			if our_game.eggs[i][j] == 2 or our_game.eggs[i][j] == 3:
				txt += "E"
			txt+="\n\n\n"
			if our_game.borders[i][j] is not None and \
					(our_game.borders[i][j] == 1 or our_game.borders[i][j] == 3):
				txt += "C "
			if our_game.eggs[i][j] == 1 or our_game.eggs[i][j] == 3:
				txt += " E"
			grid[i][j].configure(text=txt)
			if our_game.borders[i][j] is not None:
				grid[i][j].configure(bg="chocolate")
			grid[i][j].place(relx=(0.5/our_game.w)+(1/our_game.w)*j, rely=(0.5/(our_game.h//2))+(1/(our_game.h//2))*i, anchor=CENTER)


	right = Canvas(main, width=200, height=400)
	right.background = bgr
	bgr = right.create_image(95, 200, anchor=CENTER, image=bgr)
	label_r_top = Label(right, width=10, height=2, text="Solution", bg="lightblue", font=("Courier", 20, 'bold'))
	label_r_top.place(x=95, y=10, anchor=N)
	label_r_top2 = Label(right, width=10, height=2, text=str(len(prev_moves))+" Moves", bg="lightblue", font=("Courier", 16, 'bold'))
	label_r_top2.place(x=95, y=100, anchor=N)
	label_r_mid = Label(right, width=5, height=2, text="- - -", fg="white", bg="blue", font=("Courier", 16))
	if len(prev_moves) > 0 and prev_moves[0] == 0:
		label_r_mid.configure(text="UP")
	if len(prev_moves) > 0 and prev_moves[0] == 1:
		label_r_mid.configure(text="RIGHT")
	if len(prev_moves) > 0 and prev_moves[0] == 2:
		label_r_mid.configure(text="DOWN")
	if len(prev_moves) > 0 and prev_moves[0] == 3:
		label_r_mid.configure(text="LEFT")
	label_r_mid.place(x=95, y=200, anchor=CENTER)
	button_r_bot2 = Button(right, text="New Game", font=("Courier", 14), command=NewGame)
	button_r_bot2.place(x=95, y=340, anchor=S)
	button_r_bot3 = Button(right, text="Full Solution", font=("Courier", 14), command=FullSolution)
	button_r_bot3.place(x=95, y=390, anchor=S)

	main.add(left)
	main.add(right)
	main.pack(expand=1, fill='both')
	main.paneconfigure(main.panes()[0], minsize=400)
	main.paneconfigure(main.panes()[0], width=400)
	main.paneconfigure(main.panes()[1], minsize=200)

	window.mainloop()
