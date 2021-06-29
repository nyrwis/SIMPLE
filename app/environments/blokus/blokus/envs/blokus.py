# Modified code from https://github.com/DerekGloudemans/Blokus-Reinforcement-Learning

import gym
import numpy as np

import config

from stable_baselines import logger

from classes import Piece, Player

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
        pass
    

    @property
    def legal_actions(self, action):
        #calculate legal_actions based on board state, player's pieces
        legal_action = 
        for piece in self.current_player:
            for point in get_point(self.current_player.possible_point):
                for loc in self.current_player.loc:
                    
                    


    @property
    def current_player(self):
        return self.players[self.current_player_num]


    def get_point(self, board):
        point_list = []
        for col in board:
            for row in col:
                point = Point(col, row)
                point_list.append(point)
        return point_list


    def reset(self):
        self.board = [[0 for i in range(self.board_length)] for j in range(self.board_length)]
        self.players = [Player(1), Player(2)]
        for player in self.players:
            player.setup(self.board_length, self.piece_num)
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation


    def step(self, action):
        #update board
            #translate action
            #place piece
        #update player
            #delete placed piece
            #update piece location information

        #change turn

        #delete unplayable players until playable player appears
            #if no player to play -> reward, done

        #return obseration, reward, done
        pass


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
