import numpy
import math

# --- 1. Set the print options globally ---
numpy.set_printoptions(
  precision = 6,
  suppress = True,
  floatmode = 'fixed'
)

SR3 = math.sqrt(3)

def sqr(a):
  return abs(a * a)

def quadForm(a, b, c):
  det = sqr(b) - 4 * a * c
  num1 = (-b + math.sqrt(det)) / (2 * a)
  num2 = (-b - math.sqrt(det)) / (2 * a)
  return num1, num2                      
  
# c1, c2, c3 are the centers, r is the radii for all 3                            
def intersectOfThreeSpheres(c1, c2, c3, r):
  # Create a new coordinate system that is based on teh c1, c2, c3 to simplfy calculations
  # new system x in on directional vector from c1 to c2
  # new system y is based on directional vector from c1 to c3 and its orthognal to x part (normalized)
  # new system z is based on cross product of x and y (naturally orthognal to both)
  xNonNorm = c2 - c1
  xNorm = xNonNorm / numpy.linalg.norm(xNonNorm)
  diffTwo = c3 - c1
  overlapX = numpy.dot(xNorm, diffTwo)
  yNonNorm = diffTwo - overlapX * xNorm
  yNorm = yNonNorm / numpy.linalg.norm(yNonNorm)
  e_z = numpy.cross(xNorm, yNorm)

  # Coordinates within new system:
  # c1 = (0, 0, 0)
  # c2 = (dist, 0, 0)
  # c3 = (overlapX, overlapY, 0)
  dist = numpy.linalg.norm(c2 - c1)
  overlapY = numpy.dot(yNorm, diffTwo)

  # Coordinates of intersections within new system
  # x intersection (since in our case all 3 spheres have same radius)
  # this becomes dist / 2 as half way between both sphere centers they intersect
  # y intersection equation is distilled from sphere 1 - sphere 3
  # y = (-2ix + ovlX^2 + ovlY^2) / 2j
  x = dist / 2
  y = (-2 * overlapX * x + overlapX * overlapX + overlapY * overlapY) / (2 * overlapY)
  
  # Just distance of radius equation!
  # zSquared must be positive for z to exist
  zSqrd = r * r - x * x - y * y
  if zSqrd<0:
    raise Exception("The three spheres do not intersect!")
  z = math.sqrt(zSqrd)

  # transform to world coordinate system
  p1 = c1 + x * xNorm + y * yNorm + z * e_z
  p2 = c1 + x * xNorm + y * yNorm - z * e_z
  return p2

rV = {}

dVec = {}

pVec = {}

# base side length, platform side length, thigh length, calf length
def defineRobot(bsl: float, psl: float, tl: float, cl: float):
  rV['sB'] = abs(bsl)
  rV['sP'] = abs(psl)
  rV['L'] = abs(tl)
  rV['l'] = abs(cl)

  rV['wB'] = rV['sB'] * SR3 / 6
  rV['uB'] = rV['sB'] * SR3 / 3
  rV['wP'] = rV['sP'] * SR3 / 6
  rV['uP'] = rV['sP'] * SR3 / 3

  rV['a'] = rV['wB'] - rV['uP']
  rV['b'] = rV['sP'] / 2 - SR3 * rV['wB'] / 2
  rV['c'] = rV['wP'] - rV['wB'] / 2
  

  pVec['BB1'] = numpy.array([0.0, -rV['wB'], 0.0])
  pVec['BB2'] = numpy.array([rV['wB'] * SR3 / 2.0, rV['wB'] / 2.0, 0.0])
  pVec['BB3'] = numpy.array([-rV['wB'] * SR3 / 2.0, rV['wB'] / 2.0, 0.0])

  pVec['PP1'] = numpy.array([0.0, -rV['uP'], 0.0])
  pVec['PP2'] = numpy.array([rV['sP'] / 2.0, rV['wP'], 0.0])
  pVec['PP3'] = numpy.array([-rV['sP'] / 2.0, rV['wP'], 0.0])
  

def calculateIK(x, y, z):
  E1 = 2 * rV['L'] * (y + rV['a'])
  F1 = 2 * z * rV['L']
  G1 = sqr(x) + sqr(y) + sqr(z) + sqr(rV['a']) + sqr(rV['L']) + 2 * y * rV['a'] - sqr(rV['l'])

  E2 = -rV['L'] * (SR3 * (x + rV['b']) + y + rV['c'])
  F2 = 2 * z * rV['L']
  G2 = sqr(x) + sqr(y) + sqr(z) + sqr(rV['b']) + sqr(rV['c']) + sqr(rV['L']) + 2 * (x * rV['b'] + y * rV['c']) - sqr(rV['l'])
  
  E3 = rV['L'] * (SR3 * (x - rV['b']) - y - rV['c'])
  F3 = 2 * z * rV['L']
  G3 = sqr(x) + sqr(y) + sqr(z) + sqr(rV['b']) + sqr(rV['c']) + sqr(rV['L']) + 2 * (-x * rV['b'] + y * rV['c']) - sqr(rV['l'])
  
  t1Pls, t1Mns = quadForm((G1 - E1), 2 * F1, (G1 + E1))

  t2Pls, t2Mns = quadForm((G2 - E2), 2 * F2, (G2 + E2))
  
  t3Pls, t3Mns = quadForm((G3 - E3), 2 * F3, (G3 + E3))
  
  theta1 = 180 * (math.atan(t1Pls)) / math.pi
  theta2 = 180 * (math.atan(t2Pls)) / math.pi
  theta3 = 180 * (math.atan(t3Pls)) / math.pi
  
  return 2 * theta1, 2 * theta2, 2 * theta3

def calculateFK(theta1, theta2, theta3):
  radT1 = theta1 * math.pi / 180.0
  radT2 = theta2 * math.pi / 180.0
  radT3 = theta3 * math.pi / 180.0

  dVec['BL1'] = numpy.array([0, -rV['L'] * math.cos(radT1) , -rV['L'] * math.sin(radT1)])
  dVec['BL2'] = numpy.array([rV['L'] * math.cos(radT2) * SR3 / 2, rV['L'] * math.cos(radT2) / 2, -rV['L'] * math.sin(radT2)])
  dVec['BL3'] = numpy.array([-rV['L'] * math.cos(radT3) * SR3 / 2, rV['L'] * math.cos(radT3) / 2, -rV['L'] * math.sin(radT3)])

  pVec['BA1'] = pVec['BB1'] + dVec['BL1']
  pVec['BA2'] = pVec['BB2'] + dVec['BL2']
  pVec['BA3'] = pVec['BB3'] + dVec['BL3']
  
  c1 = pVec['BA1'] - pVec['PP1']
  c2 = pVec['BA2'] - pVec['PP2']
  c3 = pVec['BA3'] - pVec['PP3']
  # c1 = numpy.array([0, -rV['wB'] - rV['L'] * math.cos(radT1) + rV['uP'], -rV['L'] * math.sin(radT1)])
  # c2 = numpy.array([ (rV['wB'] + rV['L'] * math.cos(radT2)) * SR3 / 2 - rV['sP'] / 2, (rV['wB'] + rV['L'] * math.cos(radT2)) / 2 - rV['wP'], -rV['L'] * math.sin(radT2)])
  # c3 = numpy.array([ rV['sP'] / 2 - (rV['wB'] + rV['L'] * math.cos(radT3)) * SR3 / 2, (rV['wB'] + rV['L'] * math.cos(radT3)) / 2 - rV['wP'], -rV['L'] * math.sin(radT3)])

  return intersectOfThreeSpheres(c1, c2, c3, rV['l'])

defineRobot(75, 12, 100, 230)
t1, t2, t3 = calculateIK(100, -50, -200)
print(t1, t2, t3)
print(calculateFK(t1, t2, t3))