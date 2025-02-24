# referenced code from https://github.com/DerekGloudemans/Blokus-Reinforcement-Learning

import gym
import numpy as np
from numba import jit

import config
import copy

from stable_baselines import logger

from .classes import Piece, Player


#information of each piece
#[id, num of spaces each piece cover, (num of possible grid location in a row, num of possible grid location in a column), possible position, (grid_h, grid_w, grid location)]
'''
p1 = [1, 1, 196, 1, [[1, 1, [(0, 0)]]]]
p2 = [2, 2, 182, 2, [[1, 2, [(0, 0), (0, 1)]], [2, 1, [(0, 0), (1, 0)]]]]
p3 = [3, 3, 169, 4, [[2, 2, [(0, 0), (0, 1), (1, 0)]], [2, 2, [(0, 0), (0, 1), (1, 1)]], [2, 2, [(0, 1), (1, 0), (1, 1)]], [2, 2, [(0, 0), (1, 0), (1, 1)]]]]
p4 = [4, 3, 168, 2, [[1, 3, [(0, 0), (0, 1), (0, 2)]], [3, 1, [(0, 0), (1, 0), (2, 0)]]]]
p5 = [5, 4, 169, 1, [[2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]]]]
p6 = [6, 4, 156, 4, [[2, 3, [(0, 1), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (1, 0), (1, 1), (2, 0)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 1)]], [3, 2, [(0, 1), (1, 0), (1, 1), (2, 1)]]]]
p7 = [7, 4, 154, 2, [[1, 4, [(0, 0), (0, 1), (0, 2), (0, 3)]], [4, 1, [(0, 0), (1, 0), (2, 0), (3, 0)]]]]
p8 = [8, 4, 156, 8, [[2, 3, [(0, 0), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (0, 1), (1, 0), (2, 0)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 2)]], [3, 2, [(0, 1), (1, 1), (2, 0), (2, 1)]], [2, 3, [(0, 2), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (1, 0), (2, 0), (2, 1)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 0)]], [3, 2, [(0, 0), (0, 1), (1, 1), (2, 1)]]]]
p9 = [9, 4, 156, 4, [[2, 3, [(0, 0), (0, 1), (1, 1), (1, 2)]], [3, 2, [(0, 1), (1, 0), (1, 1), (2, 0)]], [2, 3, [(0, 1), (0, 2), (1, 0), (1, 1)]], [3, 2, [(0, 0), (1, 0), (1, 1), (2, 1)]]]]
p10 = [10, 5, 143, 8, [[2, 4, [(0, 3), (1, 0), (1, 1), (1, 2), (1, 3)]], [4, 2, [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)]], [2, 4, [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)]], [4, 2, [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)]], [2, 4, [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)]], [4, 2, [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)]], [2, 4, [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)]], [4, 2, [(0, 1), (1, 1), (2, 1), (3, 0), (3, 1)]]]]
p11 = [11, 5, 144, 4, [[3, 3, [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)]], [3, 3, [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)]], [3, 3, [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]], [3, 3, [(0, 2), (1, 0), (1, 1), (1, 2), (2, 2)]]]]
p12 = [12, 5, 144, 4, [[3, 3, [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)]], [3, 3, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]], [3, 3, [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]], [3, 3, [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]]]]
p13 = [13, 5, 143, 8, [[2, 4, [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)]], [4, 2, [(0, 1), (1, 1), (2, 0), (2, 1), (3, 0)]], [2, 4, [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3)]], [4, 2, [(0, 1), (1, 0), (1, 1), (2, 0), (3, 0)]], [2, 4, [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1)]], [4, 2, [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)]], [2, 4, [(0, 2), (0, 3), (1, 0), (1, 1), (1, 2)]], [4, 2, [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)]]]]
p14 = [14, 5, 144, 4, [[3, 3, [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]], [3, 3, [(0, 1), (0, 2), (1, 1), (2, 0), (2, 1)]], [3, 3, [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)]], [3, 3, [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]]]]
p15 = [15, 5, 140, 2, [[5, 1, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]], [1, 5, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]]]]
p16 = [16, 5, 156, 8, [[3, 2, [(0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]], [2, 3, [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2)]], [3, 2, [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]], [3, 2, [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]], [2, 3, [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]]]]
p17 = [17, 5, 144, 4, [[3, 3, [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)]], [3, 3, [(0, 2), (1, 1), (1, 2), (2, 0), (2, 1)]], [3, 3, [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]], [3, 3, [(0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]]]]
p18 = [18, 5, 156, 4, [[3, 2, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]], [2, 3, [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]]]]
p19 = [19, 5, 144, 8, [[3, 3, [(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)]], [3, 3, [(0, 2), (1, 0), (1, 1), (1, 2), (2, 1)]], [3, 3, [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)]], [3, 3, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0)]], [3, 3, [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)]], [3, 3, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)]], [3, 3, [(0, 1), (1, 1), (1, 2), (2, 0), (2, 1)]], [3, 3, [(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)]]]]
p20 = [20, 5, 144, 1, [[3, 3, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]]]]
p21 = [21, 5, 143, 8, [[2, 4, [(0, 2), (1, 0), (1, 1), (1, 2), (1, 3)]], [4, 2, [(0, 0), (1, 0), (2, 0), (2, 1), (3, 0)]], [2, 4, [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1)]], [4, 2, [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)]], [2, 4, [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3)]], [4, 2, [(0, 0), (1, 0), (1, 1), (2, 0), (3, 0)]], [2, 4, [(0, 0), (0, 1), (0, 2), (0, 3), (1, 2)]], [4, 2, [(0, 1), (1, 1), (2, 0), (2, 1), (3, 1)]]]]


piece_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21]

piece_point = [1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

#accumulated possible action for each piece

action_marking = [0, 196, 560, 1236, 1572, 1741, 2365, 2673, 3921, 4545, 5689, 6265, 6841, 7985, 8561, 8841, 10089, 10665, 11289, 12441, 12585, 13729, 20000]
'''

p1 = [1, 1, 64, 1, [[1, 1, [(0, 0)]]]]
p2 = [2, 2, 56, 2, [[1, 2, [(0, 0), (0, 1)]], [2, 1, [(0, 0), (1, 0)]]]]
p3 = [3, 3, 49, 4, [[2, 2, [(0, 0), (0, 1), (1, 0)]], [2, 2, [(0, 0), (0, 1), (1, 1)]], [2, 2, [(0, 1), (1, 0), (1, 1)]], [2, 2, [(0, 0), (1, 0), (1, 1)]]]]
p4 = [4, 3, 48, 2, [[1, 3, [(0, 0), (0, 1), (0, 2)]], [3, 1, [(0, 0), (1, 0), (2, 0)]]]]
p5 = [5, 4, 49, 1, [[2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]]]]
p6 = [6, 4, 42, 4, [[2, 3, [(0, 1), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (1, 0), (1, 1), (2, 0)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 1)]], [3, 2, [(0, 1), (1, 0), (1, 1), (2, 1)]]]]
p7 = [7, 4, 40, 2, [[1, 4, [(0, 0), (0, 1), (0, 2), (0, 3)]], [4, 1, [(0, 0), (1, 0), (2, 0), (3, 0)]]]]
p8 = [8, 4, 42, 8, [[2, 3, [(0, 0), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (0, 1), (1, 0), (2, 0)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 2)]], [3, 2, [(0, 1), (1, 1), (2, 0), (2, 1)]], [2, 3, [(0, 2), (1, 0), (1, 1), (1, 2)]], [3, 2, [(0, 0), (1, 0), (2, 0), (2, 1)]], [2, 3, [(0, 0), (0, 1), (0, 2), (1, 0)]], [3, 2, [(0, 0), (0, 1), (1, 1), (2, 1)]]]]
p9 = [9, 4, 42, 4, [[2, 3, [(0, 0), (0, 1), (1, 1), (1, 2)]], [3, 2, [(0, 1), (1, 0), (1, 1), (2, 0)]], [2, 3, [(0, 1), (0, 2), (1, 0), (1, 1)]], [3, 2, [(0, 0), (1, 0), (1, 1), (2, 1)]]]]


piece_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

piece_point = [1, 2, 3, 3, 4, 4, 4, 4, 4]

action_marking = [0, 64, 176, 372, 468, 517, 685, 765, 1101, 1269, 10000]

class BlokusEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(BlokusEnv, self).__init__()
        self.name = 'blokus'
        self.manual = manual

        self.board_length = 8 #14
        self.n_players = 2
        self.board_shape = (self.board_length, self.board_length)
        self.piece_num = 9 #21
        self.possible_action_num = 1269 #13729
        self.action_space = gym.spaces.Discrete(self.possible_action_num)
        self.observation_space = gym.spaces.Box(0, 2, (self.board_length*self.board_length+self.possible_action_num,))
        self.verbose = verbose

    #@jit(nopython=True)
    @property
    def observation(self):
        #combine current board state, legal_action
        combined_observation = np.array(self.obs_regularize(self.obs_rotate(self.board, (self.current_player.id)%4*self.n_players), self.current_player.id+1)).flatten()
        x = np.array(self.legal_actions)
        combined_observation = np.append(combined_observation, x)

        return combined_observation

    def obs_rotate(self, board, ror):
        
        def obs_ror(input):

            ret = np.zeros((self.board_length, self.board_length), int)

            for i in range(self.board_length):
                for j in range(self.board_length):
                    ret[j][self.board_length-i-1] = input[i][j]

            return ret

        for n in range(ror%4):
            board = obs_ror(board)

        return board

    def obs_regularize(self, board, id):

        #board = np.zeros((self.board_length, self.board_length), int)
        #board = (board - id + 1)
        for i in range(self.board_length):
            for j in range(self.board_length):
                if (board[i][j])>0:
                    board[i][j] = board[i][j]-id + 1
                    if (board[i][j])<=0:
                        board[i][j] = board[i][j]+self.n_players

        return board

    #@jit(nopython=True)
    @property
    def legal_actions(self):
        legal_action = np.zeros(self.possible_action_num)
        for piece in [self.pieces[x] for x in range(self.piece_num) if self.current_player.pieces[x]==1]:
            for point in self.get_point(self.current_player.possible):
                for pos in piece.pos_list:
                    for i in range(pos.h):
                        for j in range(pos.w):
                            r = point[0]+i
                            c = point[1]+j
                            if self.inboard(pos.h, pos.w, r, c) and self.chk_possible(point,r,c,pos) and self.chk_occupied(r,c,pos) and self.chk_adjacent(r,c,pos):
                                action_num = action_marking[piece.id-1] + (pos.id-1)*piece.dim_size + (r-(pos.h-1))*(self.board_length-(pos.w-1)) + c-(pos.w-1)
                                legal_action[action_num] = 1
        return legal_action

    #@jit(nopython=True)
    def inboard(self, h, w, r, c):
        if r-(h-1)>=0 and c-(w-1)>=0 and r<=self.board_length-1 and c<=self.board_length-1:
            return True
        else:
            return False


    #@jit(nopython=True)
    def chk_possible(self, possible, r, c, pos):
        for grid in pos.loc:
            x,y = r-(pos.h-1)+grid[0], c-(pos.w-1)+grid[1]
            new_grid = [x, y]
            if new_grid==possible:
                    return True
        return False


    #@jit(nopython=True)
    def chk_occupied(self, r, c, pos):
        for grid in pos.loc:
            x,y = r-(pos.h-1)+grid[0], c-(pos.w-1)+grid[1]
            new_grid = [x, y]
            for point in self.get_point(self.board):
                if new_grid==point:
                    return False
        return True


    #@jit(nopython=True)
    def chk_adjacent(self, r, c, pos):
        for grid in pos.loc:
            x,y = r-(pos.h-1)+grid[0], c-(pos.w-1)+grid[1]
            new_grid = [x, y]
            for point in self.get_point(self.current_player.adjacents):
                if new_grid==point:
                    return False
        return True



    @property
    def current_player(self):
        return self.players[self.current_player_num]

    #@jit(nopython=True)
    def get_point(self, board):
        #original
        point_list = []
        for i in range(self.board_length):
            for j in range(self.board_length):
                if board[i][j] != 0:
                    point = [i, j]
                    point_list.append(point)
        return point_list

    #@jit(nopython=True)
    def calc_reward(self, board, id):
        #print(board)
        tot_point=0
        #print("id")
        for i in range(self.board_length):
            for j in range(self.board_length):
                if board[i][j] == id:
                    #print(i,j)
                    tot_point += 1
        return tot_point 


    def reset(self):
        #self.board = [[0 for i in range(self.board_length)] for j in range(self.board_length)]
        self.board = np.zeros((self.board_length, self.board_length), int)
        self.players = [Player(1), Player(2)]
        for player in self.players:
            player.setup(self.board_length, self.piece_num)
        self.left_players = [1, 1]
        self.pieces = []
        for piece in piece_list:
            self.pieces.append(Piece(piece))
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation

    def all_player_update(self):
        for player in self.players:
            player.turn_update(self.board)

    #@jit(nopython=True)
    def step(self, action):
        reward = [0,0]
        self.update_board(self.translate_action(action))
        self.current_player.update(self.translate_action(action), self.board)
        self.all_player_update()
        
        done = self.change_turn()
        
        
        '''
        done = self.change_turn()

        while not self.get_point(self.current_player.possible):
            self.left_players[self.current_player_num] = 0
            done = self.change_turn()
            if done==True:
                break
        '''

        #observation = self.observation

        if done:
            reward = self.choose_winner()

        return self.observation, reward, done, {}

    #@jit(nopython=True)
    def update_board(self, action):
        id, loc_h, loc_w, pos = action[0], action[1], action[2], action[3]
        h, w, loc = pos.h, pos.w, pos.loc
        for grid in loc:
            self.board[grid[0]+loc_h-(h-1)][grid[1]+loc_w-(w-1)] = self.current_player.id

    #@jit(nopython=True)
    def choose_winner(self):
        '''
        ans = 0
        score=[]
        for player in self.players:
            for i in range(self.piece_num):
                if player.pieces[i]==1:
                    ans+=piece_point[i]
            score.append(score)
            ans=0
        if score[0]>score[1]:
            score = [1,-1]
        elif score[0]<score[1]:
            score = [-1,1] 
        else:
            score = [0,0]
        '''
        ans = 0
        score=[]
        for i in range(2):
            score.append(self.calc_reward(self.board, i+1))
        #print(score) 
        if score[0]>score[1]:
            score = [1,-1]
        elif score[0]<score[1]:
            score = [-1,1] 
        else:
            score = [0,0]
        return score

    #@jit(nopython=True)
    def change_turn(self):
        '''
        done = True
        for i in range(self.n_players):
            if self.left_players[i] == 1:
                done = False
                break
            
        self.current_player_num = (self.current_player_num+1)%self.n_players
        while self.left_players[self.current_player_num]==0:
            self.current_player_num = (self.current_player_num+1)%self.n_players
        return done
        '''
        done = False
        self.current_player_num = (self.current_player_num+1)%self.n_players
        #print("legal action!!!!!")
        #print(self.legal_actions)
        if np.count_nonzero(self.legal_actions) == 0:
            done = True
            return done

        return done

    #@jit(nopython=True)
    def translate_action(self, action):
        #translated_action int->id,loc_h,loc_w,pos
        action+=1
        translated_action = []
        id = None
        for id in range(self.piece_num+1):
            if action > action_marking[id] and action <= action_marking[id+1]:
                action = action-action_marking[id]
                translated_action.append(id+1)
                break

        pos_num = (action-1) // self.pieces[id].dim_size + 1
        pos = self.pieces[id].pos_list[pos_num-1]
        loc_num = (action-1) % self.pieces[id].dim_size + 1
        loc_h = (loc_num-1) // (self.board_length-(pos.w-1)) + (pos.h-1)
        loc_w = (loc_num-1) %  (self.board_length-(pos.w-1)) + (pos.w-1)
        translated_action.append(loc_h)        
        translated_action.append(loc_w)
        translated_action.append(pos)
        #print(translated_action)
        #print(pos)
        #print(id)
        return translated_action


    def render(self, mode='human', close=False, verbose = True):
        #print current game state
        #print current board state
        #print legal_actions

        #print(self.translate_action(121))
        #print(self.update_board(self.translate_action(1)))

        logger.debug('')
        if close:
            return
        if self.done:
            logger.debug(f'GAME OVER')
        else:
            logger.debug(f"It is Player {self.current_player.id}'s turn to move")
        
        
        for line in self.obs_regularize(self.obs_rotate(self.board, (self.current_player.id-1)%4*self.n_players), self.current_player.id):
            logger.debug(line)

        '''
        logger.debug(f'occupied')

        for line in self.current_player.occupied:
            logger.debug(line)

        logger.debug(f'corners')

        for line in self.current_player.corners:
            logger.debug(line)

        logger.debug(f'adjacents')

        for line in self.current_player.adjacents:
            logger.debug(line)

        logger.debug(f'possible')

        for line in self.current_player.possible:
            logger.debug(line)
        '''

        #logger.debug(self.observation[:64])

        if self.verbose:
            pass

        if not self.done:
            logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')