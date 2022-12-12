import pygame
import sys
import time

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Cờ gánh')
        self.game = Game()
        
    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board 
        dragger = self.game.dragger
        ai = self.game.ai
        
        while True:
            screen.fill(BG_COLOR)
            game.show_lines(screen)
            game.show_pieces(screen)
            
            if dragger.dragging:
                dragger.update_blit(screen)
                
            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            screen.fill(BG_COLOR)
                            game.show_lines(screen)
                            game.show_pieces(screen)
                
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        screen.fill(BG_COLOR)
                        game.show_lines(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            # show methods
                            screen.fill(BG_COLOR)
                            game.show_lines(screen)
                            game.show_pieces(screen)
                            # next turn
                            if game.isover():
                                game.running = False
                            game.next_turn()
                    
                    dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_g:
                        game.change_gamemode()
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        ai = self.game.ai
                        
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if game.gamemode == 'ai' and game.next_player == ai.player and game.running:
            
                pygame.display.update()
                move = ai.eval(board)
                game.make_move(move)
                # show methods
                screen.fill(BG_COLOR)
                game.show_lines(screen)
                game.show_pieces(screen)
                if game.isover():
                    game.running = False
            if game.isover():
                game.running = False            
            pygame.display.update()

main = Main()
main.mainloop()    
