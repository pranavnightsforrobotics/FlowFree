delta = [[1,0], [-1,0], [0, 1], [0, -1]]

def computePathBrute(solGrid):
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
  
  minVal = 1000000000
  bestPath = []
  
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