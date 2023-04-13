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
    
    def minimax(self, board, maximizing, depth, alpha, beta):
        #terminal case
        case = board.final_state()
        if case == 'blue':
            return 16, None #eval, move
        elif case == 'red':
            return -16, None
        elif depth >= self.level-1:
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
                eval = self.minimax(temp_board, False, depth + 1, alpha, beta)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
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
                eval = self.minimax(temp_board, True, depth + 1, alpha, beta)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
        
    def eval(self, board):
        if self.level == 1:
            eval = 'random'
            move = self.rnd(board)
        else:
            eval, move = self.minimax(board, False, 0, -100, +100)

        print('AI has chosen to move the piece at pos: ', move.initial.row, ',', move.initial.col, 'to pos: ', move.final.row, ',',\
            move.final.col, 'with the eval of: ', eval)
        return move
