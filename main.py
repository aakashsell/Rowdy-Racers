#################################################
# Term Project - Main Function
#
# This is the main file for the project and all of the code is in here.
#
# Your name: Aakash Sell
# Your andrew id: asell
#################################################

from cmu_112_graphics import *
import math, random
import pygame #Used for Sound

##########################################
# Start Screen Mode
# Taken from 112 lecture notes
# Free Music From Youtube: https://www.youtube.com/watch?v=o4PioBdZppc
##########################################

class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=-1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()

##########################################
# Start Screen Mode
# This screen is the heart of the game and directs the user to 
# other parts of the game.
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
    canvas.create_rectangle(app.width*(2/3) + 25, app.height*(2/4) + 25,
                            app.width*(2/3) - 25, app.height*(2/4) - 25,
                            fill='blue')        
    canvas.create_rectangle(app.width*(9/10) + 25, app.height*(9/10) + 25,
                            app.width*(9/10) - 25, app.height*(9/10) - 25,
                            fill='yellow')
    canvas.create_text(app.width/2, app.height*(2/4), text='Start (s)', fill='black')
    canvas.create_text(app.width*(2/3), app.height*(2/4), text='2P', fill='black')
    canvas.create_text(app.width/2, app.height*(3/4), text='Build (b)', fill='black')
    canvas.create_text(app.width*(9/10), app.height*(9/10), text='I', fill='black')

def startScreenMode_keyPressed(app, event):
    if event.key.lower() == "s":
        app.mode = "gameMode"
    if event.key.lower() == "b":
        app.mode = "courseBuilderMode"
    if event.key.lower() == "2":
        app.players = 2
        app.mode = "gameMode"
    if event.key.lower() == "i":
        app.mode = "instructionsMode"

def startScreenMode_mousePressed(app, event):
    if (event.x > app.width/2 - 100 and event.x < app.width/2 + 100 and
        event.y > app.height*(2/4) - 50 and event.y < app.height*(2/4) + 50):
        app.players = 1
        app.mode = 'gameMode'
    if (event.x > app.width/2 - 100 and event.x < app.width/2 + 100 and
        event.y > app.height*(3/4) - 50 and event.y < app.height*(3/4) + 50):
        app.mode = 'courseBuilderMode'
    if (event.x > app.width*(2/3) - 25 and event.x < app.width*(2/3) + 25 and
        event.y > app.height*(2/4) - 25 and event.y < app.height*(2/4) + 25):
        app.players = 2
        app.mode = 'gameMode'
    if (event.x > app.width*(9/10) - 25 and event.x < app.width*(9/10) + 25 and
        event.y > app.height*(9/10) - 25 and event.y < app.height*(9/10) + 25):
        app.mode = 'instructionsMode'
    pass

def startScreenMode_timerFired(app):
    try:
        if not app.sound.isPlaying():
            pygame.mixer.init()
            app.sound = Sound('splash.mp3')
            app.sound.start()
    except:
        pygame.mixer.init()
        app.sound = Sound('splash.mp3')
        app.sound.start()
    resetGame(app)

##########################################
# Instructions Mode
# This screen is just text that explains to the user how to play the game.
##########################################

def instructionsMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='yellow')
    instructionsText = ["To play rowdy racers, you just need to press start.",
                        "This will have you play against Ai on an infite randomly generated track.",
                        "To activate 2 player mode just press the 2 key and the second player can use wasd.",
                        "You can also draw your own map and play on that."
                        " Press p at any time to go back to the main screen."]
    canvas.create_text(app.width/2, app.height*(1/5), text=instructionsText[0], fill='black')
    canvas.create_text(app.width/2, app.height*(2/5), text=instructionsText[1], fill='black')
    canvas.create_text(app.width/2, app.height*(3/5), text=instructionsText[2], fill='black')
    canvas.create_text(app.width/2, app.height*(4/5), text=instructionsText[3], fill='black')
    canvas.create_rectangle(app.width*(1/10) + 50, app.height*(1/10) + 25,
                            app.width*(1/10) - 50, app.height*(1/10) - 25,
                            fill='green')
    canvas.create_text(app.width*(1/10), app.height*(1/10), text="Back", fill='black')

def instructionsMode_keyPressed(app, event):
    if event.key.lower() == "p":
        app.mode = "startScreenMode"

def instructionsMode_mousePressed(app, event):
    if (event.x > app.width*(1/10) - 50 and event.x < app.width*(1/10) + 50 and
        event.y > app.height*(1/10) - 25 and event.y < app.height*(1/10) + 25):
        app.mode = 'startScreenMode'

##########################################
# Game Mode
# This screen actually runs the game and contains all of the game mechanics.
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
    xDiff = abs(app.player.x - app.ai.x)
    yDiff = abs(app.player.y - app.ai.y)
    distance = ((xDiff ** 2) + (yDiff ** 2))**.5
    if distance < app.player.width:
        print("crash")
        return True
    return False

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
        radius = app.track.width/2
        leftBound = xCenter - radius
        rightBound = xCenter + radius
        if self.x > rightBound or self.x < leftBound:
                self.y += 10

    def checkHitObstacle(self, app):
        i = 0
        while i < len(app.track.coords):
            xDiff = app.track.coords[i] - self.x
            yDiff = app.track.coords[i+1] - self.y
            distance = ((xDiff**2) + (yDiff**2))**.5
            if distance < 20:   
                self.y += 10
            i+=2

    def physics(self, app):
        self.checkOnRoad(app)
        self.checkHitObstacle(app)

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
            if self.x < trackCenter and self.angle > -90:
                self.rotate(-distanceCenter * .2)
            elif self.x > trackCenter and self.angle < 90:
                self.rotate(distanceCenter * .2)

    def draw(self, canvas):
        top_left = self.coords[0]
        top_right = self.coords[1]
        bottom_right = self.coords[2]
        bottom_left = self.coords[3]
        canvas.create_polygon(top_left[0], top_left[1], top_right[0], top_right[1],
                            bottom_right[0], bottom_right[1], 
                            bottom_left[0], bottom_left[1], fill=self.color)
        canvas.create_oval(self.x - 2, self.y - 2, self.x + 2, self.y + 2,
                            fill="black")
    
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
    
    def getCenterForY(self, app, y):
        i = 1
        while i < len(self.coords):
            if self.coords[i] > y > self.coords[i+2]:
                diff = abs(y - self.coords[i])
                prop = diff / abs(self.coords[i] - self.coords[i+2])
                length = abs(self.coords[i-1] - self.coords[i+1])
                away = prop * length
                if self.coords[i-1] > self.coords[i+1]:
                    return self.coords[i-1] - away
                else:
                    return self.coords[i-1] + away
            i += 2
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
        i = 4
        while i < len(self.coords): 
            oX = self.coords[i]
            oY = self.coords[i+1]
            canvas.create_oval(oX - 10, oY - 10, oX + 10, oY + 10,
                            fill="red")
            i += 2

    def draw(self, app, canvas):
        canvas.create_rectangle(0, 0,
                                 app.width, app.height, 
                                fill= self.background)
        canvas.create_line(self.coords, width=self.width)
        canvas.create_line(self.coords, fill="yellow", dash=(5,5), width=self.width/50)
        self.drawObstacle(app, canvas)
    
def genNextPoint(app):
    # Used drunk man's walk algorithm
    # Inspired by this article : https://medium.com/i-math/the-drunkards-walk-explained-48a0205d304
    if app.track.coords[3] >= app.height:
        app.track.coords.pop(0)
        app.track.coords.pop(0)
    startX = app.track.coords[len(app.track.coords) - 2]
    startY = app.track.coords[len(app.track.coords) - 1]
    run = True
    while run:
        direction = 0
        if startX < app.width/2:
            direction = 1
        length = random.randint(1,30)
        length = 20 * length
        angle = random.randint(10, 15)
        angle = angle * 4
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
    # Used drunk man's walk algorithm
    # Inspired by this article : https://medium.com/i-math/the-drunkards-walk-explained-48a0205d304
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
        angle = random.randint(10,15)
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

def gameMode_redrawAll(app, canvas):
    app.track.draw(app, canvas)
    app.player.draw(canvas)
    app.ai.draw(canvas)

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
        if event.key.lower() == "a":
            app.ai.rotate(15)
        if event.key.lower() == "w":
            app.ai.move(20, app, "all")
        if event.key.lower() == "s":
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

def checkEnd(app):
    if app.player.y > app.height:
        app.winner = "AI" 
    elif app.ai.y > app.height:
        app.winner = "Player" 
    if app.winner != "":
        app.showMessage(f"{app.winner} wins!")
        app.winner = ""
        app.mode = 'startScreenMode'
    

def gameMode_timerFired(app):
    if app.infinite == False and app.centerCarCount == 0:
        app.player.x = app.track.getCenterForY(app, app.height/2)
        app.ai.x = app.track.getCenterForY(app, app.height/2)
        app.centerCarCount = 1
    if len(app.tempTrack) > 2:
        app.track = Track(app, "test", "blue", "light blue", app.tempTrack, 200)
        app.track.coords = app.track.convertCoords(app, app.track.ogCoords)
        app.infinite = False
    if app.track.coords[len(app.track.coords) - 1] > -100 and app.infinite:
        genNextPoint(app)
    movingMod(app)
    if app.players == 1:
        app.ai.race(app)
    app.player.move(40, app, None)
    app.ai.move(40, app, None)
    app.track.moveCoords(app)
    checkEnd(app)
    if not app.track.end(app) and app.infinite:
        app.scrollY += 0.1
    elif not app.track.end(app):
        app.scrollY += 4
    else:
        app.scrollY = 0
        gameFinish(app)
    if app.infinite:
        pass
    app.player.physics(app)
    app.ai.physics(app)
        
##########################################
# Course Builder
# This screen allows a player to build a track.
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
    canvas.create_rectangle(app.width*(1/10) + 50, app.height*(1/10) + 25,
                            app.width*(1/10) - 50, app.height*(1/10) - 25,
                            fill='blue')
    canvas.create_text(app.width*(1/10), app.height*(1/10), text="Back", fill='black')

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
    if (event.x > app.width*(1/10) - 50 and event.x < app.width*(1/10) + 50 and
        event.y > app.height*(1/10) - 25 and event.y < app.height*(1/10) + 25):
        app.mode = 'startScreenMode'

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
# This is where all of the global variables are created and where the app is run from.
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
    app.centerCarCount = 0
    app.obstacleCount = 0
    app.winner = ""
    app.startSoundRunning = 0
    app.centerCarCount = 0

def drawStartScreen(app, canvas):
    canvas.create_rectangle(0, 0, app.width,
                     app.height, fill='black')
    canvas.create_text(app.width/2, app.height/2,text="Hello", fill='red')

runApp(width=800, height=600, title="Rowdy Racers")

