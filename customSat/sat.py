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
import operator
from functools import reduce
import time

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
validDirs = [UD, UL, UR, DL, DR, LR]
plainDir = [UP, DOWN, LEFT, RIGHT]
delta = {UP: (1, 0),
         DOWN: (-1, 0),
         LEFT: (0, -1),
         RIGHT: (0, 1)}

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

def colorHash(colorNum, row, col):
  return colorNum * (numRows * numCols) + row * numCols + col

# ret: colorInd, row, col
def colorUnhash(hash):
  return hash // (numRows * numCols), hash // numCols, hash % numCols

def dirHash(dirType, row, col):
  return dirType * (numRows * numCols) + row * numCols + col

# dirType, row, col
def dirUnhash(hash):
  return hash // (numRows * numCols), hash // numCols, hash % numCols

def generateColorClauses():
  clauses = []
  for row in range(len(grid)):
    for col in range(len(grid[row])):
      if(grid[row][col] == -1):
        arr = []
        for color in colors:
          arr.append(colorHash(row, col, color))
        clauses.append(arr)
        clauses.extend(noTwo(arr))
      else:
        for color in colors:
          if(color == grid[row][col]):
            clauses.append(colorHash(row, col, col))
          else:
            clauses.append(-colorHash(row, col, col))
  
  return clauses

def generateValidDirections():
  arrOfDirVar = []
  for rowInd in range(numRows):
    for colInd in range(numCols):
      invalidArgs = set()
      if(rowInd == 0):
        invalidArgs.add(UP)
      if(rowInd == numRows - 1):
        invalidArgs.add(DOWN)
      if(colInd == 0):
        invalidArgs.add(LEFT)
      if(colInd == numCols - 1):
        invalidArgs.add(RIGHT)
      tempArr = []
      for dirType in validDirs:
        mult = 1
        if(grid[rowInd][colInd] != '-1'):
          mult = -1

        if(reduce(operator.xor, invalidArgs, dirType) != dirType):
          mult = -1

        tempArr.append(mult * dirHash(dirType, rowInd, colInd))
      arrOfDirVar.append(tempArr)
  
  return arrOfDirVar


def generateDirectionClauses(dirVars):
  clauses = []
  for rcInd in range(len(dirVars)):
    if(dirVars[rcInd][0] < 0):
      continue
    clauses.append(dirVars[rcInd])
    clauses.append(noTwo(dirVars[rcInd]))

    for dirVar in dirVars[rcInd]:
      dirType, row, col = dirUnhash(dirVar)
      dirs = []
      for dir in plainDir:
        if dir | dirType == dirType:
          dirs.append(dir)
      con1Row, con1Col = row + delta[dirs[0]][0], col + delta[dirs[0]][1]
      con2Row, con2Col = row + delta[dirs[1]][0], col + delta[dirs[1]][1]
      for color in colors:
        hash1 = colorHash(color, row, col)
        hash2 = colorHash(color, con1Row, con1Col)
        hash3 = colorHash(color, con2Row, con2Col)
        clauses.append([-dirType, hash1, -hash2, -hash3])
        clauses.append([-dirType, -hash1, hash2, -hash3])
        clauses.append([-dirType, -hash1, -hash2, hash3])
      
    # skip squares that are start points
    # for not start make sure 1 dir var is valid for that node
    # make sure no 2 dir vars are valid for that node
    # for each dir possible in that node, make sure that the node and the 2 dirs connected by the dirVar all have same color
    # the combination of 3 clauses at end ignores clauses if wrong dir, it ignores color for clauses if wrong color, and it mandates
    # color of nodes if correct color
  
  return clauses

def generateSAT():
  clauses = generateColorClauses()
  numColorVars = len(colors) * numRows * numCols
  numColorClauses = len(clauses)
  dirs = generateValidDirections()
  clauses.extend(generateDirectionClauses(dirs))
  numDirVars = len(dirs)
  numDirClauses = len(clauses) - numColorClauses

  return clauses, numColorVars, numDirVars, numColorClauses, numDirClauses

def decodeSolution(sol, numColorVars):
  solGrid = [[]]
  
  for clauseInd in range(numColorVars):
    if(sol[clauseInd] > 0):
      solGrid[-1].append(colorUnhash(sol[clauseInd])[0])
      if(len(solGrid[-1]) == numRows):
        solGrid.append([])
  
  solGrid.pop()

  output_string = '\n'.join(
    [' '.join(map(str, row)) for row in solGrid]
  )

  return output_string

# def checkForCycles():

# def fixCycles():

def generateSolution(clauses):
  sol = pycosat.solve(clauses)
  return sol

def fullPipeline(gridInput):
  global numRows
  global numCols
  global colors
  global grid

  startTime = time.perf_counter()
  
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
  
  clauses, numColorVars, numDirVars, numColorClauses, numDirClauses = generateSAT()
  solution = generateSolution(clauses)

  totTime = time.perf_counter() - startTime
  
  sol = decodeSolution(solution, numColorVars)
  info = f"Took Time: {totTime}\n Number of Color Variables: {numColorVars}\n Number of Direction Variables: {numDirVars}\n Number of Color Clauses: {numColorClauses}\n Number of Direction Clauses: {numDirClauses}\n"
  path = 'POOPY PATH\n'

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