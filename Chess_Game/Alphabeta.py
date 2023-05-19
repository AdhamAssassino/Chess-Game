import random
import numpy as np


class AlphaBeta:
    CHECKMATE = 1000
    STALEMATE = 0
    DEPTH = 3

    def __init__(self):
        self.piece_score = {"K":0, "Q": 10, "R": 5, "B": 3.5, "N": 3, "P": 1}

        self.knight_scores = np.array([self.randomNumbers() for _ in range(8)])
        self.bishop_scores = np.array([self.randomNumbers() for _ in range(8)])
        self.rook_scores = np.array([self.randomNumbers() for _ in range(8)])
        self.queen_scores = np.array([self.randomNumbers() for _ in range(8)])
        self.pawn_scores = np.array([self.randomNumbers() for _ in range(8)])

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

    def randomNumbers(self):
        return [random.random() for _ in range(8)]

    def findBestMove(self, game_state, valid_moves, return_queue):
        global next_move
        next_move = None
        random.shuffle(valid_moves)
        self.findMoveNegaMaxAlphaBeta(game_state, valid_moves, self.DEPTH, -self.CHECKMATE, self.CHECKMATE,
                                      1 if game_state.white_to_move else -1)
        return_queue.put(next_move)

    def findMoveNegaMaxAlphaBeta(self, game_state, valid_moves, depth, alpha, beta, turn_multiplier):
        global next_move
        if depth == 0:
            return turn_multiplier * self.scoreBoard(game_state)
        max_score = -self.CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            score = -self.findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
            if score > max_score:
                max_score = score
                if depth == self.DEPTH:
                    next_move = move
            game_state.undoMove()
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score

    def scoreBoard(self, game_state):
        """
        Score the board. A positive score is good for white, a negative score is good for black.
        """
        if game_state.checkmate:
            if game_state.white_to_move:
                return -self.CHECKMATE  # black wins
            else:
                return self.CHECKMATE  # white wins
        elif game_state.stalemate:
            return self.STALEMATE
        score = 0
        for row in range(len(game_state.board)):
            for col in range(len(game_state.board[row])):
                piece = game_state.board[row][col]
                if piece != "--":
                    piece_position_score = 0
                    if piece[1] != "K":
                        piece_position_score = self.piece_position_scores[piece][row][col]
                    if piece[0] == "w":
                        score += self.piece_score[piece[1]] + piece_position_score
                    if piece[0] == "b":
                        score -= self.piece_score[piece[1]] + piece_position_score

        return score

    def findRandomMove(valid_moves):
        """
        Picks and returns a random valid move.
        """
        return random.choice(valid_moves)
