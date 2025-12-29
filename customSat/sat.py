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

numColors = 10
showSol = False
showInfo = False
showPath = False

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

def encodeColorVar():
  global numColors

def decodeColorVar():

def generateColorClauses():

def encodeDirectionVar():

def decodeDirectionVar():

def generateValidDirections():

def generateDirectionClauses():

def generateSAT():

def decodeSolution():

def checkForCycles():

def fixCycles():

def generateSolution():


def fullPipeline(map):

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
  print('Positive Integers to represent each indvidual color, integer for like colors must match')
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