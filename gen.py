
from __future__ import print_function
from __future__ import division

import argparse
import h5py
import os
import time
import pickle
import math
import errno

import numpy as np

from synthgen import RendererV3
from load_dataset import DatasetLoader
from multiprocessing import Process
from itertools import chain

def mkdir_if_missing(dir_path):
    try:
        os.makedirs(dir_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def main():
    parser = argparse.ArgumentParser(description='synthtext generator')
    parser.add_argument('--begin_index', type=int)
    parser.add_argument('--end_index', type=int)
    parser.add_argument('--max_time', type=int, default=10)
    parser.add_argument('--gen_data_path', type=str)
    parser.add_argument('--bg_data_path', type=str)
    parser.add_argument('--instance_per_image', type=int, default=1)
    parser.add_argument('--output_path', type=str)
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--files_per_dir', type=int, default=1000)
    args = parser.parse_args()

    loader = DatasetLoader(args.bg_data_path)
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    def run_child(begin, end, job_no):
        print("Process {}-{}".format(begin, end))
        RV3 = RendererV3(args.gen_data_path, max_time=args.max_time)
        count = 0
        failed = []
        for i in range(begin, end):
            try:
                t0 = time.time()
                filename = loader.filenames[i]
                img, depth, seg, area, label = loader.load(filename)
                res = RV3.render_text(img, depth, seg, area, label, ninstance=args.instance_per_image, viz=False)
                for j, instance in enumerate(res):
                    data_instance = {
                        'img_name': filename,
                        'img': instance['img'],
                        'contour': [
                            np.array(instance['charBB'], dtype=np.float).transpose([2, 1, 0]),
                            np.array(instance['wordBB'], dtype=np.float).transpose([2, 1, 0])
                        ],
                        'is_text_cnts': False,
                        'chars': [list(y) for y in (chain(*(x.split() for x in instance['txt'])))]
                    }
                    output_path = '{}/{}_{}_{}/{}'.format(args.output_path, begin, end, job_no, count // args.files_per_dir)
                    mkdir_if_missing(output_path)
                    with open(os.path.join(output_path, '{}_{}.bin'.format(i, j)), 'wb') as f:
                        pickle.dump(data_instance, f)
                    count += 1
                print("generated: {:08} time:{:.04}".format(i, time.time()-t0))
            except Exception:
                print("generated: {:08} Exception".format(i))
                failed.append(i)
        # Second chances for the failed generation.
        for i in failed:
            try:
                t0 = time.time()
                filename = loader.filenames[i]
                img, depth, seg, area, label = loader.load(filename)
                res = RV3.render_text(img, depth, seg, area, label, ninstance=args.instance_per_image, viz=False)
                for j, instance in enumerate(res):
                    data_instance = {
                        'img_name': filename,
                        'img': instance['img'],
                        'contour': [
                            np.array(instance['charBB'], dtype=np.float).transpose([2, 1, 0]),
                            np.array(instance['wordBB'], dtype=np.float).transpose([2, 1, 0])
                        ],
                        'is_text_cnts': False,
                        'chars': [list(y) for y in (chain(*(x.split() for x in instance['txt'])))]
                    }
                    output_path = '{}/{}_{}_{}/{}'.format(args.output_path, begin, end, job_no, count // args.files_per_dir)
                    mkdir_if_missing(output_path)
                    with open(os.path.join(output_path, '{}_{}.bin'.format(i, j)), 'wb') as f:
                        pickle.dump(data_instance, f)
                    count += 1
                print("generated: {:08} time:{:.04}".format(i, time.time()-t0))
            except Exception:
                print("generated: {:08} Exception".format(i))

    processes = []

    b = args.begin_index
    e = args.end_index
    t = int(math.ceil((e-b) / args.jobs))

    for i in range(args.jobs):
        p = Process(target=run_child, args=(b+i*t, min(b+t+i*t, e), i))
        p.daemon = True
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
