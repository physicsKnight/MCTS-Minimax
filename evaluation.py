import chess
 
def is_terminal(state):
    return state.is_game_over() or state.is_stalemate()

pawn_table = [
 0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0,
]

knight_table = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50,
]

bishop_table = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20,
]

rook_table = [
  0,  0,  0,  0,  0,  0, 0,  0,
  5, 10, 10, 10, 10, 10, 10, 5,
 -5,  0,  0,  0,  0,  0, 0, -5,
 -5,  0,  0,  0,  0,  0, 0, -5,
 -5,  0,  0,  0,  0,  0, 0, -5,
 -5,  0,  0,  0,  0,  0, 0, -5,
 -5,  0,  0,  0,  0,  0, 0, -5,
  0,  0,  0,  5,  5,  0, 0,  0,
]

queen_table = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20,
]

king_table = [
-50,-40,-30,-20,-20,-30,-40,-50,
-30,-20,-10,  0,  0,-10,-20,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 30, 40, 40, 30,-10,-30,
-30,-10, 20, 30, 30, 20,-10,-30,
-30,-30,  0,  0,  0,  0,-30,-30,
-50,-30,-30,-30,-30,-30,-30,-50,
]

PIECE_VALUES = {
    chess.PAWN: 100, 
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500, 
    chess.QUEEN: 900,
    chess.KING: 20000 
}
 
PIECE_SQUARE_TABLES = {
    chess.PAWN: pawn_table,
    chess.KNIGHT: knight_table,
    chess.BISHOP: bishop_table,
    chess.ROOK: rook_table,
    chess.QUEEN: queen_table,
    chess.KING: king_table
}

def evaluate_board(state, player_colour):
    piece_values = {
        'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 10,
        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -10
    }

    total_score = 0
    for _, piece in state.piece_map().items():
        piece_value = piece_values.get(piece.symbol(), 0)
        if piece.color == player_colour:
            total_score += piece_value
        else:
            total_score -= piece_value

    return total_score

def evaluate(board):
    # Handle special cases concisely
    if board.is_game_over():
        return 9999 * board.turn
    
    if board.is_stalemate() or board.is_insufficient_material():
        return 0  # Draw

    # Calculate material difference efficiently
    piece_difference = sum(
        PIECE_VALUES[piece_type] * (len(board.pieces(piece_type, chess.WHITE)) - len(board.pieces(piece_type, chess.BLACK)))
        for piece_type in PIECE_VALUES
    )

    # Iterate through pieces and piece-square tables in a single loop
    total_score = 0
    for piece_type in PIECE_VALUES:
        piece_square_table = PIECE_SQUARE_TABLES[piece_type]
        for square in board.pieces(piece_type, chess.WHITE):
            total_score += piece_square_table[square]
        for square in board.pieces(piece_type, chess.BLACK):
            total_score -= piece_square_table[square]  # Reflect black's perspective

    return total_score + piece_difference * board.turn  # Factor in turn directly