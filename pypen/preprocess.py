import os
import cv2
import numpy as np
from skimage.io import imsave
from skimage.transform import rescale
from string import ascii_lowercase, ascii_uppercase

def find_centroid(img) :
    x, y, ctr = 0, 0, 0
    for i in range(len(img)) :
        for j in range(len(img[i])) :
            if img[i][j] < 255:
                ctr += 1
                x += i
                y += j 

    return int(x/ctr), int(y/ctr)

def crop_img(img, x, y, lx, ly) :
    lx, ly = int(lx/2), int(ly/2)
    minx, miny = max(x-lx, 0), max(y-ly, 0)
    maxx, maxy = min(x+lx, img.shape[0]), min(y+ly, img.shape[1])

    return img[minx : maxx, miny : maxy]

def gen_letters(source, width=400, height=400, output="proc_letters") :
    WIDTH = width
    HEIGHT = height
    MIN_DIM = int(1.25*min(WIDTH, HEIGHT))

    try :
        os.mkdir(f"{output}")
    except FileExistsError :
        print(f"{output} already exists ...")


    for letter in ascii_uppercase :
        img = cv2.imread(f"{source}/uppercase/{letter}.jpg", 0)
        SCALE_FACTOR = (MIN_DIM/min(img.shape))
        img = rescale(img, SCALE_FACTOR) 
        
        Gx, Gy = find_centroid(img)
        print(f"{letter}: Gx={Gx}, Gy={Gy}") 
        img = crop_img(img, Gx, Gy, HEIGHT, WIDTH)
        print(img.shape)
        
        cv2.imshow(f'{letter}', img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

        imsave(f"{output}/{letter}.png", img)
        print(f"saved as {output}/{letter}.png ...")

    for letter in ascii_lowercase :
        img = cv2.imread(f"{source}/lowercase/{letter}.jpg", 0)
        SCALE_FACTOR = (MIN_DIM/min(img.shape))
        img = rescale(img, SCALE_FACTOR) 
        
        Gx, Gy = find_centroid(img)
        print(f"{letter}: Gx={Gx}, Gy={Gy}") 
        img = crop_img(img, Gx, Gy, HEIGHT, WIDTH)
        print(img.shape)
        
        cv2.imshow(f'{letter}', img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()

        imsave(f"{output}/{letter}.png", img)
        print(f"saved as {output}/{letter}.png ...")
