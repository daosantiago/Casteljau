# -*- coding: UTF-8 -*-

#Importa os pacotes
import pygame
import os
import sys
from pygame.locals import *


class Dot(object):
    """Dot class"""
    def __init__(self, x, y, color, prev = None):
        self.__x = x
        self.__y = y
        self.__color = color
        self.__prev = prev
        
    #Defines dot position
    def position(self):
        return (self.__x, self.__y)

    #Property for x position
    @property
    def x(self):
        return self.__x

    #Property for y position
    @property
    def y(self):
        return self.__y

    #Property for dot color
    @property
    def color(self):
        return self.__color

    #Draws the clicked dots
    def draw_vertex(self, scr):
        pygame.draw.circle(scr, self.color, self.position(),3)
        pygame.display.update()
        

class Color(object):
    """docstring for color"""
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    #Dotefines the color
    def color(self):
        return [self.r, self.g, self.b]

    #Static method for white color
    @staticmethod
    def white():
        return [255, 255, 255]

    #Static method for red color
    @staticmethod
    def red():
        return [255, 0, 0]

    #Static method for green color
    @staticmethod
    def green():
        return [0, 255, 0]
    
    #Static method for blue color
    @staticmethod
    def blue():
        return [0, 0, 255]

    @staticmethod
    def black():
        return [0,0,0]

class Curve(object):
    """docstring for Curve"""
    def __init__(self, dots):
        self.dots = dots
        

class Aplication(object):
    """docstring for Aplication"""
    def __init__(self):
        self.screen = pygame.display.set_mode([1280,768])
        self.dots=[]
        self.curve_dots = []
        print('Application has been Created')

    def clear(self):
        self.screen.fill(Color.black())
        pygame.display.update()

    #Render a welcome and instructions
    def welcome(self):
        #Init the font module
        pygame.font.init()
        #Instance of Font
        font = pygame.font.SysFont('Arial', 25)
        msg = []
        msg.append('Welcome to Casteljau\'s Bezier Curve')
        msg.append('Click on the screen as many times you want (minimum 2), then press any key to draw the lines and the curve')

        #Create the image to blit on screen
        #text = font.render(msg, True, Color.white())
        for line in range(len(msg)):
            self.screen.blit(font.render(msg[line], True, Color.white()), [150, 150 + (line*30)])
        
        pygame.display.update()

        self.wait()


    #Waits for a key to be pressed
    def wait(self):
        wait = True
        while wait:
            for event in pygame.event.get():
                if (event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN):
                    wait = False
        self.clear()

    def flash_message(self, dot):
        font = pygame.font.SysFont('Arial', 25)
        self.screen.blit(font.render('You need to give at least two points', True, Color.white()), [150, 150])
        pygame.display.update()
        self.wait()
        if (len(dot) != 0):
            dot[0].draw_vertex(self.screen)

    #Get the points clicked in the screen
    def get_events(self, dots):

        run = True

        while run:
            for event in pygame.event.get():
                if (event.type == MOUSEBUTTONDOWN):
                    
                    #Creates a dot object
                    dot = Dot(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], Color.red())

                    dot.draw_vertex(self.screen)
                    #Appends into the dots array the clicked position and the dot color
                    dots.append(dot)

                #Breaks the loop if a key is pressed
                if (event.type == KEYDOWN):
                    if (len(self.dots) >= 2):
                        run = False
                    else:
                        self.flash_message(dots)



    #Draws the lines between dots
    def draw_lines(self, dots, line_color = Color.red()):
        for i in range(0, len(dots)-1):
            pygame.draw.line(self.screen, line_color, dots[i].position(), dots[i+1].position())
            pygame.display.update()



    #Calculates the new dots 
    def curve(self, dots, rate):
        u=rate
        sub_line_dots=[]

        #Runs through dots to create new sub lines
        for i in range(0, len(dots)-1):
            x_new_dot = int((1 - u) * dots[i].x + u * dots[i+1].x)
            y_new_dot = int((1 - u) * dots[i].y + u * dots[i+1].y)

            #adds new subline dots to vector
            sub_line_dots.append(Dot(x_new_dot, y_new_dot, Color.red()))


        #Calls recursievly curve method if there's more than two dots
        if (len(sub_line_dots) >= 2):
            self.curve(sub_line_dots, u)
        else: #else there's only one dot remaining, and this is the dot curve
            self.curve_dots.append(Dot(sub_line_dots[0].x, sub_line_dots[0].y, Color.white()))

            #Draws subline dots
        self.draw_lines(sub_line_dots, Color.blue())


    #Main loop
    def loop(self):

        self.welcome()

        #Call the event listener so the user can clicks de screen
        self.get_events(self.dots)

        #Draw the clicked dots
        self.draw_lines(self.dots)

        rate = 0

        #While the rate doesn't get to the end of the lines and sublines, keeps increasing
        while(rate < 1):
            self.curve(self.dots, rate)
            rate = rate + 0.01

        #Creates the efective curve whith generated dots
        curve = Curve(self.curve_dots)

        self.draw_lines(curve.dots, Color.white())

        #self.wait()

        #Calls the same draw_vertex method used before,
        #but giving as argument the efective curve dots
        for cd in curve.dots:
            cd.draw_vertex(self.screen)



if __name__ == '__main__':

    app = Aplication()

    app.loop()

    app.wait()
