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

'''The MiniMaxPlayer class which chooses the best possible moves from the aviable move. The minimax algorithm has a 2 move look ahead,
so it may have some difficulties while playing second since the player playing first has a slight advantage in this game. But when minimax
goes first, it wins 80-95% times agaist the random player and it gives a tough fight to the human player.''' 
class MiniMaxPlayer(Player):
    def __init__(self, character):
        super().__init__(character)
        
    def isAllSame(self, array, character):
        hashmap = {}
        
        for i in array:
            hashmap[i] = 0
        
        for i in array:
            hashmap[i] += 1
    
        return hashmap

    '''The evalution function for the minimax algorithm'''
    def evaluation(self, state, character):
        board = state.board
        values = []
        score = 0
        
        if state.winner():
            return -1000
        
        values.append(self.isAllSame(board[0], character))
        values.append(self.isAllSame(board[1], character))
        values.append(self.isAllSame(board[2], character))
        
        values.append(self.isAllSame([board[0][0], board[1][0], board[2][0]], character))
        values.append(self.isAllSame([board[0][1], board[1][1], board[2][1]], character))
        values.append(self.isAllSame([board[0][2], board[1][2], board[2][2]], character))
        values.append(self.isAllSame([board[0][3], board[1][3], board[2][3]], character))
        
        values.append(self.isAllSame([board[0][0], board[1][1], board[2][2]], character))
        values.append(self.isAllSame([board[0][1], board[1][2], board[2][3]], character))
        values.append(self.isAllSame([board[0][2], board[1][1], board[2][0]], character))
        values.append(self.isAllSame([board[0][3], board[1][2], board[2][1]], character))
        
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
    def choose_action(self, state):
        currentState = State(state)
        opponentCharacter = ''
        move = None
        
        if super().getCharacter() == 'X':
            opponentCharacter = 'O'
        else:
            opponentCharacter = 'X'
            
        maximum = -(10**100 + 1)
        
        action = currentState.clone().actions(super().getCharacter())
        
        for i in range(len(action)):
            nextState = currentState.clone().execute(action[i])
            if nextState.clone().winner():
                return i
            
            minimum = (10**100 + 1)
            
            opponentActions = nextState.clone().actions(opponentCharacter)
            cState = nextState.clone()
            for j in range(len(opponentActions)):
                newState = cState.clone().execute(opponentActions[j])
                
                if self.evaluation(newState.clone(), opponentCharacter) < minimum:
                    minimum = self.evaluation(newState.clone(), opponentCharacter)
            
            if minimum > maximum:
                maximum = minimum
                move = i
        
        return move
                    
    
    def getCharacter(self):
        return super().getCharacter()
    