
from __future__ import print_function
from __future__ import division

import numpy as np  
import h5py  
import os, sys, traceback
import cv2
import pickle

def group(iterator, count):
    itr = iter(iterator)
    while True:
        yield tuple([next(itr) for i in range(count)])

class DatasetLoader():
    def __init__(self, data_path):
        # generate data path
        self.data_path = data_path
        self.image_path = os.path.join(data_path, 'bg_img')
        image_name_file = os.path.join(data_path, 'imnames.cp')
        seg_file = os.path.join(data_path, 'seg.h5')
        depth_file = os.path.join(data_path, 'depth.h5')
        
        # open h5 files
        self.seg = h5py.File(seg_file, 'r')['mask']
        self.depth = h5py.File(depth_file, 'r')

        # load file names
        self.filenames = []
        with open(image_name_file) as namefile:
            for i, file in group(namefile, 2):
                i = int(i[i.find('p')+1:-1])
                vindex = file.find('V')
                if -1 == vindex:
                    break
                file = file[vindex+1:-1]
                if file in self.seg:
                    self.filenames.append(file)


    def load(self, filename):
        # load depth
        depth = self.depth[filename][:].T
        depth = depth[:,:,1]
        sz = depth.shape[:2][::-1]

        # load image
        img = cv2.imread(os.path.join(self.image_path, filename))
        img = cv2.resize(img, sz)

        # load segmentation
        seg = self.seg[filename][:]
        seg_max = np.max(seg)
        label = np.array(range(1, seg_max+1), dtype=np.int)
        area = np.array(range(1, seg_max+1), dtype=np.int)
        for i in label:
            area[i-1] = int(np.sum(seg == i))
        seg = seg.astype('float32')
        seg = cv2.resize(seg, sz, interpolation=cv2.INTER_NEAREST)

        return img, depth, seg, area, label

if __name__ == '__main__':
    loader = DatasetLoader('/home/zwj/SynthTextData')
    filename = loader.filenames[333]
    data = loader.load(filename)
    with open('dump.pkl', 'wbd') as f:
        pickle.dump(data, f)
