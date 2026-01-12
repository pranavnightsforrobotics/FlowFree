import cv2 as cv

xDiff = 42
yDiff = 16

arr = [[[-1, -1, -1] for _ in range(9)] for _ in range(9)]

img = cv.imread('./camera/postHomographFlow.png')
start = xDiff // 2, yDiff // 2
for row in range(len(arr)):
  for col in range(len(arr[row])):
    if(start[1] + yDiff * row > len(img) or start[0] + xDiff * col > len(img[0])):
      print('Out of bounds')
      break
    # print(img[start[1] + yDiff * row][start[0] + xDiff * col])
    arr[row][col] = list(img[start[1] + yDiff * row][start[0] + xDiff * col])
    cv.circle(img, [start[0] + xDiff * col, start[1] + yDiff * row], 2, [0, 255, 0], -1)

cv.imshow('name', img)
cv.waitKey(0)
cv.destroyAllWindows()

for a in arr:
  print(a)

# DarkTeal DarkBrown Black Black Black Black Black Black Black
# Black Black Black Rust/Brown Black Tan/Gold Black Black Black
# Olive Black Black Black DeepBlue Black Maroon Black Black
# DeepPink Black SkyBlue Black Black Red Black Black Black
# Black Black Black DarkBlue Black Black Black Black Black
# Black Black Black Black DarkBlue Black Black Black Purple
# Black Black Black Black PaleGold Black Black Black Black
# Black Black DarkOlive Black Black Black Black BrightBlue Black
# Black Black Black Black Black Black Black Black Black