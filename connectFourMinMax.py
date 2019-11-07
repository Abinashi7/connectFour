"""
@author: Abinashi Singh
This algorithm is designed to make AI bit smarter and always choose the center move if it's an AI's turn first.
This increases the chance of winning. Moreover, every move is evaluated first and then implement
it based on scores.
However, you will notice, this algo takes longer when we increase the look-up depth.
For example, set the dept to 5 or 6 in the main program loop, it will take forever to make
a move, since it is looking for every combination of a winning move.


                        *************************
Upon running this file, you will be prompted to new window that will show you connectFour
board in which you can make moves.
There is a little big on my end which results in premature closing of this window
when the termination condition is met. However, I am also printing updated results
on the console to confirm it was indeed a terminating condition
                        *************************
"""

import random
import sys
import numpy as np
import pygame
import math

# rgb value of blue

BLUE = (0,0,200)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4
# using numpy to create borad with all 0's initially
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
#     check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
#         vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
#         check diagonals on positive sides
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

#         check diagonals on negative sides
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_windiow(window, piece):
    score = 0
    # if it's not our turn, then opponent piece is AI's piece
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) ==2 and window.count(EMPTY) == 2:
        score += 5
    # in case AI is about to win
    if window.count(opponent_piece) ==3 and window.count(EMPTY) == 1:
        score -= 8

    return score
# to assign the score to our board
def score_position(board, piece):
    score = 0
    # to get the middle column or prefer the center position because the chances of winning are higher
    # get every row position but for the centre position
    center = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center.count(piece)
    score += center_count * 6


    #     horizontal score
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_windiow(window, piece)

    #         verticle score
    for c in range(COLUMN_COUNT):
        # we want to get every row position for a specific col
        col_array = [int(i) for i in list(board[:, c])]
    #     iterate through the row window
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_windiow(window, piece)

#         diagonal score - low on the left side and rise up on the right side
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_windiow(window, piece)

#         other diagonal winning choice- top to downwards diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3-i][c + i] for i in range(WINDOW_LENGTH)]

            score += evaluate_windiow(window, piece)


    return score
 # terninal node conditions are: us winning, or bot winning or it's a draw
def is_terminal(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_location(board)) ==0

# followed pseudocode from Wikipedia minMax
def mini_max(board, depth, maximizingPlayer):

    valid_location = get_valid_location(board)
    terminal = is_terminal(board)
    if depth ==0 or terminal:
        if terminal:
            # if it's a bot's winning move
            if winning_move(board, AI_PIECE):
                # none will take place of the column that produces the best score
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                # none will take place of the column that produces the best score
                return (None, -10000000)
            else:
                return (None, 0)  #game is over
        else: #when depth is 0
            return (None, score_position(board, AI_PIECE))
    #     True and false below will help us switch between players
    if maximizingPlayer:
        column = random.choice(valid_location)
        value = -math.inf
        for col in valid_location:
            row= get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            # [1] because 1st index is giving the best score
            new_score = mini_max(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col #which col gave you the best score
        return column, value
    else: # for minimizer
        column = random.choice(valid_location)
        value = math.inf
        for col in valid_location:
            row= get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score =  mini_max(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col #which col gave you the best score
        return column, value



def get_valid_location(board):
    valid_location = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_location.append(col)

    return valid_location

def pick_best_move(board, piece):
    valid_location = get_valid_location(board)
    # best score
    best_score = 0
    best_col = random.choice(valid_location)
    for col in valid_location:
        row = get_next_open_row(board, col)
        # temporary testing the move. Making .copy() to avoid changes in our original board
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def draw_board(board):
     for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)

     for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
     pygame.display.update()


board = create_board()
game_over = False

# for gaphics
pygame.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width , height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

# Randomly choose who goes first
turn = random.randint(PLAYER, AI)


# where game begins!
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # ask player 1 turn
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("player 1 wins!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    turn += 1
                    turn = turn % 2
                    # to see board in console
                    print_board(board)
                    # to see board in via numpy graphics
                    draw_board(board)
    # player two turn
    if turn == AI and not game_over:
        # posx = event.pos[0]
        # col = random.randint(0, COLUMN_COUNT-1)
        # making AI pick the best move available currently
        # col = pick_best_move(board, AI_PIECE)
        # setting depth level to 4 or how far is it going to look to make a best move
        col, score = mini_max(board, 5, True)

        if is_valid_location(board, col):
            # waiting to avoid very quick animation by Bot
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("player 2 wins!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            # to see board in console
            print_board(board)
            # to see board in via numpy graphics
            draw_board(board)

            turn += 1
            turn = turn % 2

    # after someone win or draw shutdown the window
    if game_over:
        pygame.time.wait(3000)

