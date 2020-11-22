import os 
import cv2
import pickle
import imageio
import numpy as np
from time import sleep
from textwrap import wrap
from string import ascii_uppercase
from skimage.transform import rescale

def convert_txt_to_hdwn(input="", letters="letters", lttr_size=25, tgt_typ="png", output="handwritten-doc") :  
    lines = wrap(input, width=70)
    print(lines)

    num_lines = len(lines)
    for i, line in enumerate(lines) :
        lines[i] = ' '.join(line.split())

    max_char_count = max([len(line) for line in lines])
    letter_table = {}
    filelist = []
    for dirname, dirnames, filenames in os.walk(f'{letters}') :
        for subdirname in dirnames:
            filelist.append(os.path.join(dirname, subdirname))
        
        for filename in filenames:
            filelist.append(os.path.join(dirname, filename))

    filelist = sorted(filelist)
    for filename in filelist :
        temp = cv2.imread(filename, 0)
        # temp = cv2.threshold(temp, 128, 255, cv2.THRESH_BINARY)[1]
        kernel = np.ones(shape=(5,5))
        temp = cv2.erode(temp, kernel, iterations = 5)
        temp = cv2.dilate(temp, kernel, iterations = 2)
        letter_table[filename.split('.')[0][-1:]] = cv2.resize(temp, (lttr_size, lttr_size))
    letter_table[' '] = np.full((lttr_size, lttr_size), 255, dtype=np.uint8)

    shape = (num_lines*lttr_size, (max_char_count+1)*lttr_size)
    hdwn_img = np.zeros(shape=(lttr_size, shape[1]), dtype=np.uint8)
    for line in lines :
        letter_img = np.zeros(shape=(lttr_size, lttr_size), dtype=np.uint8)
        for letter in line :
            letter_img = np.concatenate((letter_img, letter_table[letter]), axis=1)
            # cv2.imshow('temp', letter_img)
            # cv2.waitKey(500)
            # cv2.destroyAllWindows()
        for i in range(max_char_count-len(line)) :
            letter_img = np.concatenate((letter_img, letter_table[' ']), axis=1)
        # enter a line of space
        hdwn_img = np.concatenate((hdwn_img, letter_img))
        hdwn_img = np.concatenate((hdwn_img, np.full((5, hdwn_img.shape[1]), 255, dtype=np.uint8)))
        # cv2.imshow('temp', hdwn_img)
        # cv2.waitKey(1000)
        # cv2.destroyAllWindows()

    hdwn_img =  hdwn_img[lttr_size:,lttr_size:]
    print(hdwn_img.shape)

    if tgt_typ in ['png', 'jpg', 'svg'] :
        # with open(f"{output}.pkl", 'wb') as f :
        #     pickle.dump(hdwn_img, f)
        hdwn_img = hdwn_img.astype(np.uint8)
        imageio.imwrite(f"{output}.{tgt_typ}", hdwn_img)
        # plt.imsave(f"{output}.{tgt_typ}", hdwn_img)

    # cv2.imshow('temp', hdwn_img)
    # cv2.waitKey(10000)
    # cv2.destroyAllWindows()

    return hdwn_img.shape

def convert_doc_to_hdwn(input="input.txt", letters="letters", lttr_size=25, tgt_typ="png", output="handwritten-doc") :
    txt = open(input,"r").read().strip()
    convert_txt_to_hdwn(txt, letters, lttr_size, tgt_typ, output)

# to view the pickle file output 
def view_hdwn_document(input="handwritten-doc.pkl") :
    hdwn_img = np.load(input, allow_pickle=True)
    print(hdwn_img.shape)

    i = 0
    try:
        while True:
            i+=1
            cv2.imshow(input, hdwn_img)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
    except:
        cv2.destroyAllWindows()
            
































# def convert_doc_to_hdwn(input="input.txt", letters="letters", lttr_size=25, tgt_typ="png", output="handwritten-doc") :
#     txt = open(input, "r").read().strip()  
#     lines = wrap(txt, width=50)
#     print(lines)

#     num_lines = len(lines)
#     for i, line in enumerate(lines) :
#         lines[i] = ' '.join(line.split())

#     max_char_count = max([len(line) for line in lines])
#     letter_table = {}
#     filelist = []
#     for dirname, dirnames, filenames in os.walk(f'{letters}') :
#         for subdirname in dirnames:
#             filelist.append(os.path.join(dirname, subdirname))
        
#         for filename in filenames:
#             filelist.append(os.path.join(dirname, filename))

#     filelist = sorted(filelist)
#     for filename in filelist :
#         temp = cv2.imread(filename, 0)
#         # temp = cv2.threshold(temp, 128, 255, cv2.THRESH_BINARY)[1]
#         kernel = np.ones(shape=(5,5))
#         temp = cv2.erode(temp, kernel, iterations = 10)
#         temp = cv2.dilate(temp, kernel, iterations = 7)
#         letter_table[filename.split('.')[0][-1:]] = cv2.resize(temp, (lttr_size, lttr_size))
#     letter_table[' '] = np.full((lttr_size, lttr_size), 255, dtype=np.uint8)

#     shape = (num_lines*lttr_size, (max_char_count+1)*lttr_size)
#     hdwn_img = np.zeros(shape=(lttr_size, shape[1]), dtype=np.uint8)
#     for line in lines :
#         letter_img = np.zeros(shape=(lttr_size, lttr_size), dtype=np.uint8)
#         for letter in line :
#             letter_img = np.concatenate((letter_img, letter_table[letter.upper()]), axis=1)
#             # cv2.imshow('temp', letter_img)
#             # cv2.waitKey(500)
#             # cv2.destroyAllWindows()
#         for i in range(max_char_count-len(line)) :
#             letter_img = np.concatenate((letter_img, letter_table[' ']), axis=1)
#         hdwn_img = np.concatenate((hdwn_img, letter_img))
#         # cv2.imshow('temp', hdwn_img)
#         # cv2.waitKey(1000)
#         # cv2.destroyAllWindows()

#     hdwn_img =  hdwn_img[lttr_size:,lttr_size:]
#     print(hdwn_img.shape)

#     if tgt_typ in ['png', 'jpg', 'svg'] :
#         with open(f"{output}.pkl", 'wb') as f :
#             pickle.dump(hdwn_img, f)
#         hdwn_img = hdwn_img.astype(np.uint8)
#         imageio.imwrite(f"{output}.{tgt_typ}", hdwn_img)
#         # plt.imsave(f"{output}.{tgt_typ}", hdwn_img)

#     # cv2.imshow('temp', hdwn_img)
#     # cv2.waitKey(10000)
#     # cv2.destroyAllWindows()

#     return hdwn_img.shape