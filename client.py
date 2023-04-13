import subprocess
import sys
import get_pip

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

try:
    print("[GAME] Trying to import pygame")
    import pygame
except:
    print("[EXCEPTION] Pygame not installed")

    try:
        print("[GAME] Trying to install pygame via pip")
        import pip
        install("pygame")
        print("[GAME] Pygame has been installed")
    except:
        print("[EXCEPTION] Pip not installed on system")
        print("[GAME] Trying to install pip")
        get_pip.main()
        print("[GAME] Pip has been installed")
        try:
            print("[GAME] Trying to install pygame")
            import pip
            install("pygame")
            print("[GAME] Pygame has been installed")
        except:
            print("[ERROR 1] Pygame could not be installed")


import pygame
import os
import time
from network import Network
from dragger import *
from square import Square
from move import Move
import pickle
from button import *
from const import *

pygame.font.init()

turn = "blue"
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cờ gánh')
screen.fill(BG_COLOR)

font = pygame.font.SysFont("arialblack", 20)
TEXT_COL = (255,255,255)
#load button images
play_img = pygame.image.load("images/play.png").convert_alpha()
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()

#create button instances
play_button = Button(WIDTH/2 - play_img.get_width()/2, HEIGHT/4 - play_img.get_height()/2, play_img, 1)
resume_button = Button(WIDTH/2 - resume_img.get_width()/2, HEIGHT/4 - resume_img.get_height()/2, resume_img, 1)
options_button = Button(WIDTH/2 - options_img.get_width()/2, HEIGHT/2 - options_img.get_height()/2, options_img, 1)
quit_button = Button(WIDTH/2 - quit_img.get_width()/2, HEIGHT*3/4 - quit_img.get_height()/2, quit_img, 1)

def menu_screen(win, name):
    global bo
    run = True
    offline = False

    while run:
        win.fill(BG_COLOR)
        small_font = pygame.font.SysFont("comicsans", 30)  
        if offline:
            off = small_font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))
            win.blit(off, (WIDTH / 2 - off.get_width() / 2, HEIGHT/2 - off.get_height() / 2))     
                 
        if play_button.draw(screen):
            bo.change_gamemode()
            bo.running = True
            
        if options_button.draw(screen):
            pass
        if quit_button.draw(screen):
            run = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    bo = connect()
                    run = False
                    main()
                    break
                except:
                    print("Server Offline")
                    offline = True
    
def redraw_gameWindow(win, bo, p1, p2, color, ready):
    # win.blit(board, (0, 0))
    # bo.draw(win, color)
    win.fill(BG_COLOR)
    bo.show_lines(win)
    bo.show_pieces(win)
    if bo.board.new != True:
        x1, y1, x2, y2 = bo.board.last_move.to_num()
        # color
        color1 = (180, 180, 180)
        # rect
        rect1 = (y1 * SQSIZE + SQSIZE//4, x1 * SQSIZE+ SQSIZE//4, SQSIZE//2, SQSIZE//2)
        rect2 = (y2 * SQSIZE+ SQSIZE//4, x2 * SQSIZE+ SQSIZE//4, SQSIZE//2, SQSIZE//2)
        # blit
        pygame.draw.rect(win, color1, rect1, width=3)
        pygame.draw.rect(win, color1, rect2, width=3)
        
    if bo.dragger.dragging:
        bo.show_hover(win)
        bo.dragger.update_blit(win)

    formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    if int(p1%60) < 10:
        formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    if int(p2%60) < 10:
        formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("comicsans", 20)
    try:
        txt = font.render(bo.p1Name + "\'s Time: " + str(formatTime1), 1, (255, 255, 255))
        txt2 = font.render(bo.p2Name + "\'s Time: " + str(formatTime2), 1, (255,255,255))
    except Exception as e:
        print(e)
    win.blit(txt, (520,10))
    win.blit(txt2, (520, 700))
    if bo.paused == False:
        txt = font.render("Press SPACE to pause", 1, (255, 255, 255))
        win.blit(txt, (10, 20))
    else:
        txt = font.render("Paused! Waiting...", 1, (255, 255, 255))
        win.blit(txt, (10, 20))

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        win.blit(txt3, (WIDTH/2-txt3.get_width()/2, 10))

    if not ready:
        show = "Waiting for Player"
        if color == "s":
            show = "Waiting for Players"
        font = pygame.font.SysFont("comicsans", 50)
        txt = font.render(show, 1, (255, 0, 0))
        win.blit(txt, (WIDTH/2 - txt.get_width()/2, HEIGHT/2 - txt.get_height()/2))

    if not color == "s":
        font = pygame.font.SysFont("comicsans", 30)
        if color == "red":
            txt3 = font.render("YOU ARE RED", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))
        else:
            txt3 = font.render("YOU ARE BLUE", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 10))

        if bo.next_player == color:
            txt3 = font.render("YOUR TURN", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 700))
        else:
            txt3 = font.render("THEIR TURN", 1, (255, 0, 0))
            win.blit(txt3, (WIDTH / 2 - txt3.get_width() / 2, 700))
            
    pygame.display.update()


def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)
    txt = font.render(text,1, (255,255,0))
    win.blit(txt, (WIDTH / 2 - txt.get_width() / 2, HEIGHT/2 - txt.get_height()/2))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False
                
def click(pos):
    posX, posY = pos

    x = posX // SQSIZE
    y = posY // SQSIZE
    return x,y 


def connect():
    global n
    n = Network()
    return n.board


def main():
    global turn, bo, name

    color = bo.start_user
    count = 0

    bo = n.send("name " + name)
    clock = pygame.time.Clock()
    run = True

    while run:
        if not color == "s":
            p1Time = bo.time1
            p2Time = bo.time2
            if count == 60:
                bo = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(60)

        try:
            redraw_gameWindow(screen, bo, p1Time, p2Time, color, bo.running)
        except Exception as e:
            print(e)
            end_screen(screen, "Other player left")
            run = False
            break

        if not color == "s":
            if bo.isover():
                bo = n.send(f"winner {bo.winner}")
            elif p1Time <= 0:
                bo = n.send("winner red")
            elif p2Time <= 0:
                bo = n.send("winner blue")
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and color != "s":
                    # quit game
                    if color == "red":
                        bo = n.send("winner blue")
                    else:
                        bo = n.send("winner red")
                if event.key == pygame.K_SPACE and color != "s":
                    if bo.paused == False:
                        bo = n.send("pause")
                    else:
                        bo = n.send("not pause")
                    
                if event.key == pygame.K_RIGHT:
                    bo = n.send("forward")

                if event.key == pygame.K_LEFT:
                    bo = n.send("back")
            if event.type == pygame.MOUSEBUTTONDOWN and color != "s" and bo.paused == False:
                if color == bo.next_player and bo.running:
                    bo.dragger.update_mouse(event.pos)

                    clicked_row = bo.dragger.mouseY // SQSIZE
                    clicked_col = bo.dragger.mouseX // SQSIZE
                    # if clicked square has a piece ?
                    if bo.board.squares[clicked_row][clicked_col].has_piece():
                        piece = bo.board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == bo.next_player:
                            bo.board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            bo.dragger.save_initial(event.pos)
                            bo.dragger.drag_piece(piece)
                            # show methods 
                            screen.fill(BG_COLOR)
                            bo.show_lines(screen)
                            bo.show_pieces(screen)
            
            
            # mouse motion
            elif event.type == pygame.MOUSEMOTION:
                motion_row = event.pos[1] // SQSIZE
                motion_col = event.pos[0] // SQSIZE
                bo.set_hover(motion_row, motion_col)

                if bo.dragger.dragging:
                    bo.dragger.update_mouse(event.pos)
                    # show methods
                    screen.fill(BG_COLOR)
                    bo.show_lines(screen)
                    bo.show_pieces(screen)
                    bo.show_hover(screen)
                    bo.dragger.update_blit(screen)
            
            # click release
            elif event.type == pygame.MOUSEBUTTONUP and color != "s" and bo.paused == False:
                
                if bo.dragger.dragging and color == bo.next_player and bo.running:
                    bo.dragger.update_mouse(event.pos)

                    released_row = bo.dragger.mouseY // SQSIZE
                    released_col = bo.dragger.mouseX // SQSIZE

                    # create possible move
                    initial = Square(bo.dragger.initial_row, bo.dragger.initial_col)
                    final = Square(released_row, released_col)
                    move = Move(initial, final)

                    # valid move ?
                    if bo.board.valid_move(bo.dragger.piece, move):
                        # bo.board.move(bo.dragger.piece, move)
                        bo = n.send("movefrom " + str(bo.dragger.initial_col) + " " + str(bo.dragger.initial_row) + " " + color)
                        bo = n.send("moveto " + str(released_col) + " " + str(released_row) + " " + color)
                        # show methods
                        screen.fill(BG_COLOR)
                        bo.show_lines(screen)
                        bo.show_pieces(screen)
                        # next turn
                        bo.board.calc_value()        
                                          
        if bo.winner == "red":
            end_screen(screen, "Red is the Winner!")
            run = False
            
        elif bo.winner == "blue":
            end_screen(screen, "Blue is the winner")
            run = False
            
    n.disconnect()
    bo = 0
    menu_screen(screen)


name = input("Please type your name: ")
menu_screen(screen, name)
