from math import sqrt, log

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
 
    def add_child(self, move):
        state = self.state.copy()
        state.push(move)
        child = Node(state, parent=self, move=move)
        self.children.append(child)
        return child
 
    def update(self, result):
        self.visits += 1
        self.wins += result
 
    def uct_score(self, C=2):
        if self.visits == 0:
            return float('inf') # UCB for unvisited node
        win_ratio = self.wins / self.visits
        exploration = sqrt(C * log(self.parent.visits) / self.visits)
        return win_ratio + exploration