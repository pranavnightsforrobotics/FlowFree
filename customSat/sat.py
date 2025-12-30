# must generate color clauses
# must generate directional clauses
# must create clause -> graph
# must create graph cycle detection split each series of nodes into their own graph and then do DAGS construction on these graphs
# if impossible then we have a cycle, if possible then no cycle, make direction static incase -> <- collision exists!!
# must create new clauses to avoid continued cycle creation

# colorClauseBlank = (red or blue or green or yellow or ...)
# colorClauseNode = (red)

# dirClause = (all valid dirs: lr, or br, or tr, or ...)
# dirColorClause = lr and (red1 or blue1) and (red2 or blue1) and (red1 or blue2) and (red2 or blue2) or tb and (red1 or blue1) and (red2 or blue1) and (red1 or blue2) and (red2 or blue2) 


# color clauses isolate which color should exist for 1 square
# direction clauses mandate color and direction based on which direct is true but they do not mandate a direction
# cycle clauses just reject same path that leads to 

import sys
import pycosat

UP = 1
DOWN = 2
LEFT = 4
RIGHT = 8

UD = UP | DOWN
UL = UP | LEFT
UR = UP | RIGHT
DL = DOWN | LEFT
DR = DOWN | RIGHT
LR = LEFT | RIGHT

numRows = -1
numCols = -1
colors = []
grid = [[]]

# color hash = colorInd * gridSize + rowInd * colSize + colInd
# dir hash = dirType * gridSize + rowInd * colSize + colInd

# Helpers
def allPairs(data):
  for i in range(len(data) - 1):
    for j in range(i + 1, len(data)):
      yield [data[i], data[j]]

def noTwo(data):
  arr = []
  for elem in allPairs(data):
    arr.append([-elem[0], -elem[1]])
  return arr

def colorHash(row, col, colorNum):
  return colorNum * (numRows * numCols) + row * numCols + col 

# ret: colorInd, row, col
def colorUnhash(hash):
  return hash // (numRows * numCols), hash // numCols, hash % numCols

def generateColorClauses():
  global grid
  global colors
  clauses = []
  for row in range(len(grid)):
    for col in range(len(grid[row])):
      arr = []
      if(grid[row][col] == -1):
        for color in colors:
          arr.append(colorHash(row, col, color))
        clauses.append(arr)
        clauses.append(noTwo(arr))
      else:
        for color in colors:
          if(color == grid[row][col]):
            arr.append(colorHash(row, col, col))
          else:
            arr.append(-colorHash(row, col, col))
        clauses.append(arr)
  
  return clauses

def dirHash():

def dirUnhash():

def generateValidDirections():

def generateDirectionClauses():

def generateSAT():

def decodeSolution():

def checkForCycles():

def fixCycles():

def generateSolution():


def fullPipeline(gridInput):
  global numRows
  global numCols
  global colors
  global grid

  numCols = len(gridInput[0])
  numRows = len(gridInput)
  grid = gridInput
  unique = set()
  colors.clear()

  for row in grid:
    for elem in row:
      if elem not in unique:
        unique.add(elem)
        if(elem != -1):
          colors.append(elem)

  return sol, info, path

def handleBadInput():
  print('ERROR: Called SAT solver with incorrect argument type')
  print('Please call with following format: \'python3 ...../sat.py -s -i -g ...../puzzleLoc.txt\'')
  print('-s shows the solution in terminal')
  print('-i shows information about solving process in terminal')
  print('-p shows the recommended solution path')
  sys.exit()

def handleBadPuzzle():
  print('ERROR: Called SAT solver with incorrect puzzle format')
  print('Please call with following format: ')
  print('-1 to represent blank squares')
  print('1 to n to represent each unique color, integer for like colors must match')
  print('Spaces for colum-wise seprations')
  print('Newlines for row-wise seprations')
  print('Ensure each row has the same number of squares')
  sys.exit()

def examinePuzzleFile(filePath):
  arr = []
  lines = []
  try:
    with open(filePath, 'r') as file:
      lines = file.readlines()

  except FileNotFoundError:
    print(f"Error: The file '{filePath}' was not found.")
  
  for line in lines:
    processed_line = line.strip().split()
    arr.append([])
    for num in processed_line:
      if(not num.isdigit()):
        handleBadPuzzle()
      arr[-1].append(int(num))
    
    length = len(arr[0])

    if(len(arr[-1]) != length):
      handleBadPuzzle()
  
  numCheck = set()
  for row in arr:
    for num in row:
      if(num not in numCheck):
        numCheck.add(num)
      else:
        numCheck.remove(num)
  
  if(numCheck):
    handleBadPuzzle()
  
  return arr

if __name__ == "__main__":
  numArgs = len(sys.argv)
  if numArgs < 2:
    handleBadInput()

  validArgs = set(['-s', '-i', '-p'])

  puzzleFileName = ''
  showSol = False
  showInfo = False
  showPath = False

  for elem in range(1, len(sys.argv)):
    if(sys.argv[elem] not in validArgs):
      if(not sys.argv[elem].endswith('.txt')):
        handleBadInput()
      else:
        puzzleFileName = sys.argv[elem]
    else:
      if(sys.argv[elem] == '-s'):
        showSol = True
      elif(sys.argv[elem] == '-i'):
        showInfo = True
      elif(sys.argv[elem] == '-p'):
        showPath = True
  
  puzz = examinePuzzleFile(puzzleFileName)

  if(not puzz):
    handleBadPuzzle()
  
  sol, info, path = fullPipeline(puzz)

  if(showInfo):
    print(info)
  
  if(showSol):
    print(sol)
  
  if(showPath):
    print(path)