from board import *
from move import Move
import random
import copy

class AI:
    def __init__(self, level = 1, player = 'red'):
        self.level = level
        self.player = player
    
    def rnd(self, board):
        all_moves = board.all_valid_moves(self.player)
        idx = random.randrange(0, len(all_moves))
        return all_moves[idx]
    
    def minimax(self, board, maximizing, depth):
        #terminal case
        case = board.final_state()
        if case == 'blue':
            return 16, None #eval, move
        elif case == 'red':
            return -16, None
        elif depth > 1:
            return board.value, self.rnd(board)
        
        if maximizing:
            max_eval = -100
            best_move = None
            all_moves = board.all_valid_moves(self.player)
            for move in all_moves:  
                temp_board = copy.deepcopy(board)
                initial = move.initial
                piece = temp_board.squares[initial.row][initial.col].piece
                temp_board.move(piece, move)
                eval = self.minimax(temp_board, False, depth + 1)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                if eval == 16:
                    max_eval = eval
                    best_move = move
                    return max_eval, best_move
            return max_eval, best_move
        elif not maximizing:
            min_eval = 100
            best_move = None
            all_moves = board.all_valid_moves(self.player)
            for move in all_moves:  
                temp_board = copy.deepcopy(board)
                initial = move.initial
                piece = temp_board.squares[initial.row][initial.col].piece
                temp_board.move(piece, move)
                eval = self.minimax(temp_board, True, depth + 1)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                if eval == -16:
                    min_eval = eval
                    best_move = move
                    return min_eval, best_move
            return min_eval, best_move
        
    def eval(self, board):
        eval, move = self.minimax(board, False, 0)
        # eval = 'random'
        # move = self.rnd(board)
        print('AI has chosen to move the piece at pos: ', move.initial.row, ',', move.initial.col, 'to pos: ', move.final.row, ',',\
            move.final.col, 'with the eval of: ', eval)
        return move
            
            