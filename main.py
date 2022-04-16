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
    canvas.create_text(app.width/2, app.height*(1/4), text="Welcome To Rowdy Racers",
                        fill="black", font="comic-sans")
    canvas.create_rectangle(app.width/2 + 100, app.height*(2/4) + 50,
                            app.width/2 - 100, app.height*(2/4) - 50,
                            fill='orange')
    canvas.create_rectangle(app.width/2 + 100, app.height*(3/4) + 50,
                            app.width/2 - 100, app.height*(3/4) - 50,
                            fill='orange')
    canvas.create_text(app.width/2, app.height*(2/4), text='Start (s)', fill='black')
    canvas.create_text(app.width/2, app.height*(3/4), text='Build (b)', fill='black')

def startScreenMode_keyPressed(app, event):
    if event.key.lower() == "s":
        app.mode = "gameMode"
    if event.key.lower() == "b":
        app.mode = "courseBuilderMode"

def startScreenMode_mousePressed(app, event):
    print(f"{event.x}, {event.y}")
    if (event.x > app.width/2 - 100 and event.x < app.width/2 + 100 and
        event.y > app.height*(2/4) - 50 and event.y < app.height*(2/4) + 50):
        app.mode = 'gameMode'
    if (event.x > app.width/2 - 100 and event.x < app.width/2 + 100 and
        event.y > app.height*(3/4) - 50 and event.y < app.height*(3/4) + 50):
        app.mode = 'courseBuilderMode'
    pass

##########################################
# Game Mode
##########################################

def checkCarCollions():
    pass

class Car:
    def __init__(self, width, center):
        self.racing = False
        self.width = width
        self.height = width * 2
        self.x = center[0]
        self.y = center[1]
        self.carColors = ["red", "blue", "green", "orange", "purple", "teal", "yellow"]
        self.randColor = random.randint(0,len(self.carColors) - 1)
        self.color = self.carColors[self.randColor]
        self.angle = 0
        self.ogCoords = self.getCoords()
        self.coords = self.getCoords()
        self.lives = 3
    
    def checkOnRoad(self, app):
        for x in self.getCoords():
            if (x[0] < app.width/2 - app.track.width/2
                or x[0] > app.width/2 + app.track.width/2):
                return False
        return True

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

    def move(self, speed, app, type):
        radians = math.radians(self.angle)
        if type == "all":
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
        canvas.create_oval(self.x - 2, self.y - 2, self.x + 2, self.y + 2,
                            fill="white")

class AICar(Car):
    def race(self, app):
        self.racing = True
        if app.player.x <= self.x:
            self.x -= 100

    def draw(self, canvas):
        top_left = self.coords[0]
        top_right = self.coords[1]
        bottom_right = self.coords[2]
        bottom_left = self.coords[3]
        canvas.create_polygon(top_left[0], top_left[1], top_right[0], top_right[1],
                            bottom_right[0], bottom_right[1], 
                            bottom_left[0], bottom_left[1], fill=self.color)
    
class Track():
    def __init__(self, app, type, road_color, background_color, coords, width):
        self.type = type
        self.road = road_color
        self.background = background_color
        self.length = len(coords)
        self.width = width
        # self.top_corner = [0, app.height - self.length]
        self.bottom_corner = [app.width, app.height]
        self.coords = self.convertCoords(app, coords)
        pass

    def convertCoords(self, app, coords):
        if app.customHeight == None:
            pass
        else:
            newCoords = []
            i = 0
            while i < len(coords) - 1:
                x = (((abs((app.width/app.customHeight)/2) -
                    abs(coords[0] - app.width/2))/(app.width/app.customHeight))
                    * app.width)
                print(x)
                y = coords[i+1]
                newCoords.append(x)
                newCoords.append(y)
                i += 2
            return newCoords
        return coords
    
    def end(self, app):
        if self.coords[len(self.coords) - 1] > app.height/2:
            return False
        else:
            return True

    def generate(self, list):
        pass

    def moveCoords(self, app):
        i = 1
        while i < len(self.coords):
            self.coords[i] += app.scrollY
            i += 2

    def draw(self, app, canvas):
        canvas.create_rectangle(0, app.height - self.length + app.scrollY,
                                 app.width, app.height, 
                                fill= self.background)
        canvas.create_line(self.coords, width=self.width)
        canvas.create_line(self.coords, fill="yellow", dash=(5,5), width=self.width/50)


def gameMode_redrawAll(app, canvas):
    app.track.draw(app, canvas)
    app.player.draw(canvas)
    app.ai.draw(canvas)

def gameMode_keyPressed(app, event):
    if event.key == "Right":
        app.player.rotate(-15)
        app.player
    if event.key == "Left":
        app.player.rotate(15)
    if event.key.lower() == "p":
        app.mode = 'startScreenMode'
    if event.key == "Up":
        app.scrollY += 30
    if event.key == "Down":
        app.player.move(-20, app)
    pass

def gameMode_timerFired(app):
    app.ai.race(app)
    app.player.move(20, app, None)
    app.track.moveCoords(app)
    if not app.track.end(app):
        app.scrollY += 8
    if not app.player.checkOnRoad(app):
        app.player.life -= 1
        print("Crash")

##########################################
# Course Builder
##########################################

def checkErrors(app):
    x = []
    y = []
    i = 0
    while i <len(app.tempTrack) - 1:
        x.append(app.tempTrack[i])
        y.append(app.tempTrack[i+1])
        i += 2
    for k in range(len(y) - 1):
        if y[k] < y[k+1]:
            return True
    return False

def courseBuilderMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill="green")
    if app.customHeight != None:
        canvas.create_rectangle(app.width/2 + app.incWidth, 0, app.width/2 - app.incWidth
                                , app.height, fill='beige')
        if len(app.tempTrack) > 3:
            canvas.create_line(app.tempTrack, width=app.tempLineWidth)
            canvas.create_line(app.tempTrack, fill="yellow")

def courseBuilderMode_mousePressed(app, event):
    if (event.x > app.width/2 - app.incWidth and
         event.x < app.width/2 + app.incWidth):
        print(event.x, event.y)
        app.tempTrack.append(event.x)
        app.tempTrack.append(event.y)
        if checkErrors(app):     
            app.tempTrack = []
            app.message = 'This track is invalid, try again'

def courseBuilderMode_keyPressed(app, event):
    if event.key == "Up":
        app.tempLineWidth += 5
    if event.key == "Down":
        app.tempLineWidth -= 5
    if event.key.lower() == "s":
        app.mode = "startScreenMode"

def courseBuilderMode_timerFired(app):
    if app.customHeight == None:
        app.customHeight = app.getUserInput("How tall Do you want this track in terms of height multiplier")
    else:
        app.customHeight = int(app.customHeight)
        app.totWidth = app.width / app.customHeight
        app.incWidth = app.totWidth/2
    pass

##########################################
# Main App
##########################################

def genStraightTrack(app):
    trackCoords = []
    width = app.width/2
    for i in range(-app.height*10, 0):
        trackCoords.append(width)
        trackCoords.append(i)
    for i in range(app.height):
        trackCoords.append(width)
        trackCoords.append(i)
    return trackCoords

def appStarted(app):
    app.scrollX = 0
    app.scrollY = 0
    app.mode = 'startScreenMode'
    app.carX = app.width / 2
    app.carY = app.height / 2
    app.carWidth = 10
    app.customHeight = None
    app.tempLineWidth = 20
    app.numAI = 0
    app.totWidth = 0
    app.incWidth = 0
    app.player = Car(app.carWidth, [app.carX, app.carY])
    app.ai = AICar(app.carWidth, [app.carX - 30, app.carY])
    app.testTrack = genStraightTrack(app)
    app.tracks = []
    app.tempTrack = []
    app.track = Track(app, "test", "blue", "light blue", app.testTrack, 200)

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

runApp(width=800, height=600, title="Rowdy Racers")

