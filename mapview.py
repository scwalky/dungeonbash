import pygame
import math
import pickle

pygame.init()
w=1920
h=1080
v_offset=0
h_offset=0
i=0

size=(w,h)
screen = pygame.display.set_mode(size)
pygame.key.set_repeat(100,50)
blue=(0,0,255)
white=(120, 120, 100 )
transparent=(255,0,255)

#img=pygame.image.load('WaveEchoCavern-(ZF-1106-77751-1-001)-0_01.jpg')
img=pygame.image.load('WaveEchoCavern_small.jpg')
img_rect=img.get_rect()
img_max_h_offset=img_rect.right
img_max_v_offset=img_rect.bottom
img_max_v_offset=0-img_max_v_offset+h
img_max_h_offset=0-img_max_h_offset+w
block_size=72

fog = pygame.Surface((img_rect.size))
#fog.fill((255,255,255))
fog.fill((255,0,255))
fog.set_colorkey((255,0,255))
#fog.fill(blue)

print(img_rect.size)
print(img_max_h_offset)
print(img_max_v_offset)
print(img_rect.bottom)

# make an array - figure out how many cells there needs to be
y_blocks=math.floor(img_rect.bottom/block_size)+1
x_blocks=math.floor(img_rect.right/block_size)+1
print('Blocks across',y_blocks)
print('Blocks down',x_blocks)

Matrix={}
#Initialise as greyed out
for x in range(x_blocks):
    for y in range(y_blocks):
        Matrix[x,y]=1


# Initialise the block array
# does the file exist?
try:
    f=open('mask.obj', 'rb')
    Matrix=pickle.load(f)
    f.close()
except OSError:
    pass

#print(Matrix)  
#Matrix[2,3]=1
#Matrix[3,4]=1

while i < img_rect.right - 72:
    i+=72
    pygame.draw.line(fog,white,[i,0],[i,img_rect.bottom],2)

i=0
while i < img_rect.bottom - 72:
    i+=72
    pygame.draw.line(fog,white,[0,i],[img_rect.right,i],2)   
    
test_fill=pygame.Rect((5*block_size,block_size),(block_size, block_size))
fog.fill(white,test_fill)



#            print(line*block_size, ',', cell_y*block_size)
#            test_fill=pygame.Rect((line*block_size,cell_y*block_size),(block_size, block_size))
#            fog.fill(white,test_fill)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            file = open('mask.obj','wb')
            pickle.dump(Matrix,file)
            file.close()
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: pygame.quit()
            if event.key == pygame.K_RIGHT: h_offset += -72
            if event.key == pygame.K_LEFT: h_offset += 72
            if event.key == pygame.K_UP: v_offset += 72
            if event.key == pygame.K_DOWN: v_offset += -72
            if v_offset > 0: v_offset=0
            if h_offset > 0: h_offset=0
            if v_offset < img_max_v_offset: v_offset=img_max_v_offset
            if h_offset < img_max_h_offset: h_offset=img_max_h_offset
            #print(h_offset)
            #print(img_max_h_offset)
            #print(img_max_v_offset)
            #print(v_offset)
        # Check the mouse!
        if event.type == pygame.MOUSEBUTTONDOWN:
            # where is the mouse?
            (mouse_x,mouse_y)=pygame.mouse.get_pos()
            print(mouse_x, ',',mouse_y)
            mouse_actual_x=mouse_x+(0-h_offset)
            mouse_actual_y=mouse_y+(0-v_offset)
            mouse_block_x=math.floor(mouse_actual_x/block_size)+1
            mouse_block_y=math.floor(mouse_actual_y/block_size)+1
            print(mouse_block_x, ',',mouse_block_y)
            if (mouse_block_x, mouse_block_y) in Matrix.keys():
                print('Found!')
                #print(Matrix)
                del Matrix[mouse_block_x, mouse_block_y]
                #print(Matrix)
                #if Matrix[mouse_block_x, mouse_block_y]==0: Matrix[mouse_block_x, mouse_block_y]=1
            else:
                Matrix[mouse_block_x, mouse_block_y]=1
    
    # Fill the blocks!
    fog.fill(transparent)
    for (x,y),v in Matrix.items():
        #print(x,',',y,',',v)
        #print((x*block_size)-block_size, ',', (y*block_size)-block_size)
        if v==1:
            test_fill=pygame.Rect(((x*block_size)-block_size,(y*block_size)-block_size),(block_size, block_size))
            fog.fill(white,test_fill)
        else:
            test_fill=pygame.Rect(((x*block_size)-block_size,(y*block_size)-block_size),(block_size, block_size))
            fog.fill(transparent,test_fill)            
    screen.blit(img,(h_offset,v_offset))
    screen.blit(fog,(h_offset,v_offset))
    pygame.display.flip()
