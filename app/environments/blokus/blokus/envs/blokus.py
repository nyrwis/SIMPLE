# Modified code from https://github.com/DerekGloudemans/Blokus-Reinforcement-Learning

import gym
import numpy as np

import config
import copy

from stable_baselines import logger

from classes import Piece, Player


p1 = [1, 1, (1,1), 1, [[1, 1, [(0,0)]]]]
p2 = [2, 2, (2,1), 2, [[2, 1, [(0,0), (0,1)]], [1, 2, [(0,0), (1,0)]]]]
p3 = [3, 3, (2,2), 4, [[2, 2, [(0,0), (0,1), (1,1)]], [2, 2, [(0,1), (1,1), (1,0)]], [2, 2, [(0.0), (1,0), (1,1)]], [2, 2, [(1,0), (0,0), (0,1)]]]]
p4 = [4, 3, (3,1), 2, [[3, 1, [(0,0), (1,0), (2,0)]], [1, 3, [(0,0), (0,1), (0,2)]]]]
p5 = [5, 4, (2,2), 1, [[2, 2, [(0,0), (0,1), (1,1), (1,0)]]]]
p6 = [6, 4, (3,2), 4, [[3, 2, [(0,1), (1,0), (1,1), (1,2)]], [2, 3, [(0,0), (1,0), (1,1), (2,0)]], [3, 2, [(0,0), (0,1), (0,2), (1,1)]], [2, 3, [(0,1), (1,0), (1,1), (0,2)]]]
p7 = [7, 4, (4,1), 2, [[4, 1, [(0,0), (0,1), (0,2), (0,3)]], [1, 4, [(0,0), (1,0), (2,0), (3,0)]]]]
p8 = [8, 4, (3,2), 8, [[3, 2, [(0,2), (1,0), (1,1), (1,2)]], [2, 3, [(0,0), (1,0), (2,0), (2,1)]], [3, 2, [(0,0), (0,1), (0,2), (1,0)]], [2, 3, [(0,0), (0,1), (1,1), (2,1)]], [2, 3, [(0,0), (1,0), (1,1), (1,2)]], [3, 2, [(0,0), (0,1), (1,0), (2,0)]], [2, 3, [(0,0), (0,1), (0,2), (1,2)]], [3, 2, [(0,1), (1,1), (2,0), (2,1)]]]]
p9 = [9, 4, (3,2), 4, [[3, 2, [(0,1), (0,2), (1,0), (1,1)]], [2, 3, [(0,0), (1,0), (1,1), (2,1)]], [3, 2, [(0,0), (0,1), (1,1), (1,2)]], [2, 3, [(0,1), (1,0), (1,1), (2,1)]]]]

piece_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

action_marking = [0, 64, 176, 372, 468, 517, 685, 765, 1101, 1269]


class BlokusEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(BlokusEnv, self).__init__()
        self.name = 'blokus'
        self.manual = manual

        self.board_length = 8
        self.n_player = 2
        self.board_shape = (self.board_length, self.board_length)
        self.piece_num = 8
        self.possible_action_num = 1269
        self.action_space = gym.spaces.Discrete(self.possible_action_num)
        self.observation_space = gym.spaces.Box(low=0, high=self.n_player, self.board_shape)
        self.verbose = verbose


    @property
    def observation(self):
        #combine current board state, legal_actions
        #return combined observation
        copied_board = copy.deepcopy(self.board)
        combined_observation = np.array(copied_board).flatten()
        combined_observation.append(self.legal_actions())
        return combined_observation
    

    @property
    def legal_actions(self, action):
        #calculate legal_actions based on board state, player's pieces
        legal_actions = np.zeros(self.possible_action_num)
        for piece_num in self.current_player.pieces:
            if piece:
            for point in get_point(self.current_player.possible_point):
                for loc in self.current_player.loc:
                    if 
                    action_num=
                    legal_actions[action_num] = 1
                    
                    


    @property
    def current_player(self):
        return self.players[self.current_player_num]


    def get_point(self, board):
        point_list = []
        for col in board:
            for row in col:
                if 
                point = Point(col, row)
                point_list.append(point)
        return point_list


    def reset(self):
        self.board = [[0 for i in range(self.board_length)] for j in range(self.board_length)]
        self.players = [Player(1), Player(2)]
        for player in self.players:
            player.setup(self.board_length, self.piece_num)
        self.pieces = []
        for piece in piece_list:
            self.pieces.append(Piece(*piece))
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation


    def step(self, action):
        reward = [0,0]
        update_board(translate_action(action))
        self.current_player.update(translate_action(action))

        self.change_turn()

        while !get_point(self.current_player.possible_point):
            

            if no player to play:
                done = True

        observation = self.observation()
        return obseration, reward, done, {}
        
    def update_board(self, action):


    def change_turn(self):
        self.current_player_num = (self.current_player_num+1)%self.n_player


    def translate_action(self, action):
        #translated_action int->id,loc_h,loc_w,pos
        translated_action = []
        int id
        for id in range(9):
            if action > action_marking[id]:
                action = action-action_marking[id]
                translated_action.append(id)
                break

        pos_num = action % self.pieces[id].dim
        pos = self.pieces[id].pos_list[pos_num]
        loc_h = self.pieces[id]
        loc_w = self.pieces[id]
        translated_action.append(h)        
        translated_action.append(w)
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
            logger.debug(' '.join(line))

        if self.verbose:
            pass

        if not self.done:
            logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')
