import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0,0,255) # blue color for the screen
BLACK = (0,0,0) # black color for the screen
RED = (255,0,0) # red color for the tiles of player 1
YELLOW = (255,255,0) # yellow color for the tiles of player 2

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) # create a 6x7 matrix full of 0's
    return board;


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0 # is the column empty?


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r # the function returns the first row that is empty


def print_board(board):
    print(np.flip(board, 0)) # flips the board from axix 0


def winning_move(board, piece):
    # Check HORIZONTAL possibilities
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

    # Check VERTICAL possibilities
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

    # Check DIAGONALS WITH POSITIVE SLOPE possibilities
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check DIAGONALS WITH NEGATIVE SLOPE possibilities
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece == AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4 # it counts more that we have 3 in a row to win that that the opponent has 3 in a row
    
    return score
    

def score_position(board, piece):
    score = 0
    # CENTER SCORE
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # HORIZONTAL SCORE
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])] # store row t into an array
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # VERTICAL SCORE
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])] # store column c into an array
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # DIAGONALS WITH POSITIVE SLOPE SCORE
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # DIAGONALS WITH NEGATIVE SLOPE SCORE
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0
    # returns True if the player wins, if the AI wins, or if there are no more positions in the board

"""
THIS IS THE ORIGINAL MINIMAX VERSION, BELLOW THIS FUNCITION IS "ALPHA-BETA PRUNING", THAT IS AN IMPROVED VERSION
OF MINIMAX WHICH ELIMINATES BRANCHES THAT ARE NOT WORKING SO THAT THE ALGORITHM IS MORE EFFICIENT

def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000)
            else: # game over, no more valid movements
                return (None, 0)
        else: # depth = 0
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else: # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, True)[1] # change to maximizing player
            if new_score < value:
                value = new_score
                column = col
        return column, value
"""
def minimax(board, depth, alpha, beta, maximizingPlayer): # ALPHA-BETA PRUNING
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # game over, no more valid movements
                return (None, 0)
        else: # depth = 0
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1] # changes to maximizing player
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    # draw of the board and empty spaces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE: # draw tiles 1 (red)
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: # draw tiles 2 (yellow)
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

    pygame.display.update()


board = create_board()
print_board(board)
game_over = False

# GRAPHICAL INTERFACE
pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size) # creates the window
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI) # player or IA start at random

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # draw the tile moving in the upper part of the board before falling
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) # constantly erase the previous moving tile
            posx = event.pos[0]
            if turn == PLAYER: # player 1
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) # erase the previous moving tile
            #print(event.pos) # this tells us on the console the coordinates of the window on which we press

            # Input of FIRST player
            if turn == PLAYER:
                posx = event.pos[0] # pos[0] is the x axis of the coordinates
                col = int(math.floor(posx/SQUARESIZE)) # this gives us the column number on which we press
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, PLAYER_PIECE) # tiles of player 1 are always 1

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("JUGADOR 1 GANA", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    # TURN ALTERNANCE
                    turn += 1
                    turn = turn % 2 # turn is going to altern between 0 and 1

                    # BOARD
                    print_board(board)
                    draw_board(board)


    # Input of SECOND player
    if turn == AI and not game_over:

        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row = get_next_open_row(board,col)
            drop_piece(board, row, col, AI_PIECE) # tiles of player 2 are always 2

            if winning_move(board, AI_PIECE):
                label = myfont.render("ORDENADOR GANA", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

            # BOARD
            print_board(board)
            draw_board(board)

            # TURN ALTERNANCE
            turn += 1
            turn = turn % 2 # turn is going to altern between 0 and 1

    if game_over:
        pygame.time.wait(3000) # wait 3 seconds before closing the window
