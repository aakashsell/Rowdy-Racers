#################################################
# Term Project - Main Function
#
# Your name: Aakash Sell
# Your andrew id: asell
#################################################

from cmu_112_graphics import *
import math, copy, os, random
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

##########################################
# Game Mode
##########################################

class Car:
    def __init__(self, width, color, center):
        self.width = width
        self.height = width * 2
        self.x = center[0]
        self.y = center[1]
        self.color = color
        self.angle = 0
        self.ogCoords = self.getCoords()
        self.coords = self.getCoords()

    def getBounds(app):
        pass

    def getCoords(self):
        top_left = [self.x - self.width, self.y - self.height]
        top_right = [self.x + self.width, self.y - self.height]
        bottom_right = [self.x + self.width, self.y + self.height]
        bottom_left = [self.x - self.width, self.y + self.height]
        return [top_left, top_right, bottom_right, bottom_left]

    def rotate(self, angle):
        newCoords = []
        self.angle += angle
        for coord in self.ogCoords:
            radian = math.radians(self.angle)
            tempX = coord[0] - self.x
            tempY = coord[1] - self.y
            newX = tempX*math.cos(radian) + tempY*math.sin(radian)
            newY = tempY*math.cos(radian) - tempX*math.sin(radian)
            newCoords.append([newX + self.x, newY + self.y])
        self.coords = newCoords

    def move(self, speed, app):
        radians = math.radians(self.angle)
        self.y -= speed*math.cos(radians)
        self.x -= speed*math.sin(radians)
        self.ogCoords = self.getCoords()
        self.rotate(0)
        for coord in self.coords:
            if (coord[0] < 0 or coord[0] > app.width or coord[1] < 0 or 
                                                    coord[1] > app.height):
                self.y += speed*math.cos(radians)
                self.x += speed*math.sin(radians)
                self.ogCoords = self.getCoords()
                self.rotate(0)
                break

    def reset(self):
        self = Car()

    def draw(self, canvas):
        top_left = self.coords[0]
        top_right = self.coords[1]
        bottom_right = self.coords[2]
        bottom_left = self.coords[3]
        canvas.create_polygon(top_left[0], top_left[1], top_right[0], top_right[1],
                            bottom_right[0], bottom_right[1], 
                            bottom_left[0], bottom_left[1], fill=self.color)

class AICar(Car):
    def __init__(self):
        pass

class Track():
    def __init__(self, app, type, road_color, background_color, length):
        self.type = type
        self.road = road_color
        self.background = background_color
        self.length = length
        self.top_corner = [0, app.height - length]
        self.bottom_corner = [app.width, app.height]
        pass

    def generate(self, list):
        pass

    def draw(self, app, canvas):

        canvas.create_rectangle(0, -100 - app.scrollY, app.width, app.height, fill= self.background)
        pass

def gameMode_redrawAll(app, canvas):
    app.track.draw(app, canvas)
    app.player.draw(canvas)

def gameMode_keyPressed(app, event):
    if event.key == "Right":
        app.player.rotate(-15)
    if event.key == "Left":
        app.player.rotate(15)
    if event.key.lower() == "p":
        app.mode = 'startScreenMode'
    if event.key == "Up":
        app.player.move(20, app)
    if event.key == "Down":
        app.player.move(-20, app)
    pass

def gameMode_timerFired(app):
    app.scrollY -= 10
    pass

##########################################
# Course Buider
##########################################

##########################################
# Main App
##########################################

def appStarted(app):
    app.scrollX = 0
    app.scrollY = 0
    app.mode = 'startScreenMode'
    app.carColors = ["red", "blue", "green", "orange", "purple", "teal", "yellow"]
    app.carX = app.width / 2
    app.carY = app.height / 2
    app.carWidth = 10
    app.color = random.randint(0,len(app.carColors) - 1)
    app.player = Car(app.carWidth, app.carColors[app.color], [app.carX, app.carY])
    app.track = Track(app, "test", "blue", "teal", 1000)

def mousePressed(app, event):
    x, y = event.x, event.y
    if len(app.track) < 4:
        app.track.append([x, y])
    else:
        app.track.pop(0)
        app.track.pop(1)

def drawStartScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width,
                     app.height, fill='black')
    canvas.create_text(app.width/2, app.height/2,text="Hello", fill='red')



runApp(width=800, height=600)

