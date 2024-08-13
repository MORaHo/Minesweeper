import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import numpy
import math
import random

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#game start constants
DIFFICULTY = 5
COEFFICIENT = 1/3
MAX_DIFFICULTY = 0.14
HEIGHT = 30
WIDTH = 30
BOMB_DENSITY = MAX_DIFFICULTY/(1+math.exp(-COEFFICIENT * DIFFICULTY)) - (MAX_DIFFICULTY*math.exp(-(DIFFICULTY - math.sqrt(5))**2))
BOMB_NUMB = int(HEIGHT * WIDTH * BOMB_DENSITY)
CELL_SIZE = 25
EMPTY = 0

#pygame variables
base_colour = (68,150,72)
grey = (192,192,192)
black = (0,0,0)
lost = False

LEFT = 1
RIGHT = 3

#initialize board
flagged_numb = 0
first_click = True
empty_work_board = []
empty_check_board = []

def form_check_board():
    empty_check_board = [[[None] for a in range(WIDTH)] for y in range(HEIGHT)]
    work_check_board = numpy.array(empty_check_board).reshape(HEIGHT,WIDTH)
    return work_check_board

def form_board():
    empty_work_board = [[[0] for x in range(WIDTH)] for y in range(HEIGHT)]
    work_board = numpy.array(empty_work_board).reshape(HEIGHT,WIDTH)
    return work_board

def set_bombs():
    empty_bomb_board = form_board()
    bomb_list = []
    bombs = 0
    for a in range(BOMB_NUMB):
        y = random.randint(0,HEIGHT-1)
        x = random.randint(0,WIDTH-1)
        bomb_list.append([random.randint(0,HEIGHT-1),random.randint(0,WIDTH-1)])
        bombs += 1
    for bomb in bomb_list:
        y = bomb[0]
        x = bomb[1]
        while empty_bomb_board[y][x] == 9:
            y = random.randint(0,HEIGHT-1)
            x = random.randint(0,WIDTH-1)
        empty_bomb_board[y][x] = 9
    work_board = empty_bomb_board
    return work_board

def bomb_count(a,b,work_board):
    count = 0
    for y in range(a-1,a+2):
        for x in range(b-1,b+2):
            if y == -1 or x == -1 or y == HEIGHT or x == WIDTH: continue
            if work_board[y][x] == 9:
                count += 1
    return count

def set_board():
    worktop = set_bombs()
    for a in range(HEIGHT):
        for b in range(WIDTH):
            if worktop[a][b] == 9:
                pass
            else:
                worktop[a][b] = bomb_count(a,b,worktop)
    return worktop
#initializing pygame window
pg.init()
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((WIDTH*CELL_SIZE,HEIGHT*CELL_SIZE),0,32)
pg.display.set_caption("Minesweeper")

screen.fill(base_colour)
pg.display.flip()

for j in range(0,WIDTH+1):
    #horizontal lines 
    pg.draw.line(screen,black,(CELL_SIZE*j,0),(j*CELL_SIZE,WIDTH*CELL_SIZE),1)

for i in range(0,HEIGHT+1):
    #vertical lines
    pg.draw.line(screen,black,(0,i*CELL_SIZE),(HEIGHT*CELL_SIZE,i*CELL_SIZE),1)
pg.display.update()

def floodfill(matrix_indices):

    item = worktop[matrix_indices[0]][matrix_indices[1]]
    draw(matrix_indices)
    if item != EMPTY:
        checktop[matrix_indices[0]][matrix_indices[1]] = 1
        return
    else:
        draw(matrix_indices)
        for y in range(matrix_indices[0]-1,matrix_indices[0]+2):
            for x in range(matrix_indices[1]-1,matrix_indices[1]+2):
                if y == -1 or x == -1 or y == HEIGHT or x == WIDTH: continue
                if checktop[y][x] != None:
                    
                    pass
                    
                else:
                    checktop[y][x] = 1
                    floodfill([y,x])

def flag(matrix_indices):
    global flagged_numb
    if flagged_numb == BOMB_NUMB and ((checktop == None).any()) and checktop[matrix_indices[0]][matrix_indices[1]] != "flagged":
        return
    if checktop[matrix_indices[0]][matrix_indices[1]] == None:
        path = str(10) + ".png"
        image = pg.image.load(os.path.join(__location__,"Sprites",path)).convert()
        smol_image = pg.transform.scale(image,(CELL_SIZE-1,CELL_SIZE-1))
        srect = smol_image.get_rect(x=(matrix_indices[1]*CELL_SIZE+1),y=(matrix_indices[0]*CELL_SIZE+1))
        screen.blit(smol_image,srect)
        flagged_numb += 1
        checktop[matrix_indices[0]][matrix_indices[1]] = "flagged"
    elif checktop[matrix_indices[0]][matrix_indices[1]] == "flagged": 
        checktop[matrix_indices[0]][matrix_indices[1]] = None
        pg.draw.rect(screen,base_colour,(matrix_indices[1]*CELL_SIZE+1,matrix_indices[0]*CELL_SIZE+1,CELL_SIZE-1,CELL_SIZE-1))
        flagged_numb -= 1

def draw(matrix_indices):
    root  = worktop[matrix_indices[0]][matrix_indices[1]]
    pg.draw.rect(screen,grey,(matrix_indices[1]*CELL_SIZE+1,matrix_indices[0]*CELL_SIZE+1,CELL_SIZE-1,CELL_SIZE-1))
    if root == 0:
        pass
    else:
        path = str(root) + ".png"
        image = pg.image.load(os.path.join(__location__,"Sprites",path)).convert()
        smol_image = pg.transform.scale(image,(CELL_SIZE-1,CELL_SIZE-1))
        srect = smol_image.get_rect(x=(matrix_indices[1]*CELL_SIZE+1),y=(matrix_indices[0]*CELL_SIZE+1))
        screen.blit(smol_image,srect)

while not lost:

    for event in pg.event.get():

        if event.type == pg.QUIT:
            lost = True

        
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            matrix_indices = [int(mouse_pos[1]//CELL_SIZE),int(mouse_pos[0]//CELL_SIZE)]
            if first_click:
                empty_work_board = []
                empty_check_board = []
                worktop = set_board()
                checktop = form_check_board()
                while worktop[matrix_indices[0]][matrix_indices[1]] != 0:
                    empty_work_board = []
                    worktop = []
                    worktop = set_board()
                else:
                    first_click = False
                    floodfill(matrix_indices)
                    pass
            else:
                if event.button == LEFT: #left click
                    flagged = (checktop[matrix_indices[0]][matrix_indices[1]] == "flagged")
                    if worktop[matrix_indices[0]][matrix_indices[1]] == 9 and not flagged:
                        lost = True
                    if worktop[matrix_indices[0]][matrix_indices[1]] == 9 and flagged:
                        continue
                    else:
                        floodfill(matrix_indices)
                else: #right click
                    if checktop[matrix_indices[0]][matrix_indices[1]] == 1:
                        continue
                    else:
                        if flagged_numb == BOMB_NUMB and ((checktop != None).all()):
                            print("You won!")
                            lost = True
                        else:
                            flag(matrix_indices)
                if flagged_numb == BOMB_NUMB and ((checktop != None).all()):
                    print("You won!")
                    lost = True

    pg.display.flip()
    CLOCK.tick(60)
