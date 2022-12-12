from const import *
from square import Square
from piece import *
from move import Move
import copy
class Board:
    
    def __init__(self):
        self.squares = [[0,0,0,0,0] for col in range(COLS)]
        self._create()
        self._add_pieces('blue')
        self._add_pieces('red')
        self.value = 0
        
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    def _add_pieces(self, color):
        for col in range(COLS):
            if color == 'blue':
                self.squares[0][col] = Square(0, col, Piece(color))
            else:
                self.squares[4][col] = Square(4, col, Piece(color))
        if color == 'blue': 
            self.squares[1][0] = Square(1, 0, Piece(color))
            self.squares[1][4] = Square(1, 4, Piece(color))
            self.squares[2][0] = Square(2, 0, Piece(color))
        else:
            self.squares[2][4] = Square(2, 4, Piece(color))
            self.squares[3][4] = Square(3, 4, Piece(color))
            self.squares[3][0] = Square(3, 0, Piece(color))
            
    def move(self, piece, move, testing = False):
        initial = move.initial 
        final = move.final 
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        self.check_ganh(piece, move)
        self.check_vay(piece)
        piece.clear_moves()
        self.calc_value()
        
    def calc_moves(self, piece, row, col, bool = True):
        piece.clear_moves()
        #Calculate all the possible moves
        if (row + col) % 2 == 0:
            possible_moves = [
                (row, col + 1),
                (row, col - 1),
                (row + 1, col),
                (row - 1, col),
                (row + 1, col + 1),
                (row - 1, col + 1),
                (row + 1, col - 1),
                (row - 1, col - 1)                
            ] 
        else:
            possible_moves = [
                (row, col + 1),
                (row, col - 1),
                (row + 1, col),
                (row - 1, col)
            ]
        for possible_move in possible_moves:
            possible_move_row, possible_move_col = possible_move
            if Square.in_range(possible_move_row, possible_move_col):
                if self.squares[possible_move_row][possible_move_col].isempty():
                    #create new move
                    initial = Square(row, col)
                    final = Square(possible_move_row, possible_move_col)
                    move = Move(initial, final)
                    piece.add_move(move)
    def valid_move(self, piece, move):
        return move in piece.moves
    def final_state(self):
        if self.value == 16:
            return 'blue'
        elif self.value == -16:
            return 'red'
        else:
            return 'green'
    def calc_value(self):
        self.value = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    self.value += self.squares[row][col].piece.value
    def check_ganh(self, piece, move):
        final = move.final 
        if (final.row + final.col)%2 == 0:
            if Square.in_range(final.row, final.col + 1) and Square.in_range(final.row, final.col - 1):
                if self.squares[final.row][final.col - 1].has_piece() and self.squares[final.row][final.col + 1].has_piece():
                    if self.squares[final.row][final.col - 1].piece.color != piece.color and self.squares[final.row][final.col + 1].piece.color != piece.color:
                        self.squares[final.row][final.col - 1].piece.change_color()
                        self.squares[final.row][final.col + 1].piece.change_color()
            if Square.in_range(final.row + 1, final.col) and Square.in_range(final.row - 1, final.col):
                if self.squares[final.row + 1][final.col].has_piece() and self.squares[final.row - 1][final.col].has_piece():
                    if self.squares[final.row + 1][final.col].piece.color != piece.color and self.squares[final.row - 1][final.col].piece.color != piece.color:
                        self.squares[final.row + 1][final.col].piece.change_color()
                        self.squares[final.row - 1][final.col].piece.change_color()
            if Square.in_range(final.row+1, final.col + 1) and Square.in_range(final.row-1, final.col - 1):
                if self.squares[final.row-1][final.col - 1].has_piece() and self.squares[final.row+1][final.col + 1].has_piece():
                    if self.squares[final.row-1][final.col - 1].piece.color != piece.color and self.squares[final.row+1][final.col + 1].piece.color != piece.color:
                        self.squares[final.row-1][final.col - 1].piece.change_color()
                        self.squares[final.row+1][final.col + 1].piece.change_color()
            if Square.in_range(final.row-1, final.col + 1) and Square.in_range(final.row+1, final.col - 1):
                if self.squares[final.row+1][final.col - 1].has_piece() and self.squares[final.row-1][final.col + 1].has_piece():
                    if self.squares[final.row+1][final.col - 1].piece.color != piece.color and self.squares[final.row-1][final.col + 1].piece.color != piece.color:
                        self.squares[final.row+1][final.col - 1].piece.change_color()
                        self.squares[final.row-1][final.col + 1].piece.change_color()
        else:
            if Square.in_range(final.row, final.col + 1) and Square.in_range(final.row, final.col - 1):
                if self.squares[final.row][final.col - 1].has_piece() and self.squares[final.row][final.col + 1].has_piece():
                    if self.squares[final.row][final.col - 1].piece.color != piece.color and self.squares[final.row][final.col + 1].piece.color != piece.color:
                        self.squares[final.row][final.col - 1].piece.change_color()
                        self.squares[final.row][final.col + 1].piece.change_color()
            if Square.in_range(final.row + 1, final.col) and Square.in_range(final.row - 1, final.col):
                if self.squares[final.row + 1][final.col].has_piece() and self.squares[final.row - 1][final.col].has_piece():
                    if self.squares[final.row + 1][final.col].piece.color != piece.color and self.squares[final.row - 1][final.col].piece.color != piece.color:
                        self.squares[final.row + 1][final.col].piece.change_color()
                        self.squares[final.row - 1][final.col].piece.change_color()   
    def check_vay(self, piece):
        if piece.color == 'blue':
            color = 'red'
        else:
            color = 'blue'
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    if self.squares[row][col].piece.color == color:
                        if self.check_bi_vay(color, row, col):
                            self.squares[row][col].piece.change_color()
                            
    def check_bi_vay(self, color, row, col):
        flag = True
        if (row + col) % 2 == 0:
            possible_neighbors = [
                (row, col + 1),
                (row, col - 1),
                (row + 1, col),
                (row - 1, col),
                (row + 1, col + 1),
                (row - 1, col + 1),
                (row + 1, col - 1),
                (row - 1, col - 1)                
            ] 
        else:
            possible_neighbors = [
                (row, col + 1),
                (row, col - 1),
                (row + 1, col),
                (row - 1, col)
            ]
        for possible_neighbor in possible_neighbors:
            possible_n_row, possible_n_col = possible_neighbor 
            if Square.in_range(possible_n_row, possible_n_col):
                if self.squares[possible_n_row][possible_n_col].isempty():
                    return False
                elif self.squares[possible_n_row][possible_n_col].piece.color != color:
                    continue
                elif self.squares[possible_n_row][possible_n_col].piece.color == color and \
                    self.squares[possible_n_row][possible_n_col].piece.moves != []:   
                    return False
                elif self.squares[possible_n_row][possible_n_col].piece.color == color and \
                    self.squares[possible_n_row][possible_n_col].piece.moves == []:  
                    temp_board = copy.deepcopy(self)
                    temp_board.squares[row][col].piece.change_color()
                    flag = temp_board.check_bi_vay(color, possible_n_row, possible_n_col)
                    if flag == False:
                        return False
        return flag
    def all_valid_moves(self, player):
        all = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    if self.squares[row][col].piece.color == player:
                        self.calc_moves(self.squares[row][col].piece, row, col)
                        if self.squares[row][col].piece.moves != []:
                            for move in self.squares[row][col].piece.moves:
                                all.append(move)
        return all