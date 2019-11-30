
from __future__ import print_function

import pickle
import cv2
import numpy as np
import os
import argparse

from itertools import islice

def main():
    parser = argparse.ArgumentParser(description='convert pkl file to image to preview')
    parser.add_argument('--input_folder', type=str)
    parser.add_argument('--output_folder', type=str)
    parser.add_argument('--nimages', type=int)
    args = parser.parse_args()

    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    files = list(filter((lambda x: x.endswith('.bin')), os.listdir(args.input_folder)))

    for f in islice(files, args.nimages):
        try:
            fname = os.path.join(args.input_folder, f)
            with open(fname, 'rb') as pklfile:
                # pkl = pickle.load(pklfile, encoding='latin1')
                pkl = pickle.load(pklfile)

            img = pkl['img'].copy()

            cnts = np.array(pkl['contour'][1], dtype=np.int32)
            cnts = np.split(cnts, len(cnts), 0)
            cnts = [x.transpose([1, 0, 2]) for x in cnts]
            cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)

            cnts = np.array(pkl['contour'][0], dtype=np.int32)
            cnts = np.split(cnts, len(cnts), 0)
            cnts = [x.transpose([1, 0, 2]) for x in cnts]
            cv2.drawContours(img, cnts, -1, (0, 0, 255), 1)

            cv2.imwrite(os.path.join(args.output_folder, f+'_ori.png'), pkl['img'])
            cv2.imwrite(os.path.join(args.output_folder, f+'.png'), img)
            print('Processed:', f)
        except Exception:
            print('Exception:', f)

if __name__ == '__main__':
    main()
