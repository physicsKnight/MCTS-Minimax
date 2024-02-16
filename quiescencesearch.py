from evaluation import evaluate

def quiescence_search(board, alpha, beta):
    stand_pat = evaluate(board)
    if stand_pat >= beta:
        return beta # beta cutoff
    if stand_pat > alpha:
        alpha = stand_pat
        
    for move in get_captures_and_promotions(board):
        board.push(move)  
        score = -quiescence_search(board, -beta, -alpha)
        board.pop()
        
        if score >= beta:
            return beta # beta cutoff
        if score > alpha:   
            alpha = score

    return alpha

def get_captures_and_promotions(board):
    moves = []
    for move in board.legal_moves:
        if board.is_capture(move) or board.gives_check(move): 
            moves.append(move)
            
    return moves