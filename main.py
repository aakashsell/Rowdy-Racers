#################################################
# Term Project - Main Function
#
# Your name: Aakash Sell
# Your andrew id: asell
#################################################

from http.cookiejar import FileCookieJar
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

def startScreenMode_timerFired(app):
    resetGame(app)

##########################################
# Instructions Mode
##########################################



##########################################
# Game Mode
##########################################

def resetGame(app):
    app.player.reset()
    app.ai.reset()
    app.scrollY = 0
    app.finish = False

def endGameConditions(app):
    if not(app.player.onScreen(app) or app.ai.onScreen(app)):
        return True
    return False

def checkCarCollions(app):
    playerCoords = app.player.getCoords()
    aiCoords = app.ai.getCoords()
    # top left, top right, bootom right, bottom left
    #Check if a point of the player is in the ai
    if app.player.x > app.ai.x:
        right = app.player
        left = app.ai
    else:
        right = app.ai
        left = app.player
    for coord in playerCoords:
        pass
    pass

def checkWins(app):
    if app.ai.y < app.player.y:
        return "ai"
    else:
        return "player"

class Car:
    def __init__(self, app, width, center):
        self.boosts = 3
        self.racing = False
        self.width = width
        self.height = width * 2
        self.startX = center[0]
        self.startY = center[1]
        self.y = center[1]
        self.x = app.track.getCenterForY(app, self.y)
        self.carColors = ["red", "blue", "green", "orange", "purple", "teal", "yellow"]
        self.randColor = random.randint(0,len(self.carColors) - 1)
        self.color = self.carColors[self.randColor]
        self.angle = 0
        self.ogCoords = self.getCoords()
        self.coords = self.getCoords()
        self.lives = 3
        self.speedMod = 0
        self.xSpeed = 0

    def onScreen(self, app):
        if (self.x > app.width or self.x < 0 or app.y < 0 or app.y > app.height):
            return False
        return True

    def boost(self, app):
        if self.boosts > 0:
            self.move(20, app, "all")
            self.boosts -= 1
    
    def checkOnRoad(self, app):
        xCenter = app.track.getCenterForY(app, self.y)
        radius = app.track.width / 2
        leftBound = xCenter - radius
        rightBound = xCenter + radius
        if self.x > rightBound or self.x < leftBound:
                app.player.y += 10
                return False
        return True

    def physics(self, app):
        self.checkOnRoad(app)

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
        speed += self.speedMod
        self.x -= speed*math.sin(radians)
        self.xSpeed = speed*math.sin(radians)
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
        self.x = self.startX
        self.y = self.startY
        self.angle = 0

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

    def finish(self, app):
        while self.y > 20:
            self.y -= 10
        app.finish = True

class AICar(Car):
    def race(self, app):
        self.racing = True
        if app.player.y <= self.y:
            self.boost(app)
        trackCenter = app.track.getCenterForY(app, self.y)
        distanceCenter = abs(trackCenter - self.x)
        if self.x != trackCenter:
            if self.x < trackCenter:
                self.rotate(-distanceCenter * .2)
            else:
                self.rotate(distanceCenter * .2)

    def draw(self, canvas):
        top_left = self.coords[0]
        top_right = self.coords[1]
        bottom_right = self.coords[2]
        bottom_left = self.coords[3]
        canvas.create_polygon(top_left[0], top_left[1], top_right[0], top_right[1],
                            bottom_right[0], bottom_right[1], 
                            bottom_left[0], bottom_left[1], fill=self.color)
    
class Track():
    def __init__(self, app, type, road_color, background_color, inputCoords, width):
        self.ogCoords = inputCoords
        self.type = type
        self.road = road_color
        self.background = background_color
        self.length = len(inputCoords)
        self.width = width
        self.obstacles = []
        if len(inputCoords) > 2:
            self.coords = inputCoords
        else:
            self.coords = generateTrack(app)
            app.infinite = True
        pass

    def reset(self, app):
        app.track = Track(app, "test", "blue", "light blue", app.testTrack, 200)

    def convertCoords(self, app, coords):
        if app.customHeight != None:
            tempCoords = coords
            newCoords = []
            i = 0
            startX = tempCoords[0]
            tempCoords.insert(0, app.height)
            tempCoords.insert(0, startX)
            while i < (len(tempCoords) - 1): 
                mid = app.width/app.customHeight
                x = ((tempCoords[i] - (app.width/2 - mid/2))/mid)*app.width
                if i != 0:
                    distance = abs(abs(tempCoords[i-1])
                                 - abs(tempCoords[i+1]))
                    totDistance = distance * app.customHeight
                    y = tempCoords[i-1] - totDistance
                else:
                    y = tempCoords[i+1] 
                newCoords.append(x)
                newCoords.append(y)
                i += 2
            return newCoords
        return coords

    def obstacle(self, app):
        pass
    
    def getCenterForY(self, app, y):
        i = 1
        while i < len(self.coords):
            if self.coords[i] > y > self.coords[i+2]:
                diff = abs(y - self.coords[i])
                prop = diff / abs(self.coords[i] - self.coords[i+2])
                length = abs(self.coords[i-1] - self.coords[i+1])
                away = prop * length
                if self.coords[i-1] > self.coords[i+1]:
                    return self.coords[i-1] + away
                else:
                    return self.coords[i-1] - away
            i += 4
        return app.width / 2

    def end(self, app):
        if self.coords[len(self.coords) - 1] > app.height/3:
            return True
        else:
            return False

    def moveCoords(self, app):
        i = 1
        while i < len(self.coords):
            self.coords[i] += app.scrollY
            i += 2

    def drawObstacle(self, app, canvas):
        num = random.randint(0, 10)
        
        pass

    def draw(self, app, canvas):
        canvas.create_rectangle(0, 0,
                                 app.width, app.height, 
                                fill= self.background)
        canvas.create_line(self.coords, width=self.width)
        canvas.create_line(self.coords, fill="yellow", dash=(5,5), width=self.width/50)
        self.drawObstacle(app, canvas)
    
def genNextPoint(app):
    if app.track.coords[3] >= app.height:
        app.track.coords.pop(0)
        app.track.coords.pop(0)
    startX = app.track.coords[len(app.track.coords) - 2]
    startY = app.track.coords[len(app.track.coords) - 1]
    run = True
    count = 0
    while run:
        direction = 0
        if startX < app.width/2:
            direction = 1
        length = random.randint(1,30)
        length = 20 * length
        angle = random.randint(1, 15)
        angle = angle * 8
        angle = math.radians(angle)
        xChange = length * math.cos(angle)
        yChange = length * abs(math.sin(angle))
        if direction == 0:
            xChange = 0 - xChange
        newX = startX + xChange
        newY = startY - yChange 
        if (newX > 100 and newX < app.width - 100 
            and newY < 0):
            app.track.coords.append(newX)
            app.track.coords.append(newY)
            run = False
        

def generateTrack(app):
    run = True
    track = [app.width/2, app.height]
    startX = app.width/2
    startY = app.height/2
    track.append(startX)
    track.append(startY)
    count = 0 
    while run:
        direction = random.randint(0,1)
        length = random.randint(1,10)
        length = 80 * length
        angle = random.randint(1,15)
        angle = angle * 4
        angle = math.radians(angle)
        xChange = length * math.cos(angle)
        yChange = length * abs(math.sin(angle))
        if direction == 0:
            xChange = 0 - xChange
        newX = startX + xChange
        newY = startY - yChange
        if (newX > 0 + 100 and newX < app.width - 100 
            and newY > 0 and newY < app.height):
            track.append(newX)
            track.append(newY)
            startX = newX
            startY = newY
            if newY < 10:
                run = False
        else:
            count += 1
        if count == 3:
            count = 0
            if len(track) > 4:
                track.pop()
                track.pop()
                startX = track[len(track) - 2]
                startY = track[len(track) - 1]
    return track

def drawFinish(app, canvas):
    if app.track.end(app):
        app.showMessage(f"{app.winner} wins!")
    pass

def gameMode_redrawAll(app, canvas):
    drawFinish(app, canvas)
    app.track.draw(app, canvas)
    app.player.draw(canvas)
    app.ai.draw(canvas)
    if app.finish:
        drawFinish(app, canvas, checkWins(app))

def gameMode_keyPressed(app, event):
    universalCommands(app, event)
    if event.key == "Right":
        app.player.rotate(-15)
    if event.key == "Left":
        app.player.rotate(15)
    if event.key == "Up":
        app.player.boost(app)
    if event.key == "Down":
        app.player.move(-20, app, "all")
    if app.players > 1:
        if event.key.lower() == "d":
            app.ai.rotate(-15)
        if event.keylower() == "a":
            app.ai.rotate(15)
        if event.keylower() == "w":
            app.ai.move(20, app, "all")
        if event.keylower() == "s":
            app.ai.move(-20, app, "all")

def gameFinish(app):
        if app.player.y > 100:
            app.player.y -= 10
        if app.ai.y > 100:
            app.ai.y -= 10

def movingMod(app):
    if checkCarCollions(app):
        pSpeed = app.player.xSpeed
        aiSpeed = app.ai.xSpeed
        app.player.speedMod = pSpeed - aiSpeed
        app.ai.speedMod = aiSpeed - pSpeed

def gameMode_timerFired(app):
    if len(app.tempTrack) > 2:
        app.track = Track(app, "test", "blue", "light blue", app.tempTrack, 200)
        app.track.coords = app.track.convertCoords(app, app.track.ogCoords)
        app.infinite = False
    if app.track.coords[len(app.track.coords) - 1] > -100 and app.infinite:
        genNextPoint(app)
    movingMod(app)
    app.ai.race(app)
    app.player.move(20, app, None)
    app.ai.move(20, app, None)
    app.track.moveCoords(app)
    if not app.track.end(app) and app.infinite:
        app.scrollY += 0.1
    elif not app.track.end(app):
        app.scrollY += 5
    else:
        app.scrollY = 0
        gameFinish(app)
    if app.infinite:
        pass
    app.player.physics(app)
    app.ai.physics(app)
        
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
            app.showMessage(app.message)

def courseBuilderMode_keyPressed(app, event):
    universalCommands(app, event)
    if event.key == "Up":
        app.tempLineWidth += 5
    if event.key == "Down":
        app.tempLineWidth -= 5

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
    for i in range(0-(app.height*10), 1):
        trackCoords.append(width)
        trackCoords.append(i)
    for i in range(app.height):
        trackCoords.append(width)
        trackCoords.append(i)
    return trackCoords

def universalCommands(app, event):
    if event.key.lower() == 'p':
        app.mode = 'startScreenMode'

def appStarted(app):
    app.players = 1
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
    app.testTrack = genStraightTrack(app)
    app.tracks = []
    app.tempTrack = []
    app.track = Track(app, "test", "blue", "light blue", app.tempTrack, 200)
    app.player = Car(app, app.carWidth, [app.carX, app.carY])
    app.ai = AICar(app, app.carWidth, [app.carX - 30, app.carY])
    app.finish = False
    app.infinite = True
    app.winnder = ""

def drawStartScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width,
                     app.height, fill='black')
    canvas.create_text(app.width/2, app.height/2,text="Hello", fill='red')

runApp(width=800, height=600, title="Rowdy Racers")

