'''
Author: Ibrahim Kamal
Course: CS 380
Description: Implement the search algorithms to find a solution path to the goal condition
'''

from rgb import *
from util import *
import random
import queue

'''Node class to store all the relevant information, including the current state, parent state, and depth'''

class Node:
    def __init__(self, state, parent = None, depth = 0):
        self.__state = state
        self.__parent = parent
        self.__depth = depth
    
    def getState(self):
        return self.__state
    
    def setParent(self, parent):
        self.__parent = parent
    
    def getDepth(self):
        return self.__depth
    
    def setDepth(self, depth):
        self.__depth = depth
        
    def getParent(self):
        return self.__parent
    
    def clone(self):
        return Node(self.__state, self.__parent, self.__depth)
    
    def __gt__(self, other):
        return self.__depth > other.__depth

'''Agent class to perform the random walk and different search algorithms'''
class Agent:
    def __init__(self, string = ""):
        self.__string = string
    
    '''generating a random walk from a given state'''
    def random_walk(self, state1, n):
        currentState = State(state1)   
        currentNode = Node(currentState)
        
        for i in range(n - 1):
           
           '''getting the list of actions and then selecting one at random and executing it'''
           currentActions = currentState.actions()
           nextState = currentState.clone().execute(currentActions[random.randint(0, len(currentActions) - 1)])
           
           '''creating the node and setting its parent'''
           nextNode = Node(state = nextState, parent = currentNode)
           currentState = nextState.clone()
           currentNode = nextNode.clone()
        
        tmpReturnList = []
        tmpPrintNode = currentNode.clone();
        
        '''creating a list of states from the last node'''
        while tmpPrintNode is not None:
            tmpPrintState = tmpPrintNode.getState()
            tmpReturnList.append(tmpPrintState)
            tmpPrintNode = tmpPrintNode.getParent()
            
        return tmpReturnList[::-1]
    
    '''function used to print all the states from the current state to the parent state'''
    def printNode(self, tmpToPrintNode):
        tmpToPrintList = []
        
        while not tmpToPrintNode == None:
            tmpToPrintList.append(tmpToPrintNode.getState())
            tmpToPrintNode = tmpToPrintNode.getParent()
            
        return tmpToPrintList
    
    '''the base search method used by different search algorithms, for bfs and dfs, heuristic is None'''
    def _search(self, state, container, heuristic):
        self.__root = Node(State(state))
        self.__queue = container

        if heuristic is None:
            self.__queue.put(self.__root)
        else:
            self.__queue.put((heuristic(self.__root.getState()) + 0, self.__root))

        self.__states = {}
        while not self.__queue.empty():
            currentNode = self.__queue.get()
            
            if heuristic is not None:
                currentNode = currentNode[1]
                
            currentState = currentNode.getState()
            
            self.__states[currentState.__str__()] = True
            
            currentDepth = currentNode.getDepth()
            
            util.pprint(self.printNode(currentNode.clone())[::-1])
            
            if currentState.is_goal():
                break
            
            currentActions = currentState.actions()
            
            tmpState = currentState.clone()
            
            nextDepth = currentDepth + 1
            
            for action in currentActions:
                nextState = tmpState.execute(action)
                
                if nextState.__str__() in self.__states.keys():
                    nextNode = None
                    
                else:
                    nextNode = Node(state = nextState, depth = nextDepth)
                    nextNode.setParent(currentNode)
                    
                    if heuristic is None:
                        self.__queue.put(nextNode)
                        
                    else:
                        heuristicValue = heuristic(nextNode.getState())
                        self.__queue.put((heuristicValue + nextDepth, nextNode))
                
                tmpState = currentState.clone()
                
        print(len(self.__states.keys()))

    '''the uninformed search methods'''
    
    def bfs(self,state):
        self._search(state, queue.Queue(), None)
        
    def dfs(self,state):
        self._search(state, queue.LifoQueue(), None)
    
    '''the informed search method'''
    def a_star(self, state, heuristic):
        self._search(state, queue.PriorityQueue(), heuristic)
                
