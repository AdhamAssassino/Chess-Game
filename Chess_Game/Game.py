import pygame
import pygame as py
import sys
from board import *
from constimages import *
from minMax import *
from Alphabeta import *
from constvaribles import *
from multiprocessing import Process, Queue


class Game:
    def __init__(self):
        self.const = Const()
        self.img = Images()
        global piece_images

    def Game(self):
        user_input = input("what's your algorithm you wants to play it").upper()
        piece_images = self.img.imagesSetter()
        py.init()
        screen = py.display.set_mode((self.const.getWidth(), self.const.getHeight()))
        clock = py.time.Clock()
        screen.fill(py.Color("white"))
        game_state = Board()
        valid_moves = game_state.getValidMoves()
        move_made = False  # flag variable for when a move is made
        self.img.imagesSetter()  # do this only once before while loop

        square_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
        player_clicks = []  # this will keep track of player clicks (two tuples)
        game_over = False
        ai_thinking = False
        move_undone = False
        move_finder_process = None
        player_one = True  # if a human is playing white, then this will be True, else False
        player_two = False  # if a human is playing white, then this will be True, else False
        min_max = MinMax()
        alpha = AlphaBeta()
        while True:
            human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
            for e in py.event.get():
                if e.type == py.QUIT:
                    py.quit()
                    sys.exit()
                # mouse handler
                elif e.type == py.MOUSEBUTTONDOWN:
                    if not game_over:
                        location = py.mouse.get_pos()  # (x, y) location of the mouse
                        col = location[0] // self.const.getSize()
                        row = location[1] // self.const.getSize()
                        if square_selected == (row, col) or col >= 8:  # user clicked the same square twice
                            square_selected = ()  # deselect
                            player_clicks = []  # clear clicks
                        else:
                            square_selected = (row, col)
                            player_clicks.append(square_selected)  # append for both 1st and 2nd click
                        if len(player_clicks) == 2 and human_turn:  # after 2nd click
                            move = Move(player_clicks[0], player_clicks[1], game_state.board)
                            for i in range(len(valid_moves)):
                                if move == valid_moves[i]:
                                    game_state.makeMove(valid_moves[i])
                                    move_made = True
                                    square_selected = ()  # reset user clicks
                                    player_clicks = []
                            if not move_made:
                                player_clicks = [square_selected]

                # key handler
                elif e.type == py.KEYDOWN:
                    if e.key == py.K_BACKSPACE:  # undo when 'z' is pressed
                        game_state.undoMove()
                        move_made = True
                        animate = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
                    if e.key == py.K_r:  # reset the game when 'r' is pressed
                        game_state = Board()
                        valid_moves = game_state.getValidMoves()
                        square_selected = ()
                        player_clicks = []
                        move_made = False
                        game_over = False
                        if ai_thinking:
                            move_finder_process.terminate()
                            ai_thinking = False
                        move_undone = True
            if user_input == 'MINMAX':
                if not game_over and not human_turn and not move_undone:
                    if not ai_thinking:
                        ai_thinking = True
                        return_queue = Queue()  # used to pass data between threads
                        move_finder_process = Process(target=min_max.findBestMove,
                                                      args=(game_state, valid_moves, return_queue))
                        move_finder_process.start()

                    if not move_finder_process.is_alive():
                        ai_move = return_queue.get()
                        if ai_move is None:
                            ai_move = min_max.findRandomMove(valid_moves)
                        game_state.makeMove(ai_move)
                        move_made = True
                        ai_thinking = False

            elif user_input == 'ALPHA':
                if not game_over and not human_turn and not move_undone:
                    if not ai_thinking:
                        ai_thinking = True
                        return_queue = Queue()  # used to pass data between threads
                        move_finder_process = Process(target=alpha.findBestMove,
                                                      args=(game_state, valid_moves, return_queue))
                        move_finder_process.start()
                    if not move_finder_process.is_alive():
                        ai_move = return_queue.get()
                        if ai_move is None:
                            ai_move = alpha.findRandomMove(valid_moves)
                        game_state.makeMove(ai_move)
                        move_made = True
                        ai_thinking = False

            if move_made:
                valid_moves = game_state.getValidMoves()
                move_made = False
                move_undone = False

            self.drawGameState(screen, game_state, valid_moves, square_selected, piece_images)

            if game_state.checkmate:
                game_over = True
                if game_state.white_to_move:
                    game_state.drawEndGameText(screen, "Black wins by checkmate")
                else:
                    game_state.drawEndGameText(screen, "White wins by checkmate")

            elif game_state.stalemate:
                game_over = True
                game_state.drawEndGameText(screen, "Stalemate")

            clock.tick(self.const.getMax_fps())
            py.display.flip()

    def drawGameState(self, screen, game_state, valid_moves, square_selected, pieces_images):
        game_state.drawBoard(screen)  # draw squares on the board
        game_state.highlightSquares(screen, game_state, valid_moves, square_selected)
        game_state.drawPieces(screen, pieces_images)  # draw pieces on top of those squares
