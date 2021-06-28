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

        self.verbose = verbose

    @property
    def legal_actions(self):
        #calculate legal_actions based on board state, player's pieces
        pass

    @property
    def observation(self):
        #combine current board state, legal_actions
        #return combined observation
        pass
    
    def reset(self):
        #set board
        #set player
            #hand out pieces
            #set initial starting point
        #return observation
        pass

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
        pass
