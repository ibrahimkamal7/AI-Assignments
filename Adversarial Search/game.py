'''
Name: Ibrahim Kamal
Course: CS380
Description: To allow two players(human or agents) to play a game of Connect 3
'''

from connect3 import *
from util import *

''''The Player class'''
class Player:
    def __init__(self, character):
        self.__character = character
    
    def setCharacter(self, character):
        self.__character = character
    
    def getCharacter(self):
        return self.__character
        
    def choose_action(self, state):
        pass
    
'''The Game class which allows the uers to play the games'''
class Game:
    def __init__(self, initialState, player1, player2):
        self.__initialState = initialState
        self.__player1 = player1
        self.__player2 = player2
    
    
    def play(self):
        currentState = State(self.__initialState)
        stateLists = []
        
        while not currentState.game_over():
            player1Actions = currentState.actions(self.__player1.getCharacter())
            userChoice = self.__player1.choose_action(currentState.__str__())
            
            currentState = currentState.execute(player1Actions[userChoice])
            
            util.pprint(currentState)
            stateLists.append(currentState.clone())
            
            if currentState.game_over():
                break
            
            player2Actions = currentState.actions(self.__player2.getCharacter())
            userChoice = self.__player2.choose_action(currentState.__str__())
            
            currentState = currentState.execute(player2Actions[userChoice])
            
            util.pprint(currentState)
            stateLists.append(currentState.clone())
            
            if currentState.game_over():
                break
            
        winner = currentState.winner()
        
        return (stateLists, winner)
