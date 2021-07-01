# Modified code from https://github.com/DerekGloudemans/Blokus-Reinforcement-Learning

import gym
import numpy as np

import config
import copy

from stable_baselines import logger

from .classes import Piece, Player


#information of each piece
#[id, num of spaces each piece cover, (num of possible grid location in a row, num of possible grid location in a column), possible position, (grid_h, grid_w, grid location)]
'''
p1 = [1, 1, (7,7), 1, [[1, 1, [(0,0)]]]]
p2 = [2, 2, (7,6), 2, [[1, 2, [(0,0), (0,1)]], [2, 1, [(0,0), (1,0)]]]]
p3 = [3, 3, (6,6), 4, [[2, 2, [(0,0), (0,1), (1,1)]], [2, 2, [(0,1), (1,1), (1,0)]], [2, 2, [(0.0), (1,0), (1,1)]], [2, 2, [(1,0), (0,0), (0,1)]]]]
p4 = [4, 3, (7,5), 2, [[1, 3, [(0,0), (1,0), (2,0)]], [3, 1, [(0,0), (0,1), (0,2)]]]]
p5 = [5, 4, (6,6), 1, [[2, 2, [(0,0), (0,1), (1,1), (1,0)]]]]
p6 = [6, 4, (6,5), 4, [[2, 3, [(0,1), (1,0), (1,1), (1,2)]], [3, 2, [(0,0), (1,0), (1,1), (2,0)]], [2, 3, [(0,0), (0,1), (0,2), (1,1)]], [3, 2, [(0,1), (1,0), (1,1), (0,2)]]]]
p7 = [7, 4, (7,4), 2, [[1, 4, [(0,0), (0,1), (0,2), (0,3)]], [4, 1, [(0,0), (1,0), (2,0), (3,0)]]]]
p8 = [8, 4, (6,5), 8, [[2, 3, [(0,2), (1,0), (1,1), (1,2)]], [3, 2, [(0,0), (1,0), (2,0), (2,1)]], [2, 3, [(0,0), (0,1), (0,2), (1,0)]], [3, 2, [(0,0), (0,1), (1,1), (2,1)]], [3, 2, [(0,0), (1,0), (1,1), (1,2)]], [2, 3, [(0,0), (0,1), (1,0), (2,0)]], [3, 2, [(0,0), (0,1), (0,2), (1,2)]], [2, 3, [(0,1), (1,1), (2,0), (2,1)]]]]
p9 = [9, 4, (6,5), 4, [[2, 3, [(0,1), (0,2), (1,0), (1,1)]], [3, 2, [(0,0), (1,0), (1,1), (2,1)]], [2, 3, [(0,0), (0,1), (1,1), (1,2)]], [3, 2, [(0,1), (1,0), (1,1), (2,1)]]]]
'''
p1 = [1, 1, [7,7], 1, [[1, 1, [[0,0]]]]]
p2 = [2, 2, [7,6], 2, [[1, 2, [[0,0], [0,1]]], [2, 1, [[0,0], [1,0]]]]]
p3 = [3, 3, [6,6], 4, [[2, 2, [[0,0], [0,1], [1,1]]], [2, 2, [[0,1], [1,1], [1,0]]], [2, 2, [[0.0], [1,0], [1,1]]], [2, 2, [[1,0], [0,0], [0,1]]]]]
p4 = [4, 3, [7,5], 2, [[1, 3, [[0,0], [1,0], [2,0]]], [3, 1, [[0,0], [0,1], [0,2]]]]]
p5 = [5, 4, [6,6], 1, [[2, 2, [[0,0], [0,1], [1,1], [1,0]]]]]
p6 = [6, 4, [6,5], 4, [[2, 3, [[0,1], [1,0], [1,1], [1,2]]], [3, 2, [[0,0], [1,0], [1,1], [2,0]]], [2, 3, [[0,0], [0,1], [0,2], [1,1]]], [3, 2, [[0,1], [1,0], [1,1], [0,2]]]]]
p7 = [7, 4, [7,4], 2, [[1, 4, [[0,0], [0,1], [0,2], [0,3]]], [4, 1, [[0,0], [1,0], [2,0], [3,0]]]]]
p8 = [8, 4, [6,5], 8, [[2, 3, [[0,2], [1,0], [1,1], [1,2]]], [3, 2, [[0,0], [1,0], [2,0], [2,1]]], [2, 3, [[0,0], [0,1], [0,2], [1,0]]], [3, 2, [[0,0], [0,1], [1,1], [2,1]]], [3, 2, [[0,0], [1,0], [1,1], [1,2]]], [2, 3, [[0,0], [0,1], [1,0], [2,0]]], [3, 2, [[0,0], [0,1], [0,2], [1,2]]], [2, 3, [[0,1], [1,1], [2,0], [2,1]]]]]
p9 = [9, 4, [6,5], 4, [[2, 3, [[0,1], [0,2], [1,0], [1,1]]], [3, 2, [[0,0], [1,0], [1,1], [2,1]]], [2, 3, [[0,0], [0,1], [1,1], [1,2]]], [3, 2, [[0,1], [1,0], [1,1], [2,1]]]]]

piece_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

piece_point = [1, 2, 3, 3, 4, 4, 4, 4, 4]

#accumulated possible action for each piece
action_marking = [0, 64, 176, 372, 468, 517, 685, 765, 1101, 1269]


class BlokusEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(BlokusEnv, self).__init__()
        self.name = 'blokus'
        self.manual = manual

        self.board_length = 8
        self.n_players = 2
        self.board_shape = (self.board_length, self.board_length)
        self.piece_num = 8
        self.possible_action_num = 1269
        self.action_space = gym.spaces.Discrete(self.possible_action_num)
        self.observation_space = gym.spaces.Box(0, self.n_players, self.board_shape)
        self.verbose = verbose


    @property
    def observation(self):
        #combine current board state, legal_action
        combined_observation = np.array(self.board).flatten()
        x = np.array(self.legal_actions)
        combined_observation = np.append(combined_observation, x)
        return combined_observation
    

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
                                action_num = action_marking[piece.id-1] + (pos.id-1)*piece.dim_size + (r-(pos.h-1))*(self.board_length-(pos.w-1)) + c-(pos.h-1)
                                legal_action[action_num] = 1
        return legal_action


    def inboard(self, h, w, r, c):
        if r-(h-1)>=0 and c-(w-1)>=0 and r<=self.board_length-1 and c<=self.board_length-1:
            return True
        else:
            return False



    def chk_possible(self, possible, r, c, pos):
        pass
        '''
        for grid in pos.loc:
            print(type(grid))
            print(grid[0], grid[1])
            print("sdfasdfd")
            x,y = grid
            x += r-(pos.h-1)
            y += c-(pos.w-1)
            new_grid = [x, y]
            if new_grid==possible:
                    return True
        return False
        '''


    def chk_occupied(self, r, c, pos):
        pass
        '''
        for grid in pos.loc:
            x,y = grid
            x += r-(pos.h-1)
            y += c-(pos.w-1)
            new_grid = [x, y]
            for point in self.get_point(self.board):
                if new_grid==point:
                    return False
        return True
        '''


    def chk_adjacent(self, r, c, pos):
        pass
        '''
        for grid in pos.loc:
            x = r-(pos.h-1)+grid[0]
            y = c-(pos.w-1)+grid[1]
            new_grid = [x, y]
            for point in self.get_point(self.current_player.adjacents):
                if new_grid==point:
                    return False
        return True
        '''


    @property
    def current_player(self):
        return self.players[self.current_player_num]


    def get_point(self, board):
        point_list = []
        for i in range(self.board_length):
            for j in range(self.board_length):
                if board[i][j] == 1:
                    point = [i, j]
                    point_list.append(point)
        return point_list


    def reset(self):
        self.board = [[0 for i in range(self.board_length)] for j in range(self.board_length)]
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


    def step(self, action):
        reward = [0,0]
        self.update_board(self.translate_action(action))
        self.current_player.update(self.translate_action(action), self.board)

        done = self.change_turn()

        while not self.get_point(self.current_player.possible):
            self.left_players[self.current_player_num] = 0
            done = self.change_turn()
            if done==True:
                break

        observation = self.observation

        if done:
            reward = self.choose_winner()

        return observation, reward, done, {}


    def update_board(self, action):
        loc_h, loc_w, pos = action[1], action[2], action[3]
        h, w, loc = pos.h, pos.w, pos.loc
        for grid in loc:
            self.board[grid[0]+loc_h-(h-1)][grid[1]+loc_w-(w-1)] = self.current_player.id


    def choose_winner(self):
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


    def change_turn(self):
        done = True
        for i in range(self.n_players):
            if self.left_players[i] == 1:
                done = False
                break
            
        self.current_player_num = (self.current_player_num+1)%self.n_players
        while self.left_players[self.current_player_num]==0:
            self.current_player_num = (self.current_player_num+1)%self.n_players
        return done

    def translate_action(self, action):
        #translated_action int->id,loc_h,loc_w,pos
        translated_action = []
        id = None
        for id in range(9):
            if action < action_marking[id]:
                action = action-action_marking[id-1]
                translated_action.append(id)
                break

        pos_num = (action-1) // self.pieces[id].dim_size + 1
        pos = self.pieces[id].pos_list[pos_num]
        loc_num = (action-1) % self.pieces[id].dim_size + 1
        loc_h = (loc_num-1) // self.pieces[id].dim[1] + (pos.h-1)
        loc_w = (loc_num-1) % self.pieces[id].dim[1] + (pos.w-1)
        translated_action.append(loc_h)        
        translated_action.append(loc_w)
        translated_action.append(pos)
        return translated_action


    def render(self, mode='human', close=False, verbose = True):
        #print current game state
        #print current board state
        #print legal_actions
        logger.debug('')
        if close:
            return
        if self.done:
            logger.debug(f'GAME OVER')
        else:
            logger.debug(f"It is Player {self.current_player.id}'s turn to move")

        for line in self.board:
                logger.debug(line)

        if self.verbose:
            pass

        if not self.done:
            logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')