import random
import numpy as np


class MinMax:
    CHECKMATE = 1000
    STALEMATE = 0

    def __init__(self):
        self.piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3.5, "N": 3, "P": 1}


        self.knight_scores = np.array([[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                                       [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                                       [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                                       [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                                       [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                                       [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                                       [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                                       [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]])

        self.bishop_scores = np.array([[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                                       [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                                       [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                                       [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                                       [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                                       [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                                       [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                                       [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]])

        self.rook_scores = np.array([[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
                                     [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
                                     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                                     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                                     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                                     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                                     [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
                                     [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]])

        self.queen_scores = np.array([[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                                      [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                                      [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                                      [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                                      [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                                      [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                                      [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                                      [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]])

        self.pawn_scores = np.array([[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
                                     [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
                                     [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
                                     [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
                                     [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
                                     [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
                                     [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
                                     [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]])

        self.piece_position_scores = {
            "wN": self.knight_scores,
            "bN": np.flip(self.knight_scores, axis=0),
            "wB": self.bishop_scores,
            "bB": np.flip(self.bishop_scores, axis=0),
            "wQ": self.queen_scores,
            "bQ": np.flip(self.queen_scores, axis=0),
            "wR": self.rook_scores,
            "bR": np.flip(self.rook_scores, axis=0),
            "wP": self.pawn_scores,
            "bP": np.flip(self.pawn_scores, axis=0)
        }


    def findRandomMove(self, validMoves):
        return random.choice(validMoves)

    def findBestMove(self, gs, validMoves, return_queue):
        turnMultiplier = 1 if gs.white_to_move else -1
        opponentMinMaxScore = self.CHECKMATE
        bestPlayerMove = None
        random.shuffle(validMoves)
        for playerMove in validMoves:
            gs.makeMove(playerMove)
            opponentsMoves = gs.getValidMoves()
            opponentMaxScore = -self.CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                if gs.checkmate:
                    score = -turnMultiplier * self.CHECKMATE
                elif gs.stalemate:
                    score = self.STALEMATE
                else:
                    score = -turnMultiplier * self.scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
            if opponentMaxScore < opponentMinMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = playerMove
            gs.undoMove()
        return_queue.put(bestPlayerMove)
        return bestPlayerMove

    def scoreMaterial(self, board):
        score = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if piece != "--":
                    piece_position_score = 0
                    if piece[1] != "K":
                        piece_position_score = self.piece_position_scores[piece][row][col]
                    score += self.piece_score[piece[1]] + (
                        piece_position_score if piece[0] == "w" else -piece_position_score)
        return score
