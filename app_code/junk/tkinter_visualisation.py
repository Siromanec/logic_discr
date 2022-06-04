from __future__ import annotations
from tkinter import *


import ctypes
# root = Tk()
# myCanvas = Canvas(root)
# myCanvas.pack()

# def create_circle(x, y, r, canvasName: Canvas): #center coordinates, radius
#     x0 = x - r
#     y0 = y - r
#     x1 = x + r
#     y1 = y + r
#     canvasName.event_add()
#     return canvasName.create_oval(x0, y0, x1, y1)

# create_circle(100, 100, 20, myCanvas)
# create_circle(50, 25, 10, myCanvas)
# root.mainloop()
class GPin():
    """
    graphical pin
    """
    all_accessible_areas = []
    def __init__(self, center, canvas: Canvas) -> None:
        """
        :param tuple[int] center:
        :param Canvas canvas:

        """
        self.size = 8
        self.canvas = canvas
        self.center = center
        self.reaction_area = (center[0] - self.size, center[1] - self.size, center[0] + self.size, center[1] + self.size)
        self.draw()
        self.add_area(self)
    def check(self, inp):
        return self.reaction_area[0] < inp[0] < self.reaction_area[2] and self.reaction_area[1] < inp[1] < self.reaction_area[3]
    def draw(self):
        self.canvas.create_oval(self.reaction_area)
    def __repr__(self) -> str:
         return "(" + str(self.reaction_area) + "|" + str(self.center) + ")"
    @classmethod
    def add_area(cls, self):
        cls.all_accessible_areas.append(self)
class Line():
    """
    connects pins
    for some reaseon i use it just as a function
    ah. the line will have some other methods later
    """
    def __init__(self, inp, canvas: Canvas) -> None:
        #if in global pins theese coords execute connect abd center to pins
        self.canvas = canvas
        access = GPin.all_accessible_areas
        for gpin_start in access:
            for gpin_end in access:
                if gpin_start.check(inp[:2]) and gpin_end.check(inp[2:]):
                    adj_inp = gpin_start.center + gpin_end.center
                    # print(access)
                    # print(adj_inp, gpin_start.center, gpin_end.center, inp)
                    self.canvas.create_line(adj_inp[0], adj_inp[3], adj_inp[2], adj_inp[3], width=2, fill="black")
                    self.canvas.create_line(adj_inp[0], adj_inp[1], adj_inp[0], adj_inp[3], width=2, fill="black")

        
root = Tk()
coords = []

def key(event):
    print( "pressed", repr(event.char))

def connect(event):
    print ("clicked at", event.x, event.y)
    coords.append(event.x)
    coords.append(event.y)
    if len(coords) == 4:
        Line(coords, canvas)
        coords.clear()
        
def add_square(event):
    size = 18
    coords.append(event.x)
    coords.append(event.y)
    canvas.create_rectangle(coords[0] - size, coords[1] - size, coords[0] + size, coords[1] + size)
    coords.clear()

def add_circle(event):
    size = 18
    coords.append(event.x)
    coords.append(event.y)
    canvas.create_oval(coords[0] - size, coords[1] - size, coords[0] + size, coords[1] + size)
    coords.clear()

def add_pin(event):

    GPin(((event.x, event.y)), canvas)

 
ctypes.windll.shcore.SetProcessDpiAwareness(1)
canvas= Canvas(root, width=512, height=512)
#root.tk.call('tk', 'scaling', 2.0)
canvas.bind("<Key>", key)
print(coords)

#canvas.bind("<Button-1>", connect)

def current_command_connect():
    coords.clear()

    canvas.bind("<Button-1>", connect)
def current_command_square():
    coords.clear()

    canvas.bind("<Button-1>", add_square)

def current_command_circle():
    coords.clear()

    canvas.bind("<Button-1>", add_circle)
def current_command_pin():
    coords.clear()

    canvas.bind("<Button-1>", add_pin)
# def export_win():

#     orig_color = button1.cget("background")
#     button1.configure(background = "green")

#     tt = "Exported"
#     label = Label(root, text=tt, font=("Helvetica", 12))
#     label.grid(row=0,column=0,padx=10,pady=5,columnspan=3)

#     def change(orig_color):
#         button1.configure(background = orig_color)

#     root.after(1000, lambda: change(orig_color))
#     root.after(500, label.destroy)
button1 = Button(text = "connect", command = current_command_connect, anchor = W)
button1.configure(width = 10, activebackground = "#33B5E5", relief = SOLID,)
button1_window = canvas.create_window(10, 10, anchor=NW, window=button1)

button2 = Button(text = "square", command = current_command_square, anchor = W)
button2.configure(width = 10, activebackground = "#33B5E5", relief = SOLID)
button2_window = canvas.create_window(10, 40, anchor=NW, window=button2)

button3 = Button(text = "circle", command = current_command_circle, anchor = W)
button3.configure(width = 10, activebackground = "#33B5E5", relief = SOLID)
button3_window = canvas.create_window(10, 70, anchor=NW, window=button3)


button4 = Button(text = "add pin", command = current_command_pin, anchor = W)
button4.configure(width = 10, activebackground = "#33B5E5", relief = SOLID)
button4_window = canvas.create_window(10, 100, anchor=NW, window=button4)

canvas.pack()



root.mainloop()