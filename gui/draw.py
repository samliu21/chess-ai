import pygame
import numpy as np

from globals import board_colour, square_size
import globals

wp = pygame.image.load('images/white_pawn.gif')
bp = pygame.image.load('images/black_pawn.gif')
wn = pygame.image.load('images/white_knight.gif')
bn = pygame.image.load('images/black_knight.gif')
wb = pygame.image.load('images/white_bishop.gif')
bb = pygame.image.load('images/black_bishop.gif')
wr = pygame.image.load('images/white_rook.gif')
br = pygame.image.load('images/black_rook.gif')
wq = pygame.image.load('images/white_queen.gif')
bq = pygame.image.load('images/black_queen.gif')
wk = pygame.image.load('images/white_king.gif')
bk = pygame.image.load('images/black_king.gif')

switch = pygame.image.load('images/switch.png')
switch = pygame.transform.scale(switch, (50, 60))

restart = pygame.image.load('images/restart.png')
restart = pygame.transform.scale(restart, (40, 40))

FROM_COLOUR = (187, 203, 61)
TO_COLOUR = (246, 246, 127)

def draw_background(win):
    win.fill((255, 255, 255))

    for x in range(8):
        for y in range(0, 8):
            if (x % 2 == 1 and y % 2 == 0) or (x % 2 == 0 and y % 2 == 1):
                pygame.draw.rect(win, board_colour, (x * square_size, y * square_size, square_size, square_size))
    
    if globals.from_square:
        pygame.draw.rect(win, FROM_COLOUR, (globals.from_square[0] * square_size, globals.from_square[1] * square_size, square_size, square_size))

    if globals.to_square:
        pygame.draw.rect(win, TO_COLOUR, (globals.to_square[0] * square_size, globals.to_square[1] * square_size, square_size, square_size))

    win.blit(switch, (625, 200))
    win.blit(restart, (630, 320))

def draw_pieces(win, fen, human_white):
    def fen_to_array(fen):
        fen = fen.split()[0]

        arr = []

        rows = fen.split('/')
        for row in rows:
            row_arr = []
            for ch in str(row):
                if ch.isdigit():
                    for _ in range(int(ch)):
                        row_arr.append('.')
                else:
                    row_arr.append(ch)
            arr.append(row_arr)

        return arr
     
    arr = fen_to_array(fen=fen)

    piece_to_variable = {
        'p': bp,
        'n': bn,
        'b': bb,
        'r': br,
        'q': bq,
        'k': bk,
        'P': wp,
        'N': wn,
        'B': wb,
        'R': wr,
        'Q': wq,
        'K': wk, 
    }

    if not human_white:
        arr = np.array(arr)
        arr = np.flip(arr, axis=[0, 1])

    for x in range(8):
        for y in range(8):
            
            if arr[y][x] == '.':
                continue 
            
            piece = piece_to_variable[arr[y][x]]

            win.blit(piece, (x * square_size, y * square_size))