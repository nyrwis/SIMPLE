class Piece():
    def __init__(self, id, n, dim, pos):
        self.id = id
        self.n = n
        self.dim = dim
        self.pos = pos
        self.pos_list = []


class Pos():
    def __init__(self, h, w, loc):
        self.h = h
        self.w = w
        #self.loc = [[0 for i in range(h)] for j in range(w)]
        #tuple for point of piece as list
        self.loc = 


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player():
    def __init__(self, id):
        self.id = id


    def setup(self, board_length, piece_num):
        self.pieces = [0 for i in range(piece_num)]
        self.occupied = [[0 for i in range(board_length)] for j in range(board_length)]
        self.corners = [[0 for i in range(board_length)] for j in range(board_length)]
        self.adjacents = [[0 for i in range(board_length)] for j in range(board_length)]
        self.possible = [[0 for i in range(board_length)] for j in range(board_length)]
        
        self.possible[0][0] = self.possible[0][-1] = self.possible[-1][0] = self.possible[-1][-1] = 1


    def update(self, action):
        occupied_update(action)
        corners_update()
        adjacents_update()
        possible_update()


    def occupied_update(self):
        
    def corners_update(self):

    def adjacents_update(self):

    def possible_update(self):
