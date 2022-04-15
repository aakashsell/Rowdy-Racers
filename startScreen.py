from cmu_112_graphics import *
import math, copy, os, random
import main
import pygame #Used for Sound

##########################################
# Start Screen Mode
##########################################

def startScreenMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='green')
    canvas.create_text(app.width/2, app.height/2, text="press S to start",
                        fill="black", font="comic-sans")
    canvas.create_rectangle(app.width/2 + 100, app.height*(2/3) + 50,
                            app.width/2 - 100, app.height*2/3 - 50,
                            fill='orange')
    canvas.create_text(app.width/2, app.height*(2/3), text='start', fill='black')
    # canvas.create_rectangle()

def startScreenMode_keyPressed(app, event):
    if event.key.lower() == "s":
        app.mode = 'gameMode'

def startScreenMode_mousePressed(app, event):
    print(f"{event.x}, {event.y}")
    if (event.x > app.width/2 - 100 and event.x < app.width/2 + 100 and
        event.y > app.height*(2/3) - 50 and event.y < app.height*(2/3) + 50):
        app.mode = 'gameMode'
    pass