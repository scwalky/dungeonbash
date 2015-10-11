# Simple Tabletop RPG Assistant
# TODO:Parameterise Filename

import pygame
import math
import objects.map
import objects.mask
test_mask_filename='WaveEcho.obj'
test_img_filename='WaveEchoCavern_small.jpg'

# Start Pygame
pygame.init()
pygame.key.set_repeat(50,10)
block_size=36

w=1800
h=1000
v_offset=0
h_offset=0

# Load Map
background=objects.map.mapimage()
background.load(test_img_filename,h,w)

# Load Fog
fog=objects.mask.foglayer(block_size,background.width,background.height)
fog.load(test_mask_filename)
h_offset=fog.h_offset
v_offset=fog.v_offset
fog.paint()

#fog.fillgrid()

size=(w,h)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Dungeon Bash 0.1 (' + str(h_offset) + ',' + str(v_offset) + ') ' + test_img_filename)    

while 1:
    #pygame.event.wait()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fog.save(test_mask_filename, v_offset, h_offset)
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: pygame.quit()
            if event.key == pygame.K_RIGHT: h_offset += -block_size
            if event.key == pygame.K_LEFT: h_offset += block_size
            if event.key == pygame.K_UP: v_offset += block_size
            if event.key == pygame.K_DOWN: v_offset += -block_size
            if event.key == pygame.K_PAGEDOWN: v_offset += -(block_size*10)
            if event.key == pygame.K_PAGEDOWN: v_offset += (block_size*10)
            #if event.key == pygame.K_g: fog.gridlines()
            #if event.key == pygame.K_h: fog.clear()            
            #if event.key == pygame.K_f: fog.paint()
            if event.key == pygame.K_s: fog.save(test_mask_filename)
            if event.key == pygame.K_l: fog.load(test_mask_filename)
            #if event.key == pygame.K_q: fog.fillgrid(1)
            #if event.key == pygame.K_w: fog.fillgrid(0)
            if v_offset > 0: v_offset=0
            if h_offset > 0: h_offset=0
            if v_offset < background.max_offset('y'): v_offset=background.max_offset('y')
            if h_offset < background.max_offset('x'): h_offset=background.max_offset('x')
            fog.paint()
            pygame.display.set_caption('Dungeon Bash 0.1 (' + str(h_offset) + ',' + str(v_offset) + ') '+test_img_filename)    
        if event.type == pygame.MOUSEBUTTONDOWN:
            # where is the mouse?
            (mouse_x,mouse_y)=pygame.mouse.get_pos()
            (left_mouse, middle_mouse,right_mouse)=pygame.mouse.get_pressed()
            print(mouse_x, ',',mouse_y)
            mouse_actual_x=mouse_x+(0-h_offset)
            mouse_actual_y=mouse_y+(0-v_offset)
            mouse_block_x=math.floor(mouse_actual_x/block_size)+1
            mouse_block_y=math.floor(mouse_actual_y/block_size)+1
            if (left_mouse==1):
                print(mouse_block_x, ',',mouse_block_y)
                fog.toggleblock(mouse_block_x,mouse_block_y)
            if (right_mouse==1):
                print(mouse_block_x, ',',mouse_block_y)
                fog.togglearea(mouse_block_x,mouse_block_y)            
            fog.paint()
            
    screen.blit(background.mapsurf,(h_offset, v_offset))
    screen.blit(fog.surface,(h_offset, v_offset))
    pygame.display.flip()
