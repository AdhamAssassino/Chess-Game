import pygame
import pygame as py
import sys

import randomAI
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
        move_made = False
        self.img.imagesSetter()
        square_selected = ()
        game_over = False
        ai_thinking = False
        move_undone = False
        move_finder_process = None
        PC = True
        PC2 = False
        min_max = MinMax()
        alpha = AlphaBeta()
        while True:
            human_turn = (game_state.white_to_move and PC) or (not game_state.white_to_move and PC2)
            for e in py.event.get():
                if e.type == py.QUIT:
                    py.quit()
                    sys.exit()

            if not game_over and human_turn:
                ai_move = self.findRandomMove(game_state.getValidMoves())
                game_state.makeMove(ai_move)
                move_made = True

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
        game_state.drawBoard(screen)
        game_state.highlightSquares(screen, game_state, valid_moves, square_selected)
        game_state.drawPieces(screen, pieces_images)

    def findRandomMove(self,valid_move):
        return valid_move[random.randint(0, len(valid_move) - 1)]
