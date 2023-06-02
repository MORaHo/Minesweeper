import random
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import numpy
import math
import time

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
lost = False
LEFT = 1
RIGHT = 3

#initialize board
first_click = True
empty_work_board = []
empty_check_board = []

def form_check_board():
    for a in range(HEIGHT):
        for b in range(WIDTH):
            empty_check_board.append([None])
    work_check_board = numpy.array(empty_check_board).reshape(HEIGHT,WIDTH)
    return work_check_board

def form_board():
    for a in range(HEIGHT):
        for b in range(WIDTH):
            empty_work_board.append([0])
    work_board = numpy.array(empty_work_board,dtype=object).reshape(HEIGHT,WIDTH)
    return work_board

def set_bombs():
    empty_bomb_board = form_board()
    bomb_list = []
    for a in range(BOMB_NUMB):
        bomb_list.append([random.randint(0,HEIGHT-1),random.randint(0,WIDTH-1)])
    for bomb in bomb_list:
        empty_bomb_board[bomb[0]][bomb[1]] = 9
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
pg.display.set_caption("Go")

screen.fill(base_colour)
pg.display.flip()


def floodfill(matrix_indices):

    item = worktop[matrix_indices[0]][matrix_indices[1]]
    draw(matrix_indices)
    if item != EMPTY: return
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
    if checktop[matrix_indices[0]][matrix_indices[1]] == None:
        path = str(10) + ".png"
        image = pg.image.load(os.path.join(__location__,"Sprites",path)).convert()
        smol_image = pg.transform.scale(image,(CELL_SIZE,CELL_SIZE))
        srect = smol_image.get_rect(x=(matrix_indices[1]*CELL_SIZE),y=(matrix_indices[0]*CELL_SIZE))
        screen.blit(smol_image,srect)
        checktop[matrix_indices[0]][matrix_indices[1]] = 1
    else: 
        checktop[matrix_indices[0]][matrix_indices[1]] = None
        pg.draw.rect(screen,base_colour,(matrix_indices[1]*CELL_SIZE,matrix_indices[0]*CELL_SIZE,CELL_SIZE,CELL_SIZE))

def draw(matrix_indices):
    root  = worktop[matrix_indices[0]][matrix_indices[1]]
    pg.draw.rect(screen,grey,(matrix_indices[1]*CELL_SIZE,matrix_indices[0]*CELL_SIZE,CELL_SIZE,CELL_SIZE))
    if root == 0:
        pass
    else:
        path = str(root) + ".png"
        image = pg.image.load(os.path.join(__location__,"Sprites",path)).convert()
        smol_image = pg.transform.scale(image,(CELL_SIZE,CELL_SIZE))
        srect = smol_image.get_rect(x=(matrix_indices[1]*CELL_SIZE),y=(matrix_indices[0]*CELL_SIZE))
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
                if worktop[matrix_indices[0]][matrix_indices[1]] != 0:
                    del(worktop)
                    worktop = set_board()
                else:
                    first_click = False
                    floodfill(matrix_indices)
                    pass
            else:
                if event.button == LEFT:
                    flagged = (checktop[matrix_indices[0]][matrix_indices[1]] != None)
                    if worktop[matrix_indices[0]][matrix_indices[1]] == 9 and not flagged:
                        lost = True
                    if worktop[matrix_indices[0]][matrix_indices[1]] == 9 and flagged:
                        continue
                    else:
                        floodfill(matrix_indices)
                else:
                    flag(matrix_indices)




    pg.display.flip()
    CLOCK.tick(60)