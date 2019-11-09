import cv2, numpy as np, time, os
from matplotlib import pyplot as plt

start = time.time()
directoryString = "C:/Users/Ron/Desktop/Files/UAV Fly Pics/Flight2/"
imageName = "Frame106"
imageExtension = ".jpg"
maxContours = 100
minContours = 2
# fileSaveString = "C:/Users/Ron/UAV/GCS/ManualClassification/assets/img"

image = cv2.imread(directoryString + imageName + imageExtension)
og = image.copy()


print("Preprocessing")
originalY, originalX, _ = og.shape
currY, currX = 700, 1200
image = cv2.resize(image, (1200, 700))
image2 = image.copy()
ogResized = image.copy()
cv2.imshow("Original Image (M2)", cv2.resize(image, (1200, 700)))

print("Thresholding + Contours")
iter = 1
num = 30
while True:
   blurred = cv2.bilateralFilter(image, 30, num, num)
   cv2.imshow("Blurred", blurred)
   image2 = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
   cv2.imshow("Grayscale", image2)
   _, threshold = cv2.threshold(image2, 200, 255, cv2.THRESH_BINARY) #Figure out appropriate threshold on image-to-image basis
   contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   print("Number of contours found:", len(contours))
   print("Iteration:", iter, "\nValue of n:", num)

   if 2 <= len(contours) <= maxContours:
      break
   elif len(contours) > maxContours:
      num += 10
      iter += 1
   elif len(contours) < minContours:
      if num < 10:
         break
      num -= 10
      iter += 1
os.chdir(directoryString)
# os.chdir(fileSaveString)
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    cv2.drawContours(image, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
# cv2.imwrite("1list.jpg", image)
for i in range(0, len(contours)):
   windowName = "Contour " + str(i)
   minX, minY = 10000000, 10000000
   maxX, maxY = 0, 0
   for point in contours[i]:
      point = point[0]
      if point[0] < minX:
         minX = point[0]
      if point[1] < minY:
         minY = point[1]
      if point[0] > maxX:
         maxX = point[0]
      if point[1] > maxY:
         maxY = point[1]
   if minX < 10:
      minX = 0
   else:
      minX -= 10
   if minY < 10:
      minY = 0
   else:
      minY -= 10
   if maxX > len(image[0]) - 10:
      maxX = len(image[0])
   else:
      maxX += 10
   if maxY > len(image) - 10:
      maxY = len(image)
   else:
      maxY += 10
   scaledMinY = int(minY * originalY / currY)
   scaledMaxY = int(maxY * originalY / currY)
   scaledMinX = int(minX * originalX / currX)
   scaledMaxX = int(maxX * originalX / currX)
   crop = og[scaledMinY: scaledMaxY, scaledMinX: scaledMaxX]
   crop = cv2.resize(crop, (len(crop[0])*10, len(crop)*10))
   fileName = "Target" + str(i) + ".png"
   # cv2.imwrite(fileName, crop)
print(time.time() - start)
cv2.imshow("Drawn Contours (M2)", image)
cv2.imshow("Final Image (M2)", threshold)
cv2.imwrite(imageName + "Concat.jpg", np.concatenate((np.concatenate((ogResized, blurred)), np.concatenate((image, cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR))))))
cv2.waitKey(0)