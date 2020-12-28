'''
Name: Ibrahim Kamal
Course: CS380
Description: To allow two players(human or agents) to play a game of Connect 3
'''

from connect3 import *
from util import *
from game import *
from human import *
from agent import *

'''The main class which carries out the game between two players. Remove the comments from this part to play the game'''
# if __name__ == '__main__':
#     arg1 = util.get_arg(1)
#     arg2 = util.get_arg(2)
#     
#     player1 = None
#     player2 = None
#     
#     if arg1 and arg2:
#         
#         if arg1 == 'human':
#             player1 = HumanPlayer("X")
#         elif arg1 == 'random':
#             player1 = RandomPlayer("X")
#         elif arg1 == 'minimax':
#             player1 = MiniMaxPlayer("X")
#             
#         if arg2 == 'human':
#             player2 = HumanPlayer("O")
#         elif arg2 == 'random':
#             player2 = RandomPlayer("O")
#         elif arg2 == 'minimax':
#             player2 = MiniMaxPlayer("O")
#          
#         game = Game("    |    |    ", player1, player2)
#         gameTuple = game.play()
#          
#         util.pprint(gameTuple[0])
#          
#         if gameTuple[1] is not None:
#             print(gameTuple[1], "wins !!")
#         else:
#             print("Game is Drawn")

'''This part of the code can be used to see what's the percentage of the MiniMax agent winning'''
player1 = MiniMaxPlayer("O")
player2 = RandomPlayer("X")
game = Game("    |    |    ", player2, player1)
count = 0
for i in range(100):
    gameTuple = game.play()
    if gameTuple[1] == 'O':
        count += 1

print(count/100 * 100)
