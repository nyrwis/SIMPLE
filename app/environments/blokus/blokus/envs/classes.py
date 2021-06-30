class Piece():
    def __init__(self, id, n, dim, pos, poss):
        self.id = id
        self.n = n
        self.dim = dim
        self.pos = pos
        self.pos_list = []
        for p in poss:
            self.pos_list.append(Pos(*p))

    def return_pos(self, num):
        return pos_list[num]


class Pos():
    def __init__(self, w, h, loc):
        self.h = h
        self.w = w
        #self.loc = [[0 for i in range(h)] for j in range(w)]
        #tuple for point of piece as list
        self.loc = loc


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
        self.occupied_update(action)
        self.corners_update(action)
        self.adjacents_update(action)
        self.possible_update(action)


    def delete_piece(self, action):
        id, _, _ , _ = *action
        self.pieces[id] = 0


    def occupied_update(self, action):
        id, loc_w, loc_h, pos = *action
        occupied_update_loc = []
        y,x = (h-1)+loc.h, (w-1)+loc.w
        for pos in pos.loc:
            grid = list(pos)
            self.occupied[grid[0]+y, grid[1]+x] = 1


    def corners_update(self, action):
        id, loc_w, loc_h, pos = *action
        occupied_update_loc = []
        y,x = (h-1)+loc.h, (w-1)+loc.w
        for pos in pos.loc:
            grid = list(pos)
            self.occupied[grid[0]+y+1, grid[1]+x+1] = self.occupied[grid[0]+y+1, grid[1]+x-1] = self.occupied[grid[0]+y-1, grid[1]+x+1] = self.occupied[grid[0]+y-1, grid[1]+x-1] = 1


    def adjacents_update(self, action):
        id, loc_w, loc_h, pos = *action
        occupied_update_loc = []
        y,x = (h-1)+loc.h, (w-1)+loc.w
        for pos in pos.loc:
            grid = list(pos)
            self.occupied[grid[0]+y+1, grid[1]+x] = self.occupied[grid[0]+y, grid[1]+x+1] = self.occupied[grid[0]+y-1, grid[1]+x] = self.occupied[grid[0]+y, grid[1]+x-1] = 1


    def possible_update(self, action):
        for i in 

