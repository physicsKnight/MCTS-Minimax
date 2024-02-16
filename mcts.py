import random
 
from node import Node
from evaluation import *

class MCTS:
    def __init__(self, tt, mm, minimax=False):
        self.tt = tt
        self.mm = mm
        self.minimax = False

    def select_leaf(self, node: Node):
        # traverse the tree in terms of
        # highest UCT score
        while node.children:
            node = max(node.children, key=lambda x: x.uct_score())
        return node

    def expand(self, node: Node):
        # Check for terminal state
        if node.state.is_game_over():
            return node
    
        # iterate through all the legal moves
        moves = list(node.state.legal_moves)
        if not moves:  # No legal moves, it's a terminal state
            return node
        
        for move in moves:
            # if move not in [c.state for c in node.children]:
            node.add_child(move)
        
        return random.choice(node.children)

    def simulate(self, node: Node):
        def evaluate(state, current_player):
            current = state.turn == current_player
            if state.is_checkmate():
                return 1000 if current else -1000
            else:
                player_colour = 'white' if current else 'black'
                return evaluate_board(state, player_colour)
    
        if self.minimax:
            move, min_eval = self.mm.predict_iddfs(node, max_depth=1)
            if min_eval is not None:
                return min_eval

        curr_state = node.state.copy()
        while not is_terminal(curr_state) and curr_state.ply() < 50:
            legal_moves = list(curr_state.legal_moves)
            move = random.choice(legal_moves)
            curr_state.push(move)
    
        # return state.result()  # 1 for win, 0 for loss, 0.5 for draw
        return evaluate(curr_state, node.state.turn)
    
    def backpropagate(self, node: Node, reward: int):
        while node is not None:
            node.update(reward)
            node = node.parent

    def execute_best(self, node: Node):
        best_child = max(node.children, key=lambda x: (x.wins / x.visits, x.visits))  # Prioritize win ratio, then visits
        return best_child.move

    def execute_best_minimax(self, node: Node):
        best_child = max(node.children, key=lambda x: (x.wins / x.visits, x.visits))  # Prioritize win ratio, then visits
        minimax_move, min_eval = self.mm.predict_iddfs(node, max_depth=3, choices=best_child.parent.children)
        for child in best_child.parent.children:
            if child.move == minimax_move:
                minimax_child = child
                break

        # minimax move already exists
        if minimax_child:
            self.backpropagate(minimax_child, min_eval)
            best = max(best_child, minimax_child, key=lambda x: (x.wins / x.visits, x.visits))
            print(f"Best move: {best.move}")
            return best.move
        
        # Minimax move not in tree, return best child and add it to tree
        minimax_child = node.parent.add_child(minimax_child)
        self.backpropagate(minimax_child, min_eval)
        print(f"best move: {minimax_move}")
        return minimax_move
    
    def predict(self, root: Node, iterations=100, minimax=False):
        self.minimax = minimax

        print("AI thinking...")
        for i in range(iterations):
            print(f"Iteration: {i+1}/{iterations}", end='\r')
            # go to leaf node based on UCT score
            # add a child node to the leaf node
            # simulate the game from the child node
            # backpropagate the reward from the child node to the root
            leaf = self.select_leaf(root) # selection
            child = self.expand(leaf) # expansion
            reward = self.simulate(child) # simulation
            self.backpropagate(child, reward) # backpropagation
        
        return self.execute_best(root)