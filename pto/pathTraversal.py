delta = [[1,0], [-1,0], [0, 1], [0, -1]]

def generateColorPath(solGrid):
  colorPath = {}
  
  def traverseThrough(row, col):
    prev = ()
    cur = (row, col)
    order = []
    order.append(cur)

    while(solGrid[cur[0]][cur[1]][1] != -1 or (cur[0] == row and cur[1] == col)):
      for x, y in delta:
        nX, nY = cur[0] + x, cur[1] + y
        if((0 <= nX < len(solGrid)) and (0 <= nY < len(solGrid[0])) and (nX, nY) != prev and solGrid[nX][nY][0] == solGrid[cur[0]][cur[1]][0]):
          prev = cur
          cur = (nX, nY)
          order.append(cur)
          break
    
    return order

  for row in range(len(solGrid)):
    for col in range(len(solGrid[row])):
      color = solGrid[row][col][0]
      if color not in colorPath and solGrid[row][col][1] == -1:
        colorPath[color] = traverseThrough(row, col)

  return colorPath

def computePathBrute(solGrid):
  colorPath = generateColorPath(solGrid)
  
  minVal = 1000000000
  bestPath = []

  memo = {}
  
  def backTrack(doneSoFar, cntSoFar, startingPoint, order):
    nonlocal minVal
    nonlocal bestPath
    if cntSoFar >= minVal:
      return
    
    for color in colorPath:
      if(color not in doneSoFar):
        doneSoFar.add(color)
        addational = len(colorPath[color]) - 1 + abs(startingPoint[0] - colorPath[color][0][0]) + abs(startingPoint[1] - colorPath[color][0][1])
        tempOrder = order + colorPath[color]
        backTrack(doneSoFar, cntSoFar + addational, (colorPath[color][-1][0], colorPath[color][-1][1]), tempOrder)

        addational = len(colorPath[color]) - 1 + abs(startingPoint[0] - colorPath[color][-1][0]) + abs(startingPoint[1] - colorPath[color][-1][1])
        tempOrder = order + colorPath[color][::-1]
        backTrack(doneSoFar, cntSoFar + addational, (colorPath[color][0][0], colorPath[color][0][1]), tempOrder)

        doneSoFar.remove(color)
    
    if(len(doneSoFar) == len(colorPath) and cntSoFar < minVal):
      minVal = cntSoFar
      bestPath = order
  
  for r in range(len(solGrid)):
    for c in range(len(solGrid[r])):
      backTrack(set(), 0, (r, c), [])

  print(minVal)
  print(bestPath)

  return 'Poopy Path\n'

def computePathDP(solGrid):
  colorPath = generateColorPath(solGrid)

  # set up base case

  allColors = frozenset(colorPath.keys())

  memo = {}
  for x in range(len(solGrid)):
    for y in range(len(solGrid[x])):
      memo[(x, y, frozenset())] = (0, [])

  minVal = 100000000000
  minPath = []
  
  def backTrack(remaning, startingPoint):
    key = (startingPoint[0], startingPoint[1], remaning)

    if(key in memo):
      return memo[key]
    
    bestCst = float('inf')
    bestPath = []
    
    for color in remaning:
      start = colorPath[color][0]
      end = colorPath[color][-1]
      pathCst = len(colorPath[color]) - 1
      jumpCst = abs(start[0] - startingPoint[0]) + abs(start[1] - startingPoint[1])

      remNew = remaning - {color}
      
      remCst, remPath = backTrack(remNew, end)
      
      if(remCst + jumpCst + pathCst < bestCst):
        bestCst = remCst + jumpCst + pathCst
        bestPath = colorPath[color] + remPath

      jumpCst = abs(end[0] - startingPoint[0]) + abs(end[1] - startingPoint[1])

      remCst, remPath = backTrack(remNew, start)
      
      if(remCst + jumpCst + pathCst < bestCst):
        bestCst = remCst + jumpCst + pathCst
        bestPath = colorPath[color][::-1] + remPath    
    
    memo[key] = (bestCst, bestPath)
    return bestCst, bestPath
  
  for color in colorPath:
    tempVal, tempPath = backTrack(allColors, colorPath[color][0])
    if(tempVal < minVal):
      minVal = tempVal
      minPath = tempPath

    tempVal, tempPath = backTrack(allColors, colorPath[color][-1])
    if(tempVal < minVal):
      minVal = tempVal
      minPath = tempPath

  print(minVal)
  print(minPath)

  return 'Poopy Path\n'