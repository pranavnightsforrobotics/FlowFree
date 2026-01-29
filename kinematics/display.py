import mesh as m
import kin as k
import open3d as o3d
import numpy as np
import time
from functools import partial

# kinematics setup
k.defineRobot(242, 42, 100, 230, 30)
goalX = 0
goalY = 0
goalZ = -200

# Visualization setup
vis = o3d.visualization.VisualizerWithKeyCallback()
coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10.0)
vis.create_window()
vis.get_render_option().background_color = np.asarray([0, 0, 0])

def redraw():
  global goalX, goalY, goalZ
  ang1, ang2, ang3 = k.calculateIK(goalX, goalY, goalZ)
  testPos = k.calculateFK(ang1, ang2, ang3)

  if(abs(testPos[0] - goalX) < 0.1 and abs(testPos[1] - goalY) < 0.1 and abs(testPos[2] - goalZ) < 0.1):
    basePos, baseSideLen, botPos, botSideLen, base1Pos, base2Pos, base3Pos, knee1Pos, knee2Pos, knee3Pos, disPal1, disPal2, disPal3, bot1Pos, bot2Pos, bot3Pos = k.givePositionsFromTheta(ang1, ang2, ang3)
    # print('IK, FK results match moving forward to display')
    # print(ang1, ang2, ang3)
    basePrism = m.create_custom_triangular_prism(baseSideLen, 1, basePos, False)
    botPrism = m.create_custom_triangular_prism(botSideLen, 1, botPos, True)
    thigh1 = m.create_custom_pipe(9.5, base1Pos, knee1Pos)
    thigh2 = m.create_custom_pipe(9.5, base2Pos, knee2Pos)
    thigh3 = m.create_custom_pipe(9.5, base3Pos, knee3Pos)
    calf1 = m.create_custom_parallelogram(9.5, knee1Pos, bot1Pos, disPal1)
    calf2 = m.create_custom_parallelogram(9.5, knee2Pos, bot2Pos, disPal2)
    calf3 = m.create_custom_parallelogram(9.5, knee3Pos, bot3Pos, disPal3)

    vis.clear_geometries()
    vis.add_geometry(coordinate_frame)
    vis.add_geometry(basePrism)
    vis.add_geometry(botPrism)
    vis.add_geometry(thigh1)
    vis.add_geometry(thigh2)
    vis.add_geometry(thigh3)
    vis.add_geometry(calf1)
    vis.add_geometry(calf2)
    vis.add_geometry(calf3)
  
  else:
    print(testPos)
    print('SOMETHING FAILED FUCK')

def upCallback(vis):
  global goalZ
  goalZ += 1
  redraw()
  return True

def downCallback(vis):
  global goalZ
  goalZ -= 1
  redraw()
  return True

def leftCallback(vis):
  global goalX
  goalX -= 1
  redraw()
  return True

def rightCallback(vis):
  global goalX
  goalX += 1
  redraw()
  return True

def forwardCallback(vis):
  global goalY
  goalY += 1
  redraw()
  return True

def backwardCallback(vis):
  global goalY
  goalY -= 1
  redraw()
  return True
  
def lerpCallBack(vis):
  global goalX, goalY, goalZ
  goalX, goalY, goalZ = 0, 0, -200
  redraw()
  ang1Init, ang2Init, ang3Init = k.calculateIK(goalX, goalY, goalZ)

  newGoalX, newGoalY, newGoalZ = 100, 0, -200
  ang1Fin, ang2Fin, ang3Fin = k.calculateIK(newGoalX, newGoalY, newGoalZ)

  angDis1, angDis2, angDis3 = (ang1Fin - ang1Init), (ang2Fin - ang2Init), (ang3Fin - ang3Init)

  for i in range(0, 100, 5):
    lerpLevel = 0.01 * i

    tempAng1, tempAng2, tempAng3 = ang1Init + angDis1 * lerpLevel, ang2Init + angDis2 * lerpLevel, ang3Init + angDis3 * lerpLevel
    goalX, goalY, goalZ = k.calculateFK(tempAng1, tempAng2, tempAng3)
    print(goalX, goalY, goalZ)
    redraw()
    time.sleep(0.01)

  goalX, goalY, goalZ = 100, 0, -200
  redraw()

  return True


vis.register_key_callback(ord("Y"), forwardCallback)
vis.register_key_callback(ord("H"), backwardCallback)
vis.register_key_callback(ord("G"), leftCallback)
vis.register_key_callback(ord("T"), upCallback)
vis.register_key_callback(ord("U"), downCallback)
vis.register_key_callback(ord("J"), rightCallback)
vis.register_key_callback(ord('B'), lerpCallBack)

vis.run()