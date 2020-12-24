# Name: Ibrahim Kamal
# Course: CS 380
# Assignment A1
# Description: Representing a single state of the rotator puzzle, calculating possible next states after executing a single action, and executing a
# simple walk

import sys

#state class
class State:
    def __init__(self, initialState = '12345|1234 |12354'):
        self.__initialState = initialState
        self.__matrixRepresentation = []
    
    #making the m * n matrix representation of the given string
    def setMatrixRepresentation(self):
        rows = self.__initialState.split('|')
        
        for i in range(len(rows)):
            self.__matrixRepresentation.append([])
        
        for i in range(0,len(rows)):
            for j in rows[i]:
                self.__matrixRepresentation[i].append(j)
                
    #returning the matrix representation
    def getMatrixRepresentation(self):
        return self.__matrixRepresentation
    
    #printing the given state
    def print(self, matrix):
        stringRepresentation = ''
        
        for i in range(len(self.__matrixRepresentation)):
            
            for j in range(len(self.__matrixRepresentation[0])):
                stringRepresentation +=  str(self.__matrixRepresentation[i][j])
                
            if i != len(self.__matrixRepresentation) - 1:
                stringRepresentation += '|'
                
        print(stringRepresentation) 
    
    #rotating the row left or right depending on dx
    def rotate(self, y, dx):
        if dx == '-1':
            self.__matrixRepresentation[y].append(self.__matrixRepresentation[y][0])
            self.__matrixRepresentation[y].pop(0)
            
        elif dx == '1':
            self.__matrixRepresentation[y].insert(0, self.__matrixRepresentation[y][len(self.__matrixRepresentation[y]) - 1])
            self.__matrixRepresentation[y].pop(len(self.__matrixRepresentation[y]) - 1)
    
    #sliding the at x1, y1 to x2, y2
    def slide(self, x1, y1, x2, y2):
        self.__matrixRepresentation[y2][x2] = self.__matrixRepresentation[y1][x1]
        self.__matrixRepresentation[y1][x1] = " "
    
    #executing the given slide or rotation action
    def execute(self, action):
        if 'rotate' in action:
            index = action.index(',')
            y = action[7 : index]
            index2 = action.index(')')
            dx = action[index + 1 : index2]
            self.print(self.__matrixRepresentation)
            
            for i in range(0, len(self.__matrixRepresentation[0]) - 1):
                self.rotate(int(y), dx)
                self.print(self.__matrixRepresentation)
        
        elif 'slide' in action:
            values = action[6:-1].split(',')
            
            for i in range(len(values)):
                values[i] = int(values[i])
                
            self.print(self.__matrixRepresentation)
            
            if values[1] < values[3]:
                
                while values[1] >= 0 and values[3] >= 0:
                    self.slide(values[0], values[1], values[2], values[3])
                    self.print(self.__matrixRepresentation)
                    values[1] -= 1
                    values[3] -= 1
                    
            if values[1] > values[3]:
                
                while values[1] < len(self.__matrixRepresentation) and values[3] < len(self.__matrixRepresentation):
                    self.slide(values[0], values[1], values[2], values[3])
                    self.print(self.__matrixRepresentation)
                    values[1] += 1
                    values[3] += 1
    
    #helper function for is_goal() method. checking whether all the elements in an array are same or not, keeping in mind the empty space.
    def isAllSame(self, array):
        hashmap = {}
        
        for i in array:
            hashmap[i] = 0
            
        if len(hashmap) == 1:
            return True
        
        elif len(hashmap) == 2 and ' ' in hashmap.keys() and hashmap[' '] == 0:
            return True
        
        return False
    
    #checking whether all the elements in a column are same or not
    def is_goal(self):
        columns = len(self.__matrixRepresentation[0])
        temp = []
        
        for i in range(0, columns):
            
            for j in range(0, len(self.__matrixRepresentation)):
                temp.append(self.__matrixRepresentation[j][i])
                
            if not self.isAllSame(temp):
                return False
            temp = []
            
        return True

#actions class
class Actions:
    def __init__(self, matrix):
        self.__matrix = matrix
        self.__actionList = []
    
    #returns the list of all the possible actions from a given state
    def actions(self):
        for i in range(len(self.__matrix)):
            self.__actionList.append('rotate('+str(i)+',-1)')
            self.__actionList.append('rotate('+str(i)+',1)')
            
        columns = len(self.__matrix[0])      
        emptySpaceIndex = []
        
        for i in range(0, len(self.__matrix)):
            
            for j in range(0, columns):
                
                if matrix[i][j] == ' ':
                    emptySpaceIndex.append(i)
                    emptySpaceIndex.append(j)
        
        if emptySpaceIndex[0] == 0:
          self.__actionList.append('slide(' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0] + 1) + ',' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0]) + ')')
          
        elif emptySpaceIndex[0] == len(matrix) - 1:
          self.__actionList.append('slide(' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0] - 1) + ',' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0]) + ')')
        
        else:
           self.__actionList.append('slide(' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0] - 1) + ',' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0]) + ')')
           self.__actionList.append('slide(' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0] + 1) + ',' + str(emptySpaceIndex[1]) + ',' + str(emptySpaceIndex[0]) + ')')
        
        return self.__actionList
    
    #returning the string representation of the actionList
    def __str__(self):
        actionListString = ''
        
        for i in self.__actionList:
            actionListString += str(i) + '\n'
        
        return actionListString

#main routine and testing the input
if __name__ == '__main__':
    optionalArguement = ''
    state = State()
    
    if(len(sys.argv) < 2):
        print("The command arguement is missing")
        sys.exit(0)

    if len(sys.argv) < 3:
        optionalArguement = '12345|1234 |12354'
    else:
        optionalArguement = sys.argv[2]
    
    
    testString = optionalArguement.split("|")
    
    if len(testString) == 0:
        print("Given string is not formatted properly")
        sys.exit(0)
    
    length = len(testString[0])
    
    for i in testString:
        if len(i) != length:
            print("Given string is not formatted properly")
            sys.exit(0)
        
    count = 0
    for i in optionalArguement:
        if i == " ":
            count += 1
            
    if count != 1:
      print("Given string is not formatted properly")
      sys.exit(0)
    
    state = State(optionalArguement)
    state.setMatrixRepresentation()
    matrix = state.getMatrixRepresentation()
    
    action = Actions(matrix)
    actionList = action.actions()
    
    command = sys.argv[1]
    
    if command == 'print':
        state.print(matrix)
        
    elif command == 'goal':
        print(state.is_goal())
        
    elif command == 'actions':
        print(action)
        
    elif 'walk' in command:
        actionIndex = command[4:]
        if int(actionIndex) >= len(actionList):
            print("Given action cannot be executed at this time")
            sys.exit(0)
        state.execute(actionList[int(actionIndex)])