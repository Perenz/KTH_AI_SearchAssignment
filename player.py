#!/usr/bin/env python3
import random, time, math
import model

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR

TIME_RES = 0.050


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class GameModel:
    def __init__(self, init):
        self.init = init
        self.best_value = 0
        self.hash_table = {}

    def check_rep_state(self, s):
        if self.hash_table.get(s, None) is None:
            #State is new
            return False
        else:
            #State is not new
            return True

    def get_value(self, s):
        return self.hash_table.get(s, 0)

    def set_best_value(self, best):
        self.best_value = best

    
class Timer:
    def __init__(self, sec):
        self.sec = sec
        self.done = False

    def start_timer(self):
        start = time.time()
        while time.time() < start + self.sec:
            # print('still have time')
            pass
        # print('oop time ran out')
        self.done = True

class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model 
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3}, 
          'fish1': {'score': 2, 'type': 1}, 
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        #Create a Tree with all the possible moves through DFS
        #Check if a move is legal
        #Check terminal state
        #model = GameModel(initial_data)
        print("Prova")
        model_minimax = model.GameModel(initial_data)
        return model_minimax

    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node 
        :type initial_tree_node: game_tree.Node 
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE FROM MINIMAX MODEL ###
        
        # NOTE: Don't forget to initialize the children of the current node 
        #       with its compute_and_get_children() method!

        #Set max depth and max timer
        '''
        max_d = 5
        actual_d = 0

        start = time.time()
        best_depth = {}

        while (actual_d <= max_d) and (time.time() < start + TIME_RES):
            # print("calling with DEPTHS {}".format(depth), file=sys.stderr)
            #value = self.alpha_beta(model, initial_tree_node, actual_d, -math.inf, math.inf, 0, start)
            value = self.node_value(model, initial_tree_node, actual_d, -math.inf, math.inf, 0, start)
            best_depth[actual_d] = (value, model.best_move)
            actual_d += 1

        random_move = random.randrange(5)
        return ACTION_TO_STR[random_move]
        '''

    '''
    def node_value(self, model, node, depth, alpha, beta, player, start):

        best = None
        if len(node.children) == 0:
            node.compute_and_get_children()


        if (depth == 0) or not len(node.children):
            #LEAF
            value = self.computeHeuristic(node.state, player)
        elif player==0 and depth>0:
            nodes = node.children
            value = -math.inf
            #For every node, dfs
            for c in nodes:
                #If still in time
                if time.time() < start + TIME_RES:
                    #Check if state already explored
                    pass




    def computeHeuristic(self, state, player):
        hooks_position = state.get_hook_positions()
        fishes_position = state.get_fish_positions()
        fishes_scores = state.get_fish_scores()

        # algorithm: moves towards its best fish --------------- FOR A
        best_value = -math.inf
        best_id = -1
        negative_value = 0
        for fish_id, fish_position in fishes_position.items():
            dist = self.computeDistance(hooks_position[0], hooks_position[1], fish_position)
            w = self.distanceFactor(dist)
            score = fishes_scores[fish_id]
            value = score * w
            if value < 0:
                negative_value += value

            if best_value < value:
                best_value = value
                best_id = fish_id

        if best_id != -1:
            return best_value + (negative_value/2) + state.player_scores[0] - state.player_scores[1]
        else:
            return state.player_scores[0] -state.player_scores[1]


    def distanceFactor(self, distance):
        # given a distance, return a number from 0.1 and 1
        N = 19
        return ((0.01 - 1) / (math.sqrt((N/2)**2 + N**2))) * (distance) + 1

    def computeDistance(self, player_position, opp_position, fish_position):
        N = 19
        a_X = player_position[0]
        a_Y = player_position[1]

        b_X = opp_position[0]
        #b_Y = opp_position[1]

        f_X = fish_position[0]
        f_Y = fish_position[1]


        if a_X < b_X and b_X < f_X:
            distance_X= N - f_X + a_X     # c'é B in mezzo , devo fare il giro del mondo
        else:
            distance_X = f_X - a_X        # non c'é B in mezzo

        distance_Y = f_Y - a_Y

        return math.sqrt(distance_X ** 2 + distance_Y ** 2)
    '''