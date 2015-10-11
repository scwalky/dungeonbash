#Handles The underlying map object for the base layer of the screen
#TODO : Add ability to offset the start of the image

import pygame
import math

class mapimage(object):
    def __init__(self):
        self.img_max_h_offset=0
        self.img_max_v_offset=0
    def load(self,filename, h,w,indent_x=0,indent_y=0):
        self.mapsurf = pygame.image.load(filename)        
        self.rect = self.mapsurf.get_rect()
        # Check parameters to see if we are cropping the image
        add=indent_x+indent_y
#        if add > 0:
            # cropping image NYI!       
        self.width=self.rect.right
        self.height=self.rect.bottom
        self.img_max_h_offset=self.rect.right
        self.img_max_v_offset=self.rect.bottom
        self.img_max_v_offset=0-self.img_max_v_offset+h
        self.img_max_h_offset=0-self.img_max_h_offset+w        
    def max_offset(self,xytype):
        if xytype=='x':return self.img_max_h_offset
        if xytype=='y':return self.img_max_v_offset
