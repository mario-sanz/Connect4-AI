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
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) # creo una matriz 6x7 rellena de ceros
    return board;


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0 # está la columna vacía?


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r # la funcion nos devuelve la primera fila que esté vacía


def print_board(board):
    print(np.flip(board, 0)) # revierte el board desde el eje 0


def winning_move(board, piece):
    # Comprobar posibilidades HORIZONTALES
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

    # Comprobar posibilidades VERTICALES
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

    # Comprobar posibilidades DIAGONALES CON PENDIENTE POSITIVA
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Comprobar posibilidades DIAGONALES CON PENDIENTE NEGATIVA
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
        score -= 4 # cuenta más que nosotros tengamos 3 en raya que que el rival tenga 3 en raya
    
    return score
    

def score_position(board, piece):
    score = 0
    # PUNTUACIÓN DEL CENTRO
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # PUNTUACIÓN HORIZONTAL
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])] # esto guarda una fila en un solo array
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # PUNTUACIÓN VERTICAL
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])] # la columna c es guardada en un array
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # PUNTUACIÓN DIAGONAL CON PENDIENTE POSITIVA
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # PUNTUACIÓN DIAGONAL CON PENDIENTE NEGATIVA
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0
    # devuelve True si gana el jugador, si gana la AI, o si np quedan posiciones en el tablero


"""
ESTA ES LA VERSION ORIGINAL DE MINIMAX, DEBAJO DE ESTA FUNCIÓN ESTÁ "ALPHA-BETA PRUNING", QUE ES UNA VERSION MAS COMPLEJA DE MINIMAX QUE ELIMINA LAS RAMAS QUE NO DEBEN SER TOMADAS DESDE UN PRINCIPIO PARA QUE EL ALGORITMO FUNCIONE MAS RAPIDO

def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000)
            else: # game over, no hay mas movimientos validos
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
            new_score = minimax(b_copy, depth-1, True)[1] # cambia al maximizing player
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
            else: # game over, no hay mas movimientos validos
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
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1] # cambia al maximizing player
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
    # dibujo del tablero y agujeros vacios
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE: # dibujar fichas 1
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: # dibujar fichas 2
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

turn = random.randint(PLAYER, AI) # hace que empiece el jugador o la IA aleatoriamente

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # dibuja la ficha arriba moviendose antes de caer
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) # borra la anterior ficha moviendose
            posx = event.pos[0]
            if turn == PLAYER: # jugador 1
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE)) # borra la anterior ficha moviendose
            #print(event.pos) # esto nos imprime en consola las coordenadas de donde pinchamos

            # Input del PRIMER jugador
            if turn == PLAYER:
                posx = event.pos[0] # pos[0] indica el eje x de las coordenadas
                col = int(math.floor(posx/SQUARESIZE)) # esto nos da el numero de la columna que pulsamos
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, PLAYER_PIECE) # las fichas del jugador 1 siempre son 1

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("JUGADOR 1 GANA", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    # ALTERNANCIA DE TURNOS
                    turn += 1
                    turn = turn % 2 # el turno va a alternar entre 0 y 1

                    # TABLERO
                    print_board(board)
                    draw_board(board)


    # Input del SEGUNDO jugador
    if turn == AI and not game_over:

        # col = random.randint(0, COLUMN_COUNT-1)
        # col = pick_best_move(board, AI_PIECE)
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row = get_next_open_row(board,col)
            drop_piece(board, row, col, AI_PIECE) # las fichas del jugador 2 siempre son 2

            if winning_move(board, AI_PIECE):
                label = myfont.render("ORDENADOR GANA", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

            # TABLERO
            print_board(board)
            draw_board(board)

            # ALTERNANCIA DE TURNOS
            turn += 1
            turn = turn % 2 # el turno va a alternar entre 0 y 1

    if game_over:
        pygame.time.wait(3000) # espera 3 segundos antes de cerrarse la ventana

