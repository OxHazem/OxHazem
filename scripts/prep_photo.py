import cv2
from rembg import remove
import sys

input_path = sys.argv[1]
output_path = 'source-prepped.png'

# 1. Remove the background
with open(input_path, 'rb') as i:
    subject_only = remove(i.read())
with open('temp.png', 'wb') as o:
    o.write(subject_only)

# 2. Boost contrast so the ASCII looks 3D
img = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
contrasted = clahe.apply(img)

cv2.imwrite(output_path, contrasted)
print("Success! Created source-prepped.png")