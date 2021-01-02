import json
import os
import random

from .state import State


class Q_State(State):
    '''Augments the game state with Q-learning information'''

    def __init__(self, string):
        super().__init__(string)

        # key stores the state's key string (see notes in _compute_key())
        self.key = self._compute_key()

    def _compute_key(self):
        '''
        Returns a key used to index this state.

        The key should reduce the entire game state to something much smaller
        that can be used for learning. When implementing a Q table as a
        dictionary, this key is used for accessing the Q values for this
        state within the dictionary.
        '''

        # this simple key uses the 3 object characters above the frog
        # and combines them into a key string
        return ''.join([
            self.get(self.frog_x - 1, self.frog_y - 1) or '_',
            self.get(self.frog_x, self.frog_y - 1) or '_',
            self.get(self.frog_x + 1, self.frog_y - 1) or '_',
        ])

    def reward(self):
        '''Returns a reward value for the state.'''

        if self.at_goal:
            return self.score
        elif self.is_done:
            return -10
        else:
            return 0


class Agent:

    def __init__(self, train=None):

        # train is either a string denoting the name of the saved
        # Q-table file, or None if running without training
        self.train = train

        # q is the dictionary representing the Q-table
        self.q = {}

        # name is the Q-table filename
        # (you likely don't need to use or change this)
        self.name = train or 'q'

        # path is the path to the Q-table file
        # (you likely don't need to use or change this)
        self.path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), 'train', self.name + '.json')

        self.load()

    def load(self):
        '''Loads the Q-table from the JSON file'''
        try:
            with open(self.path, 'r') as f:
                self.q = json.load(f)
            if self.train:
                print('Training {}'.format(self.path))
            else:
                print('Loaded {}'.format(self.path))
        except IOError:
            if self.train:
                print('Training {}'.format(self.path))
            else:
                raise Exception('File does not exist: {}'.format(self.path))
        return self

    def save(self):
        '''Saves the Q-table to the JSON file'''
        with open(self.path, 'w') as f:
            json.dump(self.q, f)
        return self

    
    def choose_action(self, state_string):
        """
        Returns the action to perform.

        This is the main method that interacts with the game interface:
        given a state string, it should return the action to be taken
        by the agent.
        
        This method uses the Q-learning algorithm to train the model
        """

        max_action = 0
        alpha = 0.9
        gamma = 0.7

        state = Q_State(state_string)
        actions = self.possible_actions(state)
        current_key = state._compute_key()
        value = random.random()
        
        if value < 0.5:
            return State.ACTIONS[0]
        
        if current_key not in self.q.keys():
            self.q[current_key] = [0, 0, 0, 0]
        
        
        for i in range(len(actions)):
            new_state = self.execute_action(Q_State(state_string), actions[i])
            new_key = new_state._compute_key()
            if new_key not in self.q.keys():
                self.q[new_key] = [0, 0, 0, 0]
            
            if (max(self.q[new_key]) > max_action):
                max_action = max(self.q[new_key])
            
            self.q[current_key][i] = ((1-alpha) * self.q[current_key][i]) +(alpha*(new_state.reward() + (gamma*max_action)))
            self.save()
            
        q_max_index = self.q[current_key].index(max(self.q[current_key]))
        return State.ACTIONS[q_max_index]
            
    
    #executing the given action on the given state
    def execute_action(self, state, action):
        
        if action == "u":
            state.frog_y = state.frog_y - 1
        elif action == "d":
            state.frog_y = state.frog_y + 1
        elif action == "l":
            state.frog_x = state.frog_x - 1
        elif action == "r":
            state.frog_x = state.frog_x + 1
            
        return state
    
    #computing all the possible actions
    def possible_actions(self, state):
        output = []
        frog_x = state.frog_x
        frog_y = state.frog_y
        
        for action in State.ACTIONS:
            if action == "u" and state.is_legal(frog_x, frog_y-1):
                output.append("u")
            elif action == "d" and state.is_legal(frog_x, frog_y+1):
                output.append("d")
            elif action == "l" and state.is_legal(frog_x-1, frog_y):
                output.append("l")
            elif action == "r" and state.is_legal(frog_x+1, frog_y):
                output.append("r")
                
        return output
