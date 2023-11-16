# 1 - Import packages
import sys
import pygame
import pygame.camera
import pygwidgets
import numpy as np
import math

from pygame.locals import *
from pathlib import Path
from ThresholdControls import *

# 2 - Define constants 
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TEAL = (0, 255, 255)
PURPLE = (255, 0, 255)

WINDOW_WIDTH = 640 # 1280
WINDOW_HEIGHT = 480 # 720
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FRAMES_PER_SECOND = 60

BASE_PATH = Path(__file__).resolve().parent


class CameraControl:
    
    __slots__ = ('timer', 'window_width', 'window_height', 'frames_per_second', 'camera_surface',
                 'ui_surface', 'window', 'clock', 'backends', 'cameras', 'threshold_active',
                 'threshold_settings_active', 'ghosting_active', 'flashback_active', 'grayscale_active',
                 'threshold_inverted','button_array', 'oButtonColorSpace', 'button_array', 'oButtonThresholdEffectSettings',
                 'oInputThresholdActive', 'oInputGhostingEffect', 'oInputFlashbackEffect', 'oInputGrayscale',
                 'ghosting_dict', 'flashback_dict', 'search_color', 'thresh_color', 'oThresh', 'cam_list',
                 'current_cam', 'pycam', 'frame', 'frame_alt',)
                 
    def __init__(self, window_width=WINDOW_WIDTH, window_height=WINDOW_HEIGHT, frames_per_second=FRAMES_PER_SECOND):                
        # 3 - Initialize the world
        pygame.init()
        pygame.camera.init()
        self.timer = 0
        self.window_width = window_width
        self.window_height = window_height
        self.frames_per_second = frames_per_second

        self.camera_surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.ui_surface = pygame.display.set_mode((100, 50))
        self.window = pygame.display.set_mode((self.window_width+300, self.window_height))


        self.clock = pygame.time.Clock()

        # 4 - Load assets: image(s), sound(s), etc.

        # 5 - Initialize variables

        self.backends = pygame.camera.get_backends()
        self.cameras = pygame.camera.list_cameras()

        self.threshold_active = False
        self.threshold_settings_active = False
        self.threshold_inverted = False
        self.ghosting_active = False
        self.flashback_active = False
        self.grayscale_active = False

        self.button_array = []
        startingx = CAMERA_WIDTH + 10
        self.oButtonColorSpace = pygwidgets.TextButton(self.window, (startingx, 10), 'Change Color Space')
        self.button_array.append(self.oButtonColorSpace)


        self.oButtonThresholdEffectSettings = pygwidgets.TextButton(self.window, (startingx, 50), 'Threshold Settings')
        self.button_array.append(self.oButtonThresholdEffectSettings)

        self.oInputThresholdActive = pygwidgets.TextCheckBox(self.window, (startingx + 145, 15), 'Threshold effect', value=self.threshold_active)
        self.button_array.append(self.oInputThresholdActive)

        self.oInputGhostingEffect = pygwidgets.TextCheckBox(self.window, (startingx + 145, 30), 'Ghosting effect', value=self.ghosting_active)
        self.button_array.append(self.oInputGhostingEffect)

        self.oInputFlashbackEffect = pygwidgets.TextCheckBox(self.window, (startingx + 145, 45), 'Flashback effect', value=self.flashback_active)
        self.button_array.append(self.oInputFlashbackEffect)
        
        self.oInputGrayscale = pygwidgets.TextCheckBox(self.window, (startingx + 145, 60), 'Grayscale', value=self.threshold_active)
        self.button_array.append(self.oInputGrayscale)

        self.ghosting_dict = {'x_offset':0,
                               'direction':1,
                               'y_offset':0,
                               }

        self.flashback_dict = {'x_offset':1,
                               'y_offset':0,
                               'direction':0,
                               }

        self.search_color = {'R':0,
                             'G':255,
                             'B':0,
                             }
        self.thresh_color = {'R':90,
                             'G':170,
                             'B':170,
                             }

        self.oThresh = ThresholdControls(self.window, startingX=startingx, startingY=115, searchColor=(0,255,0), threshColor=(90,170,170), threshinvert=False)



        # Use camera 0
        print(self.cameras)
        self.cam_list = []
        pycamRGB = pygame.camera.Camera(self.cameras[0], (CAMERA_WIDTH, CAMERA_HEIGHT), "RGB")
        self.cam_list.append(pycamRGB)
        pycamYUV = pygame.camera.Camera(self.cameras[0], (CAMERA_WIDTH, CAMERA_HEIGHT), "YUV")
        self.cam_list.append(pycamYUV)
        pycamHSV = pygame.camera.Camera(self.cameras[0], (CAMERA_WIDTH, CAMERA_HEIGHT), "HSV")
        self.cam_list.append(pycamHSV)

        self.current_cam = 0
        self.pycam = self.cam_list[self.current_cam]
        self.pycam.start()

        # wait for camera to grab first frame
        while (self.pycam.query_image() == False):
            pass
        self.frame = self.pycam.get_image()
        self.frame_alt = pygame.surfarray.array2d(self.frame)

    # Okay I called this the flashback effect initially but it's actually the Wayne's World "dream sequence" effect.
    def flashback(self, frame, x_max=100):
        # x(t)= A cos(((2π)/T)t) = A cos(ωt) 
        # # T = period (total time), A = amplitude, 2pi = angular velocity
        # The "period" here could be the time it takes to reach x_max
        
        if(not isinstance(frame, np.ndarray)):
            return
        alt_frame = frame.copy()
        col = len(alt_frame)-1
        while col > 0:
            row = len(alt_frame[col])-1
            while row > 0:
                self.flashback_dict['x_offset'] = int(100 * math.cos( (((2 * math.pi) / x_max)) * (self.timer+row)))
                # print(self.flashback_dict['x_offset'])
                if col + self.flashback_dict['x_offset'] < self.window_width and col + self.flashback_dict['x_offset'] > 0:
                    if row + self.flashback_dict['y_offset'] < self.window_height:
                        alt_frame[col + self.flashback_dict['x_offset']][row + self.flashback_dict['y_offset']] = frame[col][row]
                        
                row-=1
                # For traingular zig zags remove self.flashback_dict['x_offset'] = int(100 * math.cos( (((2 * math.pi) / x_max)) * self.timer)) above
                """ 
                if self.flashback_dict['direction']: # if direction is 1 then increase offset
                    self.flashback_dict['x_offset']+=1
                else:
                    self.flashback_dict['x_offset']-=1 # otherwise descrese offset
                
                if self.flashback_dict['x_offset'] > x_max: # if the offset is higher than the max
                    self.flashback_dict['direction'] = 0 # switch the offset direction
                if self.flashback_dict['x_offset'] < x_max - 100: # if it's lower than max -100
                    self.flashback_dict['direction'] = 1 # start increasing the amount
                    self.flashback_dict['x_offset'] = x_max -100 # starting at x_max - 100
                """
            col-=1
            # self.flashback_dict['x_offset'] = 0
        alt_frame=pygame.surfarray.make_surface(alt_frame)
        return alt_frame

    def ghosting(self, alt_frame):
        if(not isinstance(alt_frame, np.ndarray)):
            return
        # if(not isinstance(alt_frame, pygame.PixelArray)):
        #   return
        for col in range(len(alt_frame)): # Col is width 640
            for row in range(len(alt_frame[col])): # Row is height 480
                
                if col + self.ghosting_dict['x_offset'] < self.window_width:
                    if row + self.ghosting_dict['y_offset'] < self.window_height:
                        # alt_frame[col][row]+=10500 # adjust the hue of the ghosting effect 
                        # alt_frame[col + self.ghosting_dict['x_offset']][row+ self.ghosting_dict['y_offset']] = alt_frame[col][row] 
                        # Switching to faster "itemset" method below:
                        alt_frame.itemset(( col + self.flashback_dict['x_offset'], row + self.flashback_dict['y_offset']), frame[col][row])
                    
                self.ghosting_dict['x_offset']+=2
                if self.ghosting_dict['x_offset'] > 400:
                    self.ghosting_dict['x_offset'] = 0
            self.ghosting_dict['y_offset']+=0
            if self.ghosting_dict['y_offset'] > 200:
                self.ghosting_dict['y_offset'] = 0

        # alt_frame.close()
        alt_frame=pygame.surfarray.make_surface(alt_frame)
        return alt_frame
    
    def action(self):
        # 6 - Loop forever
        while True:
            # 7 - Check for and handle events
            for event in pygame.event.get():
                # Clicked the close button? Quit pygame and end the program
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # 8 - Do any "per frame" actions
                if self.oButtonColorSpace.handleEvent(event):
                    self.current_cam+=1
                    if self.current_cam > len(self.cam_list)-1:
                        self.current_cam = 0
                    self.pycam.stop()
                    self.pycam = self.cam_list[self.current_cam]
                    self.pycam.start()
                
                if self.oButtonThresholdEffectSettings.handleEvent(event):
                    self.threshold_settings_active = not self.threshold_settings_active

                if self.oInputGhostingEffect.handleEvent(event):
                    self.ghosting_active = not self.ghosting_active

                if self.oInputFlashbackEffect.handleEvent(event):
                    self.flashback_active = not self.flashback_active

                if self.oInputThresholdActive.handleEvent(event):
                    self.threshold_active = not self.threshold_active
                
                if self.oInputGrayscale.handleEvent(event):
                    self.grayscale_active = not self.grayscale_active

                if self.threshold_active:
                    thresh_event = self.oThresh.handleEvent(event)
                    if "searchcolor" in thresh_event.keys():
                        self.search_color = thresh_event["searchcolor"]
                    if "threshcolor" in thresh_event.keys():
                        self.thresh_color = thresh_event["threshcolor"]
                    if "threshinvert" in thresh_event.keys():
                        self.threshold_inverted = thresh_event['threshinvert']


            # 9 - Clear the window

            self.window.fill(GRAY)

            # 10 - Draw all window elements
            if self.pycam.query_image():
                self.frame = self.pycam.get_image()
                self.frame_alt = pygame.surfarray.array2d(self.frame)
                # self.frame_alt = pygame.PixelArray(self.frame)
            
            if self.ghosting_active == True:
                self.frame_alt = self.ghosting(self.frame_alt)
                self.frame = self.frame_alt
            
            if self.flashback_active == True:             
                self.frame_alt = self.flashback(self.frame_alt, x_max=100)
                self.frame = self.frame_alt
            
            if self.grayscale_active == True:
                if self.frame is not None:
                    self.frame = pygame.transform.grayscale(self.frame)
        
            if self.threshold_active == True:
                scolor = (int(self.search_color['R']), int(self.search_color['G']), int(self.search_color['B']))
                threshColor = (int(self.thresh_color['R']), int(self.thresh_color['G']), int(self.thresh_color['B']))
                # print("Threshcolor :", threshColor)
                if self.frame is not None:
                    pygame.transform.threshold(self.frame, self.frame, scolor, threshColor, (0,0,0),1,inverse_set=self.threshold_inverted)
            if self.frame is not None:
               self.window.blit(self.frame, (0,0))

            for button in self.button_array:
                button.draw()
            
            if self.threshold_settings_active:
                self.oThresh.draw()


            # 11 - Update the window
            pygame.display.update()

            # 12 - Slow things down a bit
            self.timer += 5
            if self.timer > 300:
                self.timer = 0
            self.clock.tick(self.frames_per_second)
    

oCamControl = CameraControl()
oCamControl.action()
