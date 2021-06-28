class Piece():
    def __init__(self, id, n, pos, pos):
        self.id = id
        self.n = n
        self.pos = pos
        self.pos_list = []

class Player():
    def __init__(self, id):
        self.id = id
        #player's piece information
        self.pieces = None
        self.occupied_grid = None
        self.corners_grid = None
        self.adjacents_grid = None
        self.possible_grid = None