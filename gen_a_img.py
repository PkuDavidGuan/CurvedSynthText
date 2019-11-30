
from __future__ import print_function

import pickle
import cv2
import numpy as np
import os
import argparse

from itertools import islice

fname = 'SynthTextData/results_bin2/4000_4100_0/2/4067_22.bin'
with open(fname, 'rb') as pklfile:
    pkl = pickle.load(pklfile, encoding='latin1')

img = pkl['img'].copy()

cnts = np.array(pkl['contour'][1], dtype=np.int32)
cnts = np.split(cnts, len(cnts), 0)
cnts = [x.transpose([1, 0, 2]) for x in cnts]
cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)

cnts = np.array(pkl['contour'][0], dtype=np.int32)
cnts = np.split(cnts, len(cnts), 0)
cnts = [x.transpose([1, 0, 2]) for x in cnts]
cv2.drawContours(img, cnts, -1, (0, 0, 255), 1)

cv2.imwrite('1_ori.png', pkl['img'])
cv2.imwrite('1.png', img)
