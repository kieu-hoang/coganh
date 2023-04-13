import pygame
import time
from const import *
from board import Board
from dragger import Dragger
from square import Square
from move import Move
from AI import *

class Game:
    def __init__(self, level=1):
        self.next_player = 'blue'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.ai = AI(level)
        self.running = False
        self.paused = False
        self.gamemode = 'ai'
        self.winner = 'green'
        self.p1Name = "Player 1"
        self.p2Name = "Player 2"
        self.startTime = time.time()
        self.time1 = 360
        self.time2 = 360

        self.storedTime1 = 0
        self.storedTime2 = 0
        
    def show_lines(self, surface):
        #vertical line
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, SQSIZE//2), (SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (3*SQSIZE//2, SQSIZE//2), (3*SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (5*SQSIZE//2, SQSIZE//2), (5*SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (7*SQSIZE//2, SQSIZE//2), (7*SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (WIDTH-SQSIZE//2, SQSIZE//2), (WIDTH-SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        #horizontal line
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, SQSIZE//2), (WIDTH-SQSIZE//2, SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, 3*SQSIZE//2), (WIDTH-SQSIZE//2, 3*SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, 5*SQSIZE//2), (WIDTH-SQSIZE//2, 5*SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, 7*SQSIZE//2), (WIDTH-SQSIZE//2, 7*SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, HEIGHT-SQSIZE//2), (WIDTH-SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        #diagonal lines
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, SQSIZE//2), (WIDTH-SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (WIDTH-SQSIZE//2, SQSIZE//2), (SQSIZE//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (WIDTH//2, SQSIZE//2), (SQSIZE//2, HEIGHT//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (WIDTH//2, SQSIZE//2), (WIDTH-SQSIZE//2, HEIGHT//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (SQSIZE//2, HEIGHT//2), (WIDTH//2, HEIGHT-SQSIZE//2), LINE_WIDTH)
        pygame.draw.line(surface, LINE_COLOR, (WIDTH//2, HEIGHT-SQSIZE//2), (WIDTH-SQSIZE//2, HEIGHT//2), LINE_WIDTH)
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # all pieces except dragger piece
                    if piece is not self.dragger.piece:
                        piece.set_texture()
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other methods

    def next_turn(self):
        self.next_player = 'blue' if self.next_player == 'red' else 'red'
    def reset(self):
        self.__init__()
    def change_gamemode(self):
        if self.gamemode == 'pvp': 
            self.gamemode = 'ai'
        else:
            self.gamemode = 'pvp'  
    def isover(self):
        self.winner = self.board.final_state()
        return self.board.final_state() != 'green'
    def make_move(self, move: Move):
        initial = move.initial 
        piece = self.board.squares[initial.row][initial.col].piece
        self.board.move(piece, move)
        if self.next_player == "blue":
            self.storedTime1 += (time.time() - self.startTime)
        else:
            self.storedTime2 += (time.time() - self.startTime)
        self.startTime = time.time()
        self.next_turn()            