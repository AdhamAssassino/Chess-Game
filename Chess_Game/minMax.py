import random
import numpy as np


class MinMax:
    CHECKMATE = 1000
    STALEMATE = 0

    def __init__(self):
        self.piece_score = {"K": 0, "Q": 10, "R": 5, "B": 3.5, "N": 3, "P": 1}
        self.piece_position_scores = self.generate_piece_position_scores()

    def generate_piece_position_scores(self):
        random_numbers = lambda: [random.random() for _ in range(8)]
        return {
            "wN": np.array([random_numbers() for _ in range(8)]),
            "bN": np.flip(np.array([random_numbers() for _ in range(8)]), axis=0),
            "wB": np.array([random_numbers() for _ in range(8)]),
            "bB": np.flip(np.array([random_numbers() for _ in range(8)]), axis=0),
            "wQ": np.array([random_numbers() for _ in range(8)]),
            "bQ": np.flip(np.array([random_numbers() for _ in range(8)]), axis=0),
            "wR": np.array([random_numbers() for _ in range(8)]),
            "bR": np.flip(np.array([random_numbers() for _ in range(8)]), axis=0),
            "wP": np.array([random_numbers() for _ in range(8)]),
            "bP": np.flip(np.array([random_numbers() for _ in range(8)]), axis=0)
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
            opponentMaxScore = max(-turnMultiplier * self.CHECKMATE,
                                   *[self.scoreMaterial(gs.board) for opponentsMove in gs.getValidMoves()])
            opponentMinMaxScore, bestPlayerMove = min(opponentMaxScore, opponentMinMaxScore), playerMove
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
