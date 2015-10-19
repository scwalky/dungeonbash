# Handles the fog layer
#

import pygame
import math
import pickle

white=(120, 120, 100 )
transparent=(255,0,255)

class foglayer(object):
    def __init__(self, blocksize, width, height):
        self.Matrix={}
        self.width=width
        self.height=height
        self.x_blocks=int(math.floor(width/blocksize)+1)
        self.y_blocks=int(math.floor(height/blocksize)+1)
        self.blocksize=blocksize
        self.surface=pygame.Surface((width,height))
        self.clear()
        self.fillgrid(0)
        self.v_offset=0
        self.h_offset=0
        
    def clear(self):
        self.surface.fill(transparent)
        self.surface.set_colorkey(transparent)
        
    def fillgrid(self,value):
        for x in range(self.x_blocks):
            for y in range(self.y_blocks):
                self.Matrix[x,y]=value
                
    def gridlines(self):
        i=0
        while i < self.width - self.blocksize:
            i+=self.blocksize
            pygame.draw.line(self.surface,white,[i,0],[i,self.height],2)

        i=0
        while i < self.height - self.blocksize:
            i+=self.blocksize
            pygame.draw.line(self.surface,white,[0,i],[self.width,i],2)
    def paint(self):
        x=0
        y=0
        v=0
        for (x,y),v in self.Matrix.items():
            if v==1:
                fillrect=pygame.Rect(((x*self.blocksize)-self.blocksize,(y*self.blocksize)-self.blocksize),(self.blocksize, self.blocksize))
                self.surface.fill(white,fillrect)
            else:
                fillrect=pygame.Rect(((x*self.blocksize)-self.blocksize,(y*self.blocksize)-self.blocksize),(self.blocksize, self.blocksize))
                self.surface.fill(transparent,fillrect)
    def toggleblock(self,block_x,block_y):
        if (block_x, block_y) in self.Matrix.keys():
            if (self.Matrix[block_x, block_y]==1):
                print('Removing Block')
                self.Matrix[block_x, block_y]=0
            else:
                print('Adding Block')
                self.Matrix[block_x, block_y]=1
        self.paint()
                
    def clearblock(self,block_x,block_y):
        if (block_x, block_y) in self.Matrix.keys():
            #print('Adding Block')
            self.Matrix[block_x, block_y]=0
                
    def paintblock(self,block_x,block_y):
        if (block_x, block_y) in self.Matrix.keys():
            #print('Removing Block')
            self.Matrix[block_x, block_y]=1
                
    def togglearea(self, block_x, block_y):
        if (block_x, block_y) in self.Matrix.keys():
            # remove a larger block
            if (self.Matrix[block_x, block_y]==1):
                for x in range(0,3):
                    for y in range(-1,3):
                        self.clearblock(block_x+y, block_y-x)
                        self.clearblock(block_x+y, block_y+y)
                        self.clearblock(block_x+y, block_y+x)
                        self.clearblock(block_x+x, block_y-x)
                        self.clearblock(block_x+x, block_y+y)
                        self.clearblock(block_x+x, block_y+x)
                        self.clearblock(block_x-x, block_y-x)
                        self.clearblock(block_x-x, block_y+y)
                        self.clearblock(block_x-x, block_y+x)                    
            else:
                for x in range(1,3):
                    for y in range(-1,3):
                        self.paintblock(block_x+y, block_y-x)
                        self.paintblock(block_x+y, block_y+y)
                        self.paintblock(block_x+y, block_y+x)
                        self.paintblock(block_x+x, block_y-x)
                        self.paintblock(block_x+x, block_y+y)
                        self.paintblock(block_x+x, block_y+x)
                        self.paintblock(block_x-x, block_y-x)
                        self.paintblock(block_x-x, block_y+y)
                        self.paintblock(block_x-x, block_y+x)
	self.paint()
            
    def blockstate(self,block_x,block_y):
        return self.Matrix[block_x,block_y]
    
    def save(self, filename,v_offset,h_offset):
        file = open(filename,'wb')
        pickle.dump(self.Matrix,file)
        pickle.dump(v_offset, file)
        pickle.dump(h_offset, file)
        file.close()
    def load(self, filename):
        try:
            f=open(filename, 'rb')
            self.Matrix=pickle.load(f)
            self.v_offset=pickle.load(f)
            self.h_offset=pickle.load(f)
            f.close()
        except EOFError:
            pass
        except OSError:
            pass
    
