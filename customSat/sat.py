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
# cycle clauses just reject same path that leads to cycle

import pycosat

numColors = 10

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

def fullPipeline():