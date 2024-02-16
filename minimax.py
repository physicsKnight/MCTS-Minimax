from evaluation import *
from quiescencesearch import quiescence_search
import time
from node import Node

import multiprocessing.dummy
from transposition_table import TranspositionTable

class Minimax:
    def __init__(self, tt=None):
        self.tt = tt
        if tt is None:
            self.tt = TranspositionTable()
 
    def minimax(self, board, depth, alpha, beta, maximising):
        if depth <= 0 or is_terminal(board):
            return quiescence_search(board, alpha, beta)
    
        if maximising:
            return self.max_value(board, depth, alpha, beta)
        else:
            return self.min_value(board, depth, alpha, beta)

    def max_value(self, board, depth, alpha, beta):
        entry = self.tt.getEntry(depth, board.fen())
        if entry: return entry.evaluation
        
        best_value = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            value = self.minimax(board, depth-1, alpha, beta, False)
            best_value = max(best_value, value)
            if entry: entry.update(board, depth, value, entry)
            alpha = max(alpha, best_value)
            board.pop()
            if beta <= alpha:
                break
    
        return best_value
    
    def min_value(self, board, depth, alpha, beta):
        entry = self.tt.getEntry(depth, board.fen())
        if entry: return entry.evaluation

        best_value = float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = self.minimax(board, depth-1, alpha, beta, True)
            best_value = min(best_value, value)
            if entry: entry.update(board, depth, value, entry)
            beta = min(beta, best_value)
            board.pop()
            if beta <= alpha:
                break
    
        return best_value

    def eval_move(self, board, move, depth, maximising, alpha=float('-inf'), beta=float('inf')):
        board.push(move)
        eval_score = self.minimax(board, depth, alpha, beta, not maximising)
        board.pop()
        return eval_score

    def predict(self, board, depth, legal_moves, maximising=True):
        best_move = None
        best_eval = -float("inf") if maximising else float("inf")
        
        with multiprocessing.dummy.Pool(processes=4) as pool:
            results = [pool.apply_async(self.eval_move, (board.copy(), move, depth, maximising)) 
                    for move in legal_moves]
            scores = [r.get() for r in results]
            
            for move, score in zip(legal_moves, scores):
                if maximising:
                    if score > best_eval:
                        best_eval = score
                        best_move = move
                else:
                    if score < best_eval:
                        best_eval = score
                        best_move = move
                        
        return best_move, best_eval


    def predict_iddfs(self, root, max_depth=3, maximising=True, choices=None):
        board = root
        if isinstance(board, Node):
            board = board.state

        legal_moves = choices
        if choices is None:
            legal_moves = list(board.legal_moves)
        else:
            legal_moves = [n.move for n in legal_moves]
    
        best_move, best_eval = None, None
    
        for current_depth in range(1, max_depth + 1, 2):
            start_time = time.time()
            current_best_move, current_best_eval = self.predict(board, current_depth, legal_moves, maximising)
            elapsed_time = time.time() - start_time
    
            #print(f"Best move: {current_best_move}, Time: {elapsed_time} seconds")
    
            if elapsed_time > 5 or (current_depth > 1 and current_best_move == best_move):
                break  # Stop searching if time limit is reached or no significant improvement
    
            best_move = current_best_move  # Update the best move for the current depth
            best_eval = current_best_eval
    
        return best_move, best_eval
    