import cv2
import numpy as np
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import sys



# img_path = 'test1.jpeg'
img_path_temp = 'test_temp.jpeg'
img_op = "whoami.txt"
img_bg_path = "whoami.png"

sens = 120
inverted = 1
img_size = (250,100)
txt_size = (140,40)

inverted = int(sys.argv[-1])

text_color = 0
bg_color = 0

if(inverted):
    bg_color = 0
    text_color = 255
else:
    bg_color = 255
    text_color = 0

def get_image():

    cam = cv2.VideoCapture(0)

    while True:
        status, img = cam.read(img_size)
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) == ord('q'):
            break
        cv2.imwrite(img_path_temp, img)

def resize_image(img_path,size):

    img = Image.open(img_path)
    img_resized = img.resize(size)
    img_resized.save(img_path_temp)

def make_new(img_path):

    img = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)

    pic_array = np.zeros(((len(img),len(img[0]))))

    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] >= sens:
                pic_array[i][j] = inverted
            else:
                pic_array[i][j] = not inverted

    #print(pic_array)
    return pic_array


def make_blank_slate(img_size):
    bg = np.ones((16*img_size[1],9*img_size[0]))
    bg[bg == 1] = bg_color
    cv2.imwrite(img_bg_path,bg)

def write_to_slate(text):
    img = Image.open(img_bg_path)
    img_draw = ImageDraw.Draw(img)

    img_font = ImageFont.truetype('FreeMono.ttf', 1)


    for i in range(len(text)):
        for j in range(len(text[i])):
            if(
            i>1 and j>1 and i<len(text)-1 and j<len(text[i])-1 and\
            text[i-1][j] and text[i+1][j] and\
            text[i][j-1] and text[i][j+1] and\
            text[i-1][j-1] and text[i+1][j+1] and\
            text[i+1][j-1] and text[i-1][j+1]and\
            text[i][j]):
                img_draw.text((9*j, 16*i),"@",fill=int(text_color))
            elif(text[i][j]):
                img_draw.text((9*j, 16*i),"#",fill=int(text_color))


    img.show()
    img.save(img_bg_path)


def write_to_text(text):

    global img_op

    f = open(img_op,"w")
    f.write("")
    f.close()

    #saving to text
    f = open(img_op,"a")
    for i in range(len(text)):
        for j in range(len(text[i])):
            if(
            i>1 and j>1 and i<len(text)-1 and j<len(text[i])-1 and\
            text[i-1][j] and text[i+1][j] and\
            text[i][j-1] and text[i][j+1] and\
            text[i-1][j-1] and text[i+1][j+1] and\
            text[i+1][j-1] and text[i-1][j+1]and\
            text[i][j]):
                f.write(str('@'))
            elif(text[i][j]):
                f.write(str('#'))
            else:
                f.write(str(' '))
        f.write("\n")
    f.close()



get_image()

#prep for image
resize_image(img_path_temp,img_size)
text = make_new(img_path_temp)

#make image
make_blank_slate(img_size)
write_to_slate(text)

#prep for text
resize_image(img_path_temp,txt_size)
text = make_new(img_path_temp)

#remove temp files
os.remove(img_path_temp)

write_to_text(text)
