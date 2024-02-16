import chess
import mcts, minimax
from draw import ChessView

from transposition_table import TranspositionTable

def run(chessView):
    chessView.run()

if __name__ == "__main__":
    tt = TranspositionTable()
    mm = minimax.Minimax(tt)
    monte_carlo = mcts.MCTS(tt, mm)
    board = chess.Board()
    chessView = ChessView(board, chess.BLACK, monte_carlo, 1000, 1000)
    run(chessView)