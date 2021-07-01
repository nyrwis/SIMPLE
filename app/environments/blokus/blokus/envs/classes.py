import numpy as np

class Piece():
    def __init__(self, id, n, dim, pos, poss):
        self.id = id
        self.n = n
        self.dim = dim
        self.dim_size = dim[0]*dim[1]
        self.pos = pos
        self.pos_list = []
        int num=1
        for p in poss:
            self.pos_list.append(num, Pos(*p))
            num+=1


class Pos():
    def __init__(self, id, h, w, loc):
        self.id = id
        self.h = h
        self.w = w
        #tuple for point of piece as list
        self.loc = loc


class Player():
    def __init__(self, id):
        self.id = id


    def setup(self, board_length, piece_num):
        self.pieces = np.ones(piece_num, dtype=int32)
        self.occupied = np.zeros((board_length, board_length), dtype=int32)
        self.corners = np.zeros((board_length, board_length), dtype=int32)
        self.adjacents = np.zeros((board_length, board_length), dtype=int32)
        self.possible = np.zeros((board_length, board_length), dtype=int32)
        
        self.possible[0][0] = self.possible[0][-1] = self.possible[-1][0] = self.possible[-1][-1] = 1


    def update(self, action, board):
        self.occupied_update(action)
        self.corners_update(action)
        self.adjacents_update(action)
        self.possible_update(action, board)


    def delete_piece(self, action):
        id, _, _, _ = *action
        self.pieces[id] = 0


    def occupied_update(self, action):
        id, loc_h, loc_w, pos = *action
        occupied_update_loc = []
        i,j = (h-1)+loc.h, (w-1)+loc.w
        for pos in pos.loc:
            grid = list(pos)
            self.occupied[grid[0]+i, grid[1]+j] = 1


    def corners_update(self, action):
        id, loc_w, loc_h, pos = *action
        occupied_update_loc = []
        i,j = (h-1)+loc.h, (w-1)+loc.w
        dir = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for pos in pos.loc:
            grid = [grid[0]+i, grid[1]+j]
            for d in dir:
                x = grid[0]+dir[0]
                y =  grid[1]+dir[1]
                if x>=0 and x<8 and y>=0 and y<8:
                    self.corners[x, y] = 1
            


    def adjacents_update(self, action):
        id, loc_w, loc_h, pos = *action
        occupied_update_loc = []
        i,j = (h-1)+loc.h, (w-1)+loc.w
        dir = [(1,0), (0,1), (-1,0), (0,-1)]
        for pos in pos.loc:
            grid = [grid[0]+i, grid[1]+j]
            for d in dir:
                x = grid[0]+dir[0]
                y =  grid[1]+dir[1]
                if x>=0 and x<8 and y>=0 and y<8:
                    self.corners[x, y] = 1


    def possible_update(self, action, board):
        self.possible = self.corners - self.occupied - self.adjacents - board
        np.clip(self.possible, 0, 1, out=self.possible)

