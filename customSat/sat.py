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

def is_valid_integer(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def sizeOf2dArr(arr):
  cnt = 0
  for row in arr:
    for _ in row:
      cnt += 1
  
  return cnt

import sys
import pycosat
import operator
from functools import reduce
import time
import os

# Get the path to the FlowFree directory (one level up from customSat)
# Assuming sat.py is in FlowFree/customSat/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now use an absolute import path relative to the FlowFree root
from pto.pathTraversal import computePathBrute, computePathDP, computePathGreedy



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
delta = {UP: (-1, 0),
         DOWN: (1, 0),
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
  colorInd = hash // (numRows * numCols)
  remHash = hash % (numRows * numCols)
  row = remHash // numCols
  col = remHash % numCols
  
  return colorInd, row, col

def dirHash(dirType, row, col):
  return (dirType * (numRows * numCols) + row * numCols + col) + (numRows * numCols * len(colors))

# dirType, row, col
def dirUnhash(hash):
  hash -= numRows * numCols * len(colors)
  dirType = hash // (numRows * numCols)
  remHash = hash % (numRows * numCols)
  row = remHash // numCols
  col = remHash % numCols
  
  return dirType, row, col

def generateColorClauses():
  clauses = []
  for row in range(len(grid)):
    for col in range(len(grid[row])):
      if(grid[row][col] == -1):
        arr = []
        for color in colors:
          arr.append(colorHash(color, row, col))
        clauses.append(arr)
        clauses.extend(noTwo(arr))
      else:
        for color in colors:
          if(color == grid[row][col]):
            clauses.append([colorHash(color, row, col)])
          else:
            clauses.append([-colorHash(color, row, col)])
  
  return clauses

def generateValidDirections():
  arrOfDirVar = []

  endpointConnectClasues = []

  for rowInd in range(numRows):
    for colInd in range(numCols):
      if(grid[rowInd][colInd] != -1):
        validNeigh = []
        for data in delta.values():
          tRow = rowInd + data[0]
          tCol = colInd + data[1]
          if(tRow >= 0 and tRow < numRows and tCol >= 0 and tCol < numCols):
            validNeigh.append(colorHash(grid[rowInd][colInd], tRow, tCol))
        
        endpointConnectClasues.append(validNeigh)
        endpointConnectClasues.extend(noTwo(validNeigh))
        continue

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
        if(reduce(operator.or_, invalidArgs, 0) & dirType != 0 and invalidArgs):
          tempArr.append(-dirHash(dirType, rowInd, colInd))
        else:
          tempArr.append(dirHash(dirType, rowInd, colInd))
        
      arrOfDirVar.append(tempArr)

  return arrOfDirVar, endpointConnectClasues


def generateDirectionClauses(dirVars):
  clauses = []

  for rcInd in range(len(dirVars)):
    valid = []
    for dirVar in dirVars[rcInd]:
      if(dirVar < 0):
        clauses.append([dirVar])
        continue

      valid.append(dirVar)
      
      dirType, row, col = dirUnhash(dirVar)
      dirs = []
      nonDirs = []
      for dir in plainDir:
        if dir | dirType == dirType:
          dirs.append(dir)
        else:
          nonDirs.append(dir)

      con1Row, con1Col = row + delta[dirs[0]][0], col + delta[dirs[0]][1]
      con2Row, con2Col = row + delta[dirs[1]][0], col + delta[dirs[1]][1]

      nonCon1Row, nonCon1Col = row + delta[nonDirs[0]][0], col + delta[nonDirs[0]][1]
      nonCon2Row, nonCon2Col = row + delta[nonDirs[1]][0], col + delta[nonDirs[1]][1]

      for color in colors:
        hash1 = colorHash(color, row, col)
        hash2 = colorHash(color, con1Row, con1Col)
        hash3 = colorHash(color, con2Row, con2Col)

        hash4 = colorHash(color, nonCon1Row, nonCon1Col)
        hash5 = colorHash(color, nonCon2Row, nonCon2Col)
        
        # If this direction is active, current cell and neighbor1 must have same color
        clauses.append([-dirVar, -hash1, hash2])
        clauses.append([-dirVar, hash1, -hash2])
        
        # If this direction is active, current cell and neighbor2 must have same color
        clauses.append([-dirVar, -hash1, hash3])
        clauses.append([-dirVar, hash1, -hash3])

        # make color similarity for non direction following nodes illegal essentially
        # mandate only direction nodes have same color and other nodes have different color
        if(nonCon1Row >= 0 and nonCon1Row < numRows and nonCon1Col >= 0 and nonCon1Col < numCols):
          clauses.append([-dirVar, -hash1, -hash4])
        if(nonCon2Row >= 0 and nonCon2Row < numRows and nonCon2Col >= 0 and nonCon2Col < numCols):
          clauses.append([-dirVar, -hash1, -hash5])
        
    
    if(valid):
      clauses.append(valid)
      clauses.extend(noTwo(valid))
      
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
  dirs, endPointClauses = generateValidDirections()
  directionClauses = generateDirectionClauses(dirs)
  
  clauses.extend(directionClauses)
  clauses.extend(endPointClauses)
  numDirVars = sizeOf2dArr(dirs)
  numDirClauses = len(clauses) - numColorClauses

  return clauses, numColorVars, numDirVars, numColorClauses, numDirClauses

def decodeSolution(sol, numColorVars):
  solGrid = []

  solSet = set(sol)

  for _ in range(numRows):
    solGrid.append([])
    for _i in range(numCols):
      solGrid[-1].append([-1, -1])

  for clause in range(numRows * numCols, numRows * numCols + numColorVars):
    if(clause in solSet):
      yur = colorUnhash(clause)
      solGrid[yur[1]][yur[2]][0] = yur[0]
      if(grid[yur[1]][yur[2]] != -1):
        solGrid[yur[1]][yur[2]][1] = -1
      else:
        for dir in validDirs:
          if(dirHash(dir, yur[1], yur[2]) in solSet):
            solGrid[yur[1]][yur[2]][1] = dirHash(dir, yur[1], yur[2])

  output_string = '\n'.join(
    ['  '.join(str(cell[0]).rjust(2) for cell in row) for row in solGrid]
  )

  return output_string, solGrid

# take input of solGrid and iter through things and explore all nodes that are adjacent to it in a 1d dfs manner

def fixCycles(solGrid):
  visited = [[False for _ in range(len(solGrid[0]))] for _ in range(len(solGrid))]
  color = [False for _ in range(len(colors))]
  colorDirClauses = [[] for _ in colors]

  extraClauses = []

  def dfs(row, col, isSingle, endAtEnd, pathSoFar):
    if(solGrid[row][col][1] != -1):
      pathSoFar.append(solGrid[row][col][1])
    
    elif(endAtEnd):
      return pathSoFar, True

    visited[row][col] = True

    for x, y in delta.values():
      nRow, nCol = row + x, col + y
      if((0 <= nRow < numRows) and (0 <= nCol < numCols) and not visited[nRow][nCol] and solGrid[nRow][nCol][0] == solGrid[row][col][0]):
        pathSoFar, var = dfs(nRow, nCol, isSingle, isSingle, pathSoFar)
        if(isSingle):
          return pathSoFar, var
    
    return pathSoFar, False

  for row in range(len(solGrid)):
    for col in range(len(solGrid[row])):
      if(solGrid[row][col][1] == -1 and not visited[row][col]):
        path, isGood = dfs(row, col, True, False, [])

        if(not isGood):
          extraClauses.append([-var for var in path])

        else:
          colorDirClauses[solGrid[row][col][0] - 1] = path
  
  for row in range(len(solGrid)):
    for col in range(len(solGrid[row])):
      if(not visited[row][col]):
        color[solGrid[row][col][0] - 1] = True
        path, isGood = dfs(row, col, False, False, [])

        if not colorDirClauses[solGrid[row][col][0] - 1]:
          colorDirClauses[solGrid[row][col][0] - 1] = path
        else:
          extraClauses.append([-var for var in path])
      
  return [item for item in extraClauses if item != []]

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
  solStr, solGrid = decodeSolution(solution, numColorVars)

  extraClauses = fixCycles(solGrid)
  totExtra = len(extraClauses)

  while extraClauses:
    print(extraClauses)
    clauses.extend(extraClauses)
    solution = generateSolution(clauses)
    solStr, solGrid = decodeSolution(solution, numColorVars)
    
    extraClauses = fixCycles(solGrid)
    totExtra += len(extraClauses)
  
  path = computePathDP(solGrid)
  # path = computePathGreedy(solGrid)
  # path = computePathBrute(solGrid)

  totTime = time.perf_counter() - startTime
  info = f"Took Time: {totTime}\n Number of Color Variables: {numColorVars}\n Number of Direction Variables: {numDirVars}\n Number of Color Clauses: {numColorClauses}\n Number of Direction Clauses: {numDirClauses}\n Amount of Extra Clauses: {totExtra}"
  
  return solStr, info, path

def handleBadInput():
  print('ERROR: Called SAT solver with incorrect argument type')
  print('Please call with following format: \'python3 ...../sat.py -s -i -p ...../puzzleLoc.txt\'')
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
      if(not is_valid_integer(num)):
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
  
  if((-1 not in numCheck and numCheck) or len(numCheck) > 1):
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
  
  sol, info, path = fullPipeline(puzz)

  if(showInfo):
    print(info)
  
  if(showSol):
    print(sol)
  
  if(showPath):
    print(path)