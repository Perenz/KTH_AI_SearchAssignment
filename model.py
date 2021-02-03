import math
import time
from fishing_game_core.shared import ACTION_TO_STR

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class GameModel:
    def __init__(self, initial_data):
        print("PROVA")
        self.init_fishes(initial_data)

    def init_fishes(self, initial_data):
        '''
        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3}, 
          'fish1': {'score': 2, 'type': 1}, 
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }
        '''
        self.fishes = {}
        for f in initial_data:
            #Check if fish
            
            if f[:4] == 'fish':
                fish_n = f[4:]
                el = {'score':initial_data[f]['score'], 'type':initial_data[f]['type']}
                self.fishes[fish_n] = el

        '''
        print(self.fishes)
        print("PROVA")
        '''

    def man_distance(self, fish, hook):
        x = min((fish[0] - hook[0]), 20-(fish[0]-hook[0]))
        y = abs(hook[1] - fish[1])

        return x + y

    def heur_1(self, state):
        node = state.node
        player_scores = node.player_scores
        fish = node.fish_positions
        fish_scores = node.fish_scores
        n_fish = len(fish)

        hook_p1, hook_p2 = node.get_hook_positions().values()
        scores_diff = player_scores[0] - player_scores[1]

        #If no fish, return score difference
        if n_fish == 0:
            return scores_diff

        #Evaluate distance for every fish
        val = 0
        for fish, pos in fish.items():
            proximity = self.man_distance(pos, hook_p1)
            #Check distance
            val += fish_scores[fish] / (proximity + 1)

        #Linear combination of val and scores difference
        return scores_diff + val



