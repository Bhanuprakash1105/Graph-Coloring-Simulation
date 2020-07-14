from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import random
import turtle

def checkInput(inValue, canBeZero, positive):
	if not inValue.isdigit():
		return False
	if canBeZero and positive:
		return int(inValue) >= 0
	elif positive and not canBeZero:
		return int(inValue) > 0
	elif not positive and canBeZero:
		return int(inValue) == 0
	else:
		return int(inValue) < 0

def checkInputRangeClosedBar(inValue, a, b):
	return (int(inValue) >= a) and (int(inValue) <= b)

def rgb(r, g, b):
	assert(r <= 255 and r >= 0)
	assert(g <= 255 and g >= 0)
	assert(b <= 255 and b >= 0)
	return "#%02x%02x%02x" % (r, g, b)

window = Tk()
window.title("GRAPH COLORING SIMULATION INPUT")
width = int(window.winfo_screenwidth())
height = int(window.winfo_screenheight())
window.geometry("{0}x{1}+0+0".format(int(width*0.7), int(height*0.7)))
window.config(bg = rgb(252, 68, 69))

proceed1_cleaner = False

myFont = font.Font(family = "Source Code Pro Medium", size = 12)
buttonFont = font.Font(family = "Source Code Pro Medium", size = 12, weight = "bold")

graph, labelEdgeInput, entryEdgeInput1, entryEdgeInput2 = list(), list(), list(), list()

def showOutput(result, ncu):
	global window, width, height, graph
	window2 = Toplevel(window)
	window2.title("GRAPH COLORING SIMULATION INPUT")
	window2.geometry("{0}x{1}+0+0".format(int(width*0.7), int(height*0.7)))
	window2.config(bg = rgb(255, 255, 255))

	displayOutput = Label(window2, text = "The number of colors used are only = {0}, observe properly".format(ncu))
	displayOutput['font'] = myFont
	displayOutput['bg'] = rgb(255, 255, 255)
	displayOutput.pack()

	cv = turtle.ScrolledCanvas(window2)
	cv.pack(fill = "both", expand = True)

	screen = turtle.TurtleScreen(cv)
	screen.screensize(5000, 5000)

	no_of_vertices = len(graph)
	angle = 360/no_of_vertices

	shapeMaker = turtle.RawTurtle(screen)
	shapeMaker.hideturtle()
	shapeMaker.speed(100)
	shapeMaker.color(rgb(255, 255, 255), rgb(255, 255, 255))

	mul = 1
	while no_of_vertices > mul or mul%10 != 0:
		mul += 1
	d = mul*10

	vertex, vertexID = list(), list()
	for i in range(no_of_vertices):
		x, y = shapeMaker.position()
		vertex.append(turtle.RawTurtle(screen))
		vertex[i].hideturtle()
		vertex[i].speed(100)
		vertex[i].color(rgb(255, 255, 255), rgb(255, 255, 255))
		vertex[i].setpos(x, y)
		vertexID.append(turtle.RawTurtle(screen))
		vertexID[i].hideturtle()
		vertexID[i].speed(100)
		vertexID[i].color(rgb(255, 255, 255), rgb(255, 255, 255))
		vertexID[i].setpos(x, y)
		shapeMaker.left(angle)
		shapeMaker.fd(d)

	for i in range(no_of_vertices):
		vertex[i].color(result[i], result[i])
		vertex[i].begin_fill()
		vertex[i].circle(20)
		vertex[i].end_fill()
		vertexID[i].color("black", "black")
		vertexID[i].write(i, False, "center", font  = ("Arial", 12, "bold"))
	
	drawEdges = list()
	k = 0
	for i in range(len(graph)):
		for j in range(len(graph[i])):
			drawEdges.append(turtle.RawTurtle(screen))
			drawEdges[k].hideturtle()
			drawEdges[k].speed(100)
			drawEdges[k].color(rgb(255, 255, 255), rgb(255, 255, 255))
			x, y = vertex[i].position()
			drawEdges[k].setpos(x, y)
			k += 1
	
	for i in range(no_of_vertices):
		vertex[i].color(result[i], result[i])
		vertex[i].begin_fill()
		vertex[i].circle(20)
		vertex[i].end_fill()
		vertexID[i].color("black", "black")
		vertexID[i].write(i, False, "center", font  = ("Arial", 12, "bold"))

	k = 0
	for i in range(len(graph)):
		for j in range(len(graph[i])):
			x, y = vertex[graph[i][j]].position()
			drawEdges[k].color(rgb(0, 0, 0), rgb(0, 0, 0))
			drawEdges[k].goto(x, y)
			k += 1

class Scrollable(Frame):
	def __init__(self, frame, width, height):
		scrollbar = Scrollbar(frame, width = width)
		scrollbar.pack(side=RIGHT, fill=Y, expand=False)
		self.canvas = Canvas(frame, yscrollcommand=scrollbar.set, height = height, bg = rgb(85, 188, 201), bd=0, highlightthickness=0)
		self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
		scrollbar.config(command=self.canvas.yview, elementborderwidth = 0)
		self.canvas.bind('<Configure>', self.__fill_canvas)
		Frame.__init__(self, frame, bg = rgb(85, 188, 201), bd = 0, padx = 5, pady = 20)         
		self.windows_item = self.canvas.create_window(0, 0, window=self, anchor=NW)

	def __fill_canvas(self, event):
		"Enlarge the windows item to the canvas width"
		canvas_width = int(event.width)
		self.canvas.itemconfig(self.windows_item, width = canvas_width)        

	def update(self):
		"Update the canvas and the scrollregion"
		self.update_idletasks()
		self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))

frame1 = Frame(window, bg = rgb(85, 188, 201))
frame2 = Frame(window, bg = rgb(85, 188, 201))
frame3 = Frame(window, bg = rgb(85, 188, 201))
frame1.pack(fill = X, pady = (0, 15))
frame2.pack(fill = X)
frame2.config(padx = 5, pady = 15, bd = 0)
frame3.pack(fill = BOTH, pady = (15, 5))

scrollFrame = Scrollable(frame2, 28, int(height*0.5))

def allowed(adj, color, result):
	for x in adj:
		if result[x] == color:
			return False
	return True

def coloring(graph, vertex, colors, result, flag):
	if vertex >= len(graph):
		flag[0] = True
		return
	for i in range(len(colors)):
		if allowed(graph[vertex], colors[i], result):
			result[vertex] = colors[i]
			coloring(graph, vertex + 1, colors, result, flag)
			if flag[0]:
				return
			result[vertex] = 0

def generate_Colors(nc):
	colors = []
	returnColors = []
	xc = 0
	while xc < nc:
		c = [random.randint(0, 255) for r in range(3)]
		flag = True
		for i in range(len(colors)):
			if abs(colors[i][0] - c[0]) + abs(colors[i][1] - c[1]) + abs(colors[i][2] - c[2]) < 60:
				flag = False
				break
		if flag:
			colors.append(c)
			returnColors.append(rgb(c[0], c[1], c[2]))
			xc += 1
	return returnColors

def solver(graph, nc):
	colors = [i for i in range(1, nc + 1, 1)]
	result = ["" for i in range(len(graph))]
	flag = [False]
	coloring(graph, 0, colors, result, flag)
	if flag[0]:
		rSet = set(result)
		messagebox.showinfo("SOLUTION","\nMinimum number of colors required for coloring the given graph = {0} only\n\nObserve the graph in the new window popped up".format(len(rSet)))
		realColors = generate_Colors(len(rSet))
		finalResult = [""]*len(result)
		for i in range(len(result)):
			finalResult[i] = realColors[result[i]-1]
		print("The final = ",finalResult)
		showOutput(finalResult, len(rSet))
	else:
		messagebox.showinfo("SOLUTION","Given undirected graph cannot be colored using only \"{0}\" colors".format(nc))
		return

def step2Func(entryEdgeInput1, entryEdgeInput2, entryColorCount, entryNodeCount, entryEdgeCount):
	global graph
	if len(graph) != int(entryNodeCount.get()) or len(entryEdgeInput1) != int(entryEdgeCount.get()):
		messagebox.showwarning("INPUT WARNING","INPUT HAS BEEN ALTERED\n\n\"RE-ENTER\" ALL THE INPUT VALUES FROM BEGINING")
		return
	if not checkInput(entryColorCount.get(), False, True):
		messagebox.showwarning("INPUT ERROR","Input is not valid\n\n[1] Probably entered zero\n\n[2] Maybe due to string input")
		return
	for i in range(len(entryEdgeInput1)):
		if not checkInput(entryEdgeInput1[i].get(), True, True) or not checkInput(entryEdgeInput2[i].get(), True, True):
			messagebox.showwarning("INPUT ERROR","Input is not valid\n\nMaybe due to string input or negative values")
			return
		if not checkInputRangeClosedBar(entryEdgeInput1[i].get(), 0, len(graph)-1) or not checkInputRangeClosedBar(entryEdgeInput2[i].get(), 0, len(graph)-1):
			messagebox.showwarning("INPUT ERROR","Input is not valid\n\nMaybe due to values of vertices in edge entries are incorrect")
			messagebox.showinfo("INPUT NOTE FOR EDGES","Edges input values range -> {0} <= vertex numbers <= {1}".format(0, len(graph)-1))
			return
	nc = int(entryColorCount.get())
	temp = len(graph)
	for i in range(temp):
		graph[i] = list()
	for i in range(len(entryEdgeInput1)):
		a, b = int(entryEdgeInput1[i].get()), int(entryEdgeInput2[i].get())
		graph[a].append(b)
		graph[b].append(a)
	solver(graph, nc)

def step1Func():
	if not checkInput(entryNodeCount.get(), False, True) or not checkInput(entryEdgeCount.get(), False, True):
		messagebox.showwarning("INPUT ERROR","Input is not valid\n\n[1] Probably entered zero\n\n[2] Maybe due to string input")
		return
	global scrollFrame, window, labelEdgeInput, entryEdgeInput1, entryEdgeInput2, frame2, height, frame3, graph
	thisFrame = scrollFrame
	global proceed1_cleaner
	innerCheck = False
	if not proceed1_cleaner:
		proceed1_cleaner = True
	else:
		frame2.pack_forget()
		frame3.pack_forget()
		frame2 = Frame(window, bg = rgb(85, 188, 201))
		scrollFrame = Scrollable(frame2, 28, int(height*0.5))
		thisFrame = scrollFrame
		innerCheck = True
		labelEdgeInput, entryEdgeInput1, entryEdgeInput2 = list(), list(), list()
	n = int(entryNodeCount.get())
	e = int(entryEdgeCount.get())
	graph = list()
	for i in range(n):
		graph.append(list())
	i = 0
	for i in range(e):
		labelEdgeInput.append(Label(thisFrame, text = "Enter edge number [" + str(i) +"] :- "))
		labelEdgeInput[i].config(bd = 0)
		labelEdgeInput[i]['font'] = myFont
		labelEdgeInput[i]['bg'] = rgb(0, 0, 0)
		labelEdgeInput[i]['fg'] = rgb(255, 255, 255)
		labelEdgeInput[i].grid(row = i, column = 0, columnspan = 1, padx = 7, pady = 10)
		entryEdgeInput1.append(Entry(thisFrame, width = 4))
		entryEdgeInput1[i].config(bd = 0)
		entryEdgeInput1[i]['font'] = myFont
		entryEdgeInput1[i].grid(row = i, column = 1, columnspan = 1, padx = 7, pady = 10)
		entryEdgeInput1[i].insert(0, 0)
		entryEdgeInput2.append(Entry(thisFrame, width = 4))
		entryEdgeInput2[i].config(bd = 0)
		entryEdgeInput2[i]['font'] = myFont
		entryEdgeInput2[i].grid(row = i, column = 2, columnspan = 1, padx = 7, pady = 10)
		entryEdgeInput2[i].insert(0, 0)

	if innerCheck:
		frame2.pack(fill = X)
		frame2.config(padx = 5, pady = 15, bd = 0)
		frame3.pack(fill = BOTH, pady = 20) 
	scrollFrame.update()

	colorCount = Label(frame3, text = "Enter the maximum number of colors can be used for coloring the undriected graph: ")
	colorCount['font'] = myFont
	colorCount['bg'] = rgb(0, 0, 0)
	colorCount['fg'] = rgb(255, 255, 255)
	colorCount.grid(row = 0, column = 0, columnspan = 2, padx = (15, 0), pady = 10)
	entryColorCount = Entry(frame3, width = 4)
	entryColorCount['font'] = myFont
	entryColorCount.grid(row = 0, column = 2, columnspan = 1, padx = (0, 15), pady = 10)
	entryColorCount.insert(0, 0)

	step2Button = Button(frame3, text = "Solution", bg = rgb(71, 209, 71), fg = rgb(255, 255, 255), padx = 5, pady = 2, command = lambda: step2Func(entryEdgeInput1, entryEdgeInput2, entryColorCount, entryNodeCount, entryEdgeCount))
	step2Button['font'] = buttonFont
	step2Button.grid(row = 0, column = 3, columnspan = 3, padx = (25, 5), pady = 10)

labelNodeCount = Label(frame1, text = "Enter the number of VERTICES in the undirected graph: ", bg = rgb(0, 0, 0), fg = rgb(255, 255, 255))
labelNodeCount['font'] = myFont
labelNodeCount.grid(row = 0, column = 0, columnspan = 2, padx = (15, 0), pady = 10)
entryNodeCount = Entry(frame1, width = 4)
entryNodeCount['font'] = myFont
entryNodeCount.grid(row = 0, column = 2, columnspan = 1, padx = (1, 15), pady = 10)
entryNodeCount.insert(0, 0)

labelEdgeCount = Label(frame1, text = "Enter the number of EDGES in the undirected graph: ", bg = rgb(0, 0, 0), fg = rgb(255, 255, 255))
labelEdgeCount['font'] = myFont
labelEdgeCount.grid(row = 0, column = 3, columnspan = 2, padx = (15, 0), pady = 10)
entryEdgeCount = Entry(frame1, width = 4)
entryEdgeCount['font'] = myFont
entryEdgeCount.grid(row = 0, column = 5, columnspan = 1, padx = (1, 15), pady = 10)
entryEdgeCount.insert(0, 0)

step1Button = Button(frame1, text = "Continue", command = step1Func, bg = rgb(71, 209, 71), fg = rgb(255, 255, 255), padx = 5, pady = 2)
step1Button['font'] = buttonFont
step1Button.grid(row = 0, column = 6, columnspan = 3, padx = (25, 5), pady = 10)

window.mainloop()