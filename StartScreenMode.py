##########################################
# Start Screen Mode
##########################################

from cmu_112_graphics import *
from GameMode import *
from StartScreenMode import *
import math, copy, os, random
import pygame #Used for Sound

class StartScreenMode():

    def __init(self, app, cvna):
        self.app = app

    def redrawAll(app, canvas):
        canvas.create_rectangle(0, 0, app.width, app.height, fill='green')
        canvas.create_text(app.width/2, app.height/2, text="press S to start",
                            fill="black", font="comic-sans")
        canvas.create_rectangle(app.width/2 + 100, app.height*(2/3) + 50,
                                app.width/2 - 100, app.height*2/3 - 50,
                                fill='orange')
        canvas.create_text(app.width/2, app.height*(2/3), text='start', fill='black')
        # canvas.create_rectangle()

    def keyPressed(app, event):
        if event.key.lower() == "s":
            app.mode = 'gameMode'

    def mousePressed(app, event):
        print(f"{event.x}, {event.y}")
        if (event.x > app.width/2 - 100 and event.x < app.width/2 + 100 and
            event.y > app.height*(2/3) - 50 and event.y < app.height*(2/3) + 50):
            app.mode = 'gameMode'
        
