'''
Name: Ibrahim Kamal
Course: CS380
Description: To allow two players(human or agents) to play a game of Connect 3
'''

from connect3 import *
from util import *
from game import *

'''The HumanPlayer class which allows the user to select from the next available moves'''
class HumanPlayer(Player):
    def __init__(self, character):
        super().__init__(character)
    
    def getCharacter(self):
        return super().getCharacter()
    
    def choose_action(self, state):
        currentState = State(state)
        actions = currentState.actions(super().getCharacter())
        for i in range(len(actions)):
            print(str(i) + ": " + str(actions[i]))
        
        
        userChoice = int(input("Please choose an action: "))
        
        return userChoice