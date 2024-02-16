class TranspositionTable:
    def __init__(self):
        self.table = {}

    def lookup(self, key):
        return self.table.get(key)

    def store(self, entry):
        self.table[entry.key] = entry

    def getEntry(self, depth, key):
        entry = self.lookup(key)
        if entry and entry.depth >= depth:
            return entry
        return None
        

    def update(self, board, depth, value, entry):
        if value > entry.evaluation:
            self.store(Entry(
                key=board.fen(),
                depth=depth,
                evaluation=value
            ))


class Entry:
    def __init__(self, key, depth, evaluation):
        self.key = key
        self.depth = depth
        self.evaluation = evaluation