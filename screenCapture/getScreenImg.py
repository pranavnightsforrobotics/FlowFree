import pyautogui
import cv2
import numpy as np
import time
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from customSat.sat import fullPipeline

time.sleep(3)

gridTopLeftX = 10
gridTopLeftY = 264
gridWidth = 300
gridHeight = 300

region = (gridTopLeftX, gridTopLeftY, gridWidth, gridWidth)
squareSize = 34

for i in range(44):
  screenshot = pyautogui.screenshot(None, region)

  frameRGB = np.array(screenshot)
  frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2BGR)

  arr = [[(-1, -1, -1) for _ in range(9)] for _ in range(9)]

  for row in range(9):
    for col in range(9):
      var = frameRGB[row * squareSize + squareSize // 2 - 3][col * squareSize + squareSize // 2 - 3]
      arr[row][col] = (int(var[0]), int(var[1]), int(var[2]))
      cv2.circle(frame, [col * squareSize + squareSize // 2 - 3, row * squareSize + squareSize // 2 - 3], 2, [0, 255, 0], -1)

  colToNum = {(0, 0, 0): -1}

  colorInd = 1

  puzzle = [[-1 for _ in range(9)] for _ in range(9)]

  def find_proximate_match(new_item, collection, dist=40):
    for existing_item in collection:
      if all(abs(new_item[i] - existing_item[i]) <= dist for i in range(3)):
        return existing_item
    
    return None

  for row in range(len(arr)):
    for col in range(len(arr[row])):

      m = find_proximate_match(arr[row][col], colToNum)

      if not m:
        colToNum[arr[row][col]] = colorInd
        colorInd += 1
        m = arr[row][col]

      puzzle[row][col] = colToNum[m]

  solStr, info, path, cost = fullPipeline(puzzle)

  print(solStr)
  print(info)
  print(path)
  print(cost)

  def convertToPixel(pos):
    y, x = pos
    pixX = gridTopLeftX + squareSize // 2 + x * squareSize
    pixY = gridTopLeftY + squareSize // 2 + y * squareSize
    return pixX, pixY

  for singlePath in path:
    # print(convertToPixel(singlePath[0]))
    pyautogui.moveTo(*convertToPixel(singlePath[0]), duration=0)
    for nextInd in range(1, len(singlePath)):
      # print(convertToPixel(singlePath[nextInd]))
      pyautogui.dragTo(*convertToPixel(singlePath[nextInd]), duration=0, button='left')

  pyautogui.moveTo(gridTopLeftX + gridWidth + 10, gridTopLeftY + gridHeight + 10, duration=0.1)
  time.sleep(1)

  # cv2.imshow('Captured Square', frame)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()