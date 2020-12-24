'''
Author: Ibrahim Kamal
Course: CS 380
Description: Implement the search algorithms to find a solution path to the goal condition
'''
from rgb import *
from agent import *

'''heuristic function which determines how many same color blocks are next to each other in a given state, which means that
for the given default state the heuristic function will return 3'''

def heuristic(state):
    currentState = state
    count = 0
    coordinateList = set()
    
    for x in range(currentState.size):
        
        for y in range(currentState.size):
            c = currentState.get(x, y)
            
            if c != Cell.EMPTY:
                deltas = [(-1, 0), (+1, 0), (0, -1), (0, +1)]
                
                for dx, dy in deltas:
                    x2, y2 = x+dx, y+dy
                    c2 = currentState.get(x2, y2)
                    
                    if (c == c2) and ((x2,y2) not in coordinateList or (x,y) not in coordinateList):
                            count += 1
                            coordinateList.add((x2,y2))
                            coordinateList.add((x,y))
    
                
                            
    return count

''' main routine '''
if __name__ == '__main__':
    cmd = util.get_arg(1)
    agent = Agent()
    
    if cmd:
        
        optionalArguement = util.get_arg(2)
        
        if cmd == 'random':
            util.pprint(agent.random_walk(optionalArguement, 8))
            
        elif cmd == 'bfs':
            agent.bfs(optionalArguement)
            
        elif cmd == 'dfs':
            agent.dfs(optionalArguement)
            
        elif cmd == 'a_star':
            agent.a_star(optionalArguement, heuristic)
        