import cv2
import numpy as np
from PIL import Image
import os


# img_path = 'test1.jpeg'
img_path_temp = 'test_temp.jpeg'
img_op = "whoami.txt"

def get_image():

    cam = cv2.VideoCapture(0)

    while True:
        status, img = cam.read()
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) == ord('q'):
            break
        cv2.imwrite(img_path_temp, img)

def resize_image(img_path):

    img = Image.open(img_path)
    img_resized = img.resize((170,54))
    img_resized.save(img_path_temp)

def make_new(img_path):

    img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)

    pic_array = np.zeros(((len(img),len(img[0]))))

    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] >= 80:
                pic_array[i][j] = int(1)
            else:
                pic_array[i][j] = int(0)

    #print(pic_array)
    return pic_array


get_image()
resize_image(img_path_temp)
text = make_new(img_path_temp)

os.remove(img_path_temp)

f = open(img_op,"w")
f.write("")
f.close()

f = open(img_op,"a")
for i in range(len(text)):
    for j in range(len(text[i])):
        if(text[i][j]):
            f.write(str('#'))
        else:
            f.write(str(' '))
    f.write("\n")
f.close()
