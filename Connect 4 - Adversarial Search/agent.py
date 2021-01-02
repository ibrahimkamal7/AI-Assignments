'''
Name: Ibrahim Kamal
Course: CS380
Description: To allow two players(human or agents) to play a game of Connect 3
'''

from connect3 import *
from util import *
from game import *
import random

'''The RandomPlayer class which chooses a random a move from the available next moves''' 
class RandomPlayer(Player):
    def __init__(self, character):
        super().__init__(character)
    
    def choose_action(self, state):
        currentState = State(state)
        actions = currentState.actions(super().getCharacter())
        
        return random.randint(0, len(actions) - 1)
    
    def getCharacter(self):
        return super().getCharacter()

'''The MiniMax agent which chooses the best possible moves from the available moves. The minimax algorithm has a depth of 4 and for each
recursive call there is a 2 move look ahead.''' 
class MiniMaxPlayer(Player):
    def __init__(self, character):
        super().__init__(character)
    
    ''' A utility function for the heuristic'''
    
    def characterCount(self, array):
        hashmap = {}
        
        for i in array:
            hashmap[i] = 0
        
        for i in array:
            hashmap[i] += 1
    
        return hashmap

    '''The evalution function for the minimax algorithm. It find out how many player's character and how many opponent's character are present in a single
       row, column, and diagonal and returns a value accordingly.'''
    
    def evaluation(self, state, character):
        board = state.board
        values = []
        score = 0
        
        if state.winner():
             return -1000
        values.append(self.characterCount(board[0]))
        values.append(self.characterCount(board[1]))
        values.append(self.characterCount(board[2]))
        
        values.append(self.characterCount([board[0][0], board[1][0], board[2][0]]))
        values.append(self.characterCount([board[0][1], board[1][1], board[2][1]]))
        values.append(self.characterCount([board[0][2], board[1][2], board[2][2]]))
        values.append(self.characterCount([board[0][3], board[1][3], board[2][3]]))
        
        values.append(self.characterCount([board[0][0], board[1][1], board[2][2]]))
        values.append(self.characterCount([board[0][1], board[1][2], board[2][3]]))
        values.append(self.characterCount([board[0][2], board[1][1], board[2][0]]))
        values.append(self.characterCount([board[0][3], board[1][2], board[2][1]]))
        
        if character == 'X':
            opponentCharacter = 'O'
        else:
            opponentCharacter = 'X'
            
        for i in values:
            if character in i.keys():
                if i[character] == 3:
                    score = 100
                    if opponentCharacter in i.keys():
                        if i[opponentCharacter] == 1:
                            score = 50
                    if ' ' in i.keys():
                        if i[' '] == 1:
                            score = 90
                elif i[character] == 2:
                    score = 90
                    if ' ' in i.keys():
                        if i[' '] == 2:
                            score = 75
                        if i[' '] == 1:
                            score = 40
                else:
                    score = 1
            else:
                score = 0
        return score * -1
    
    '''The minimax algorithm'''
    def choose_action(self, state, depth = 4):
        currentState = State(state)
        opponentCharacter = ''
        move = None

        if depth == 0:
            return move
        if super().getCharacter() == 'X':
            opponentCharacter = 'O'
        else:
            opponentCharacter = 'X'
            
        maximum = float("-inf")
        
        action = currentState.clone().actions(super().getCharacter())
        
        for i in range(len(action)):
            nextState = currentState.clone().execute(action[i])
            if nextState.clone().winner():
                return i
            
            minimum = float("inf")
            
            opponentActions = nextState.clone().actions(opponentCharacter)
            cState = nextState.clone()

            for j in range(len(opponentActions)):
                newState = cState.clone().execute(opponentActions[j])
                
                if self.evaluation(newState.clone(), opponentCharacter) < minimum:
                    minimum = self.evaluation(newState.clone(), opponentCharacter)

                self.choose_action(newState.clone().__str__(), depth - 1)
                
                if maximum > minimum:
                    break
                
            ''' alpha - beta pruning '''
            if minimum > maximum:
                maximum = minimum
                move = i
        
        return move
                    
    
    def getCharacter(self):
        return super().getCharacter()
    