##########################################
# Game Mode
##########################################

from cmu_112_graphics import *
import math, copy, os, random
import pygame #Used for Sound

class GameMode(App):


    def redrawAll(app, canvas):
        app.player.draw(canvas)

    def keyPressed(app, event):
        if event.key == "Right":
            app.player.rotate(-22.5)
        if event.key == "Left":
            app.player.rotate(22.5)
        if event.key.lower() == "p":
            app.mode = 'startScreenMode'
        pass

    def timerFired(app):
        app.player.move(20, app)
        pass

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
        def __init__(self, type):
            pass

        def generate(self, list):
            pass

        def draw(self, app, canvas):
            pass