import numpy as np 
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7
blue_color = (0,0, 255)
black_color = (0,0,0)
red_color = (255,0,0)
yellow_color = (255,255,0)

def board_default():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def piece_drp(board, row, played, piece):
    board[row][played] = piece

def is_Valid(board, played):
    return board[ROW_COUNT - 1][played] == 0

def open_row(board, played):
    for row in range(ROW_COUNT):
        if board[row][played] == 0:
            return row

def print_board(board):
    print(np.flip(board, 0))

def win_situation(board, piece):
    # Check Horizental 
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][column] == piece and board[row][column + 1] == piece and board[row][column + 2] == piece and board[row][column + 3] == piece:
                return True
    # Check Vertical
    for column in range(COLUMN_COUNT):
        for row in range(ROW_COUNT - 3):
            if board[row][column] == piece and board[row + 1][column] == piece and board[row + 2][column] == piece and board[row + 3][column] == piece:
                return True
    # Check Diagnols (from bottom to top)
    for column in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if board[row][column] == piece and board[row + 1][column + 1] == piece and board[row + 2][column + 2] == piece and board[row + 3][column + 3] == piece:
                return True
    # Check Diagnols (from top to bottom)
    for column in range(COLUMN_COUNT - 3):
        for row in range(3, ROW_COUNT):
            if board[row][column] == piece and board[row - 1][column + 1] == piece and board[row - 2][column + 2] == piece and board[row - 3][column + 3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, blue_color, (c*squaresize, r*squaresize+squaresize, squaresize, squaresize))
            pygame.draw.circle(screen, black_color, (int(c*squaresize+squaresize/2), int(r*squaresize+squaresize+squaresize/2)), radius)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, red_color, (int(c*squaresize+squaresize/2), height-int(r*squaresize+squaresize/2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, yellow_color, (int(c*squaresize+squaresize/2), height-int(r*squaresize+squaresize/2)), radius)
    pygame.display.update()

board = board_default()
print_board(board)
game_over = False
turn = 0

pygame.init()

squaresize = 100
width = COLUMN_COUNT * squaresize
height = (ROW_COUNT + 1) * squaresize

size = (width, height)
radius = int(squaresize/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black_color,(0,0, width, squaresize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red_color, (posx, int(squaresize/2)), radius)
            else:
                pygame.draw.circle(screen, yellow_color, (posx, int(squaresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black_color,(0,0, width, squaresize))
            #print(event.pos)       
            if turn == 0:
                posx = event.pos[0]
                played = int(math.floor(posx/squaresize))
                #played = int(input("Player 1 Turn (0-6): "))
                if is_Valid(board, played):
                    row = open_row(board, played)
                    piece_drp(board, row, played, 1)

                    if win_situation(board, 1):
                        label = myfont.render("Player 1 Wins!", 1, red_color)
                        screen.blit(label, (40,10))
                        game_over = True
    
            else:
                posx = event.pos[0]
                played = int(math.floor(posx/squaresize))
                if is_Valid(board, played):
                    row = open_row(board, played)
                    piece_drp(board, row, played, 2)

                    if win_situation(board, 2):
                        label = myfont.render("Player 2 Wins!", 1, yellow_color)
                        screen.blit(label, (40,10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2
    
            if game_over:
                pygame.time.wait(3500)

