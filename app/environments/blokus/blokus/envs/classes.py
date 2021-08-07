import numpy as np

class Piece():
    def __init__(self, info):
        self.id = info[0]
        self.n = info[1]
        self.dim = info[2]
        self.dim_size = self.dim[0]*self.dim[1]
        self.pos = info[3]
        self.pos_list = []
        num=1
        for p in info[4]:
            self.pos_list.append(Pos(num, p))
            num+=1


class Pos():
    def __init__(self, id, info):
        self.id = id
        self.h = info[0]
        self.w = info[1]
        #tuple for point of piece as list
        self.loc = info[2]


class Player():
    def __init__(self, id):
        self.id = id


    def setup(self, board_length, piece_num):
        self.pieces = np.ones(piece_num, dtype=int)
        self.occupied = np.zeros((board_length, board_length), dtype=int)
        self.corners = np.zeros((board_length, board_length), dtype=int)
        self.adjacents = np.zeros((board_length, board_length), dtype=int)
        self.possible = np.zeros((board_length, board_length), dtype=int)
        
        if self.id==1:
            self.possible[0][0] = 1
        elif self.id==2:
            self.possible[7][7] = 1
        #self.possible[0][0] = self.possible[0][7] = self.possible[7][0] = self.possible[7][7] = 1


    def update(self, action, board):
        self.delete_piece(action)
        self.occupied_update(action)
        self.corners_update(action)
        self.adjacents_update(action)
        self.possible_update(action, board)


    def delete_piece(self, action):
        id = action[0]
        self.pieces[id-1] = 0
        print(id)


    def occupied_update(self, action):
        id, loc_h, loc_w, pos = action[0], action[1], action[2], action[3]
        occupied_update_loc = []
        i,j = loc_h-(pos.h-1), loc_w-(pos.w-1)
        for pos in pos.loc:
            grid = list(pos)
            #print(grid[0]+i, grid[1]+j)
            self.occupied[grid[0]+i, grid[1]+j] = 1


    def corners_update(self, action):
        id, loc_h, loc_w, pos = action[0], action[1], action[2], action[3]
        occupied_update_loc = []
        i,j = loc_h-(pos.h-1), loc_w-(pos.w-1)
        dir = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for pos in pos.loc:
            grid = [pos[0]+i, pos[1]+j]
            for d in dir:
                x = grid[0]+d[0]
                y =  grid[1]+d[1]
                if x>=0 and x<8 and y>=0 and y<8:
                    self.corners[x, y] = 1
            


    def adjacents_update(self, action):
        id, loc_h, loc_w, pos = action[0], action[1], action[2], action[3]
        occupied_update_loc = []
        i,j = loc_h-(pos.h-1), loc_w-(pos.w-1)
        dir = [(1,0), (0,1), (-1,0), (0,-1)]
        for pos in pos.loc:
            grid = [pos[0]+i, pos[1]+j]
            for d in dir:
                x = grid[0]+d[0]
                y =  grid[1]+d[1]
                if x>=0 and x<8 and y>=0 and y<8:
                    self.adjacents[x, y] = 1


    def possible_update(self, action, board):
        self.possible = self.corners - self.occupied - self.adjacents - board
        np.clip(self.possible, 0, 1, out=self.possible)

