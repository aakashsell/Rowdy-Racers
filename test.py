from tkinter import *
import random

root = Tk()

canvas = Canvas(root, bg='white', width=1600, height=800)
canvas.pack(fill=BOTH, expand=1)

y_array = random.randint(100, 700, 5000) 

x_start = 3
x_stop = 5000
step = 1.3

# create the array of points and draw them
line_array = [(n*step, y_array[n]) for n in range(x_start, x_stop)]
canvas.create_line(line_array)

root.mainloop()