'''
Class for blackjack game.

Setup to work with a neural net.

Inputs between 0-1 to select move.
'''

import random
import neat

class Blackjack(object):

    def __init__(self, genome, config):
        self.nn = neat.nn.FeedForwardNetwork(genome, config)

        self.pool = pool
        self.bet = bet
        self.num_games = num_games
        self.player = []
        self.dealer = []
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4*4)

    def play(self):
        '''
        Play hands of Blackjack tell num_games or pool empty
        '''

    def player_move(self, move):
        '''
        Takes an input 0-1 and translates that to a card move.
            [0,0.25] => stand
            [0.25,0.5] => hit
            [0.5,0.75] => double
            [0.75,1] => split
        '''

    def get_current_state(self):
        '''
        Returns a list of all three cards player can see.
        Scales cards from 0-1 (2=0, (ace)14=1)
        '''
