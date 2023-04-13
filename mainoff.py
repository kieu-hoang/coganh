import pygame
import sys
import time

from const import *
from game import Game
from square import Square
from move import Move
from button import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cờ gánh')

font = pygame.font.SysFont("arialblack", 20)
TEXT_COL = (255,255,255)
#load button images
play1_img = pygame.image.load("images/1p.png").convert_alpha()
play2_img = pygame.image.load("images/2p.png").convert_alpha()
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()

#create button instances
play1_button = Button(WIDTH/4 - play1_img.get_width()/2, HEIGHT/4 - play1_img.get_height()/2, play1_img, 1)
play2_button = Button(WIDTH/4*3 - play2_img.get_width()/2, HEIGHT/4 - play2_img.get_height()/2, play2_img, 1)
resume_button = Button(WIDTH/2 - resume_img.get_width()/2, HEIGHT/4 - resume_img.get_height()/2, resume_img, 1)
options_button = Button(WIDTH/2 - options_img.get_width()/2, HEIGHT/2 - options_img.get_height()/2, options_img, 1)
quit_button = Button(WIDTH/2 - quit_img.get_width()/2, HEIGHT*3/4 - quit_img.get_height()/2, quit_img, 1)

clock = pygame.time.Clock()
class Main:
    def __init__(self):
        pygame.init()
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #pygame.display.set_caption('Cờ gánh')
        self.game = Game()
    
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x,y))
            
    def mainloop(self):
        clock.tick(60)
        level = 1
        # screen = self.screen
        game = self.game
        board = self.game.board 
        dragger = self.game.dragger
        ai = self.game.ai
        
        run = True
        while run:
            screen.fill(BG_COLOR)
            if game.running == True and game.paused == False:
                game.show_lines(screen)
                game.show_pieces(screen)
                self.draw_text("Press SPACE to pause", font, TEXT_COL, WIDTH/2 - 120, 720)
                self.draw_text(f"{game.next_player}'s turn", font, TEXT_COL, 200, 15)
                if game.gamemode == 'ai':
                    self.draw_text(f"Level: {ai.level}", font, TEXT_COL, 50, 15)
                if board.new != True:
                    x1, y1, x2, y2 = board.last_move.to_num()
                    # color
                    color1 = (180, 180, 180)
                    # rect
                    rect1 = (y1 * SQSIZE + SQSIZE//4, x1 * SQSIZE+ SQSIZE//4, SQSIZE//2, SQSIZE//2)
                    rect2 = (y2 * SQSIZE+ SQSIZE//4, x2 * SQSIZE+ SQSIZE//4, SQSIZE//2, SQSIZE//2)
                    # blit
                    pygame.draw.rect(screen, color1, rect1, width=3)
                    pygame.draw.rect(screen, color1, rect2, width=3)
            
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
                                board.calc_value()
                                if game.isover():
                                    if game.gamemode == 'ai' and game.winner == 'blue':
                                        level += 1
                                        self.game = Game(level)
                                        game = self.game
                                        board = self.game.board
                                        dragger = self.game.dragger
                                        ai = self.game.ai
                                        game.running = True
                                    else:
                                        game.running = False
                                game.next_turn()
                        
                        dragger.undrag_piece()
                    
                    # key press
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            level = 1
                            game.reset()
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            ai = self.game.ai
                        if event.key == pygame.K_SPACE:
                            game.paused = True
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                if game.gamemode == 'ai' and game.next_player == ai.player and game.running:
                    # show methods
                    screen.fill(BG_COLOR)
                    game.show_lines(screen)
                    game.show_pieces(screen)
                    pygame.display.update()
                    
                    move = ai.eval(board)
                    game.make_move(move)
                    # show methods
                    screen.fill(BG_COLOR)
                    game.show_lines(screen)
                    game.show_pieces(screen)
                board.calc_value()
                if game.isover():
                    if game.gamemode == 'ai' and game.winner == 'blue':
                        level += 1
                        self.game = Game(level)
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        ai = self.game.ai
                        ai.level_up()
                    else:
                        game.running = False 
            elif game.running == False and game.paused == False:
                if play1_button.draw(screen):
                    game.running = True
                    
                if play2_button.draw(screen):
                    game.change_gamemode()
                    game.running = True
                    
                if options_button.draw(screen):
                    pass
                if quit_button.draw(screen):
                    run = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
            elif game.paused == True and game.running == True:
                if resume_button.draw(screen):
                    game.paused = False
                if options_button.draw(screen):
                    pass
                if quit_button.draw(screen):
                    run = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
            pygame.display.update()
        pygame.quit()
        sys.exit()
        
main = Main()
main.mainloop()    
