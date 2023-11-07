import sys
import pygame
import pygame.camera
import pygwidgets
import cv2
import numpy as np

from pygame.locals import *
from ColorPicker import *
from SimpleSlider import *
from pathlib import Path

# pygame.transform.threshold(frame, frame, (0,255,0),(90,170,170),(0,0,0),1)

class ThresholdControls():
    
    def __init__(self, window, startingX=0, startingY=0, searchColor=(0,0,0), threshColor=(0,0,0), threshinvert=False):
        self.invert = threshinvert
        self.x = startingX
        self.y = startingY
        
        self.window = window
        self.searchColor = {'R':searchColor[0],
                            'G':searchColor[1],
                            'B':searchColor[2],
                            }
        self.threshColor = {'R':threshColor[0],
                            'G':threshColor[1],
                            'B':threshColor[2],
                            }
        

        self.button_array = []
        
        self.text_array = []
        self.input_array = []

        # Invert threshold option
        self.oInputThresholdInvert = pygwidgets.TextCheckBox(self.window, (self.x, self.y), 'Invert Threshold', value=self.invert)
        self.input_array.append(self.oInputThresholdInvert)

        # Setup search color text / input
        self.oTextThresholdSearchColor = pygwidgets.DisplayText(self.window, (self.x, self.y+30), 'Search Color :')
        self.text_array.append(self.oTextThresholdSearchColor)
        
        self.cpSearch_R = SimpleSlider(self.x, self.y+45, 200, 30, self.window, bgColor=WHITE, sliderColor=RED)
        self.input_array.append(self.cpSearch_R)

        self.oInputThresholdSearchColor_R = pygwidgets.InputText(self.window, (self.x + 210, self.y + 50), width=50, value=str(self.searchColor['R']))
        self.input_array.append(self.oInputThresholdSearchColor_R)

        self.cpSearch_G = SimpleSlider(self.x, self.y+80, 200, 30, self.window, bgColor=WHITE, sliderColor=GREEN)
        self.input_array.append(self.cpSearch_G)
        
        self.oInputThresholdSearchColor_G = pygwidgets.InputText(self.window, (self.x + 210, self.y + 85), width=50, value=str(self.searchColor['G']))
        self.input_array.append(self.oInputThresholdSearchColor_G)

        self.cpSearch_B = SimpleSlider(self.x, self.y+115, 200, 30, self.window, bgColor=WHITE, sliderColor=BLUE)
        self.input_array.append(self.cpSearch_B)
        
        self.oInputThresholdSearchColor_B = pygwidgets.InputText(self.window, (self.x + 210, self.y + 120), width=50, value=str(self.searchColor['B']))
        self.input_array.append(self.oInputThresholdSearchColor_B)

        # Now the threshold color
        self.oTextThresholdThresholdColor = pygwidgets.DisplayText(self.window, (self.x, self.y + 170), 'Threshold Color :')
        self.text_array.append(self.oTextThresholdThresholdColor)

        self.cpThresh_R = SimpleSlider(self.x, self.y + 185, 200, 30, self.window, bgColor=WHITE, sliderColor=RED)
        self.input_array.append(self.cpThresh_R)

        self.oInputThresholdThresholdColor_R = pygwidgets.InputText(self.window, (self.x + 210, self.y + 190), width=50, value=str(self.threshColor['R']))
        self.input_array.append(self.oInputThresholdThresholdColor_R)

        self.cpThresh_G = SimpleSlider(self.x, self.y + 220, 200, 30, self.window, bgColor=WHITE, sliderColor=GREEN)
        self.input_array.append(self.cpThresh_G)

        self.oInputThresholdThresholdColor_G = pygwidgets.InputText(self.window, (self.x + 210, self.y + 225), width=50, value=str(self.threshColor['G']))
        self.input_array.append(self.oInputThresholdThresholdColor_G)

        self.cpThresh_B = SimpleSlider(self.x, self.y + 255, 200, 30, self.window, bgColor=WHITE, sliderColor=BLUE)
        self.input_array.append(self.cpThresh_B)
        
        self.oInputThresholdThresholdColor_B = pygwidgets.InputText(self.window, (self.x + 210, self.y + 260), width=50, value=str(self.threshColor['B']))
        self.input_array.append(self.oInputThresholdThresholdColor_B)

    def draw(self):
        for text in self.text_array:
            text.draw()
        
        for input in self.input_array:
            input.draw()
        
        return

    def handleEvent(self, event):
        # Invert?
        if self.oInputThresholdInvert.handleEvent(event):
            self.invert = not self.invert
        # Search color
        if self.oInputThresholdSearchColor_R.handleEvent(event):
            self.searchColor_R = self.oInputThresholdSearchColor_R.getValue()
            self.searchColor['R'] = self.searchColor_R
        if self.oInputThresholdSearchColor_G.handleEvent(event):
            self.searchColor_G = self.oInputThresholdSearchColor_G.getValue()
            self.searchColor['G'] = self.searchColor_G
        if self.oInputThresholdSearchColor_B.handleEvent(event):
            self.searchColor_B = self.oInputThresholdSearchColor_B.getValue()
            self.searchColor['B'] = self.searchColor_B
        # Threshold color
        if self.oInputThresholdThresholdColor_R.handleEvent(event):
            self.threshColor_R = self.oInputThresholdThresholdColor_R.getValue()
            self.threshColor['R'] = self.threshColor_R
        if self.oInputThresholdThresholdColor_G.handleEvent(event):
            self.threshColor_G = self.oInputThresholdThresholdColor_G.getValue()
            self.threshColor['G'] = self.threshColor_G
        if self.oInputThresholdThresholdColor_B.handleEvent(event):
            self.threshColor_B = self.oInputThresholdThresholdColor_B.getValue()
            self.threshColor['B'] = self.threshColor_B
        
        
        threshEvent = {'threshinvert': self.invert,
                       'searchcolor': self.searchColor,
                       'threshcolor': self.threshColor,
                       }
        
        newTcolor = self.cpThresh_R.handleEvent(event)
        if (newTcolor):
            threshEvent['threshcolor']['R'] = newTcolor
            self.oInputThresholdThresholdColor_R.setText(str(newTcolor))
            
        newTcolor = self.cpThresh_G.handleEvent(event)
        if (newTcolor):
            threshEvent['threshcolor']['G'] = newTcolor
            self.oInputThresholdThresholdColor_G.setText(str(newTcolor))

        newTcolor = self.cpThresh_B.handleEvent(event)
        if (newTcolor):
            threshEvent['threshcolor']['B'] = newTcolor
            self.oInputThresholdThresholdColor_B.setText(str(newTcolor))
            
        
        newScolor = self.cpSearch_R.handleEvent(event)
        if (newScolor):
            threshEvent['searchcolor']['R'] = newScolor
            self.oInputThresholdSearchColor_R.setText(str(newScolor))
        
        newScolor = self.cpSearch_G.handleEvent(event)
        if (newScolor):
            threshEvent['searchcolor']['G'] = newScolor
            self.oInputThresholdSearchColor_G.setText(str(newScolor))

        newScolor = self.cpSearch_B.handleEvent(event)
        if (newScolor):
            threshEvent['searchcolor']['B'] = newScolor
            self.oInputThresholdSearchColor_B.setText(str(newScolor))
        
        
            
            
        return threshEvent
