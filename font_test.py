
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import os
import argparse
import pygame
import pygame
import cv2
import traceback

import numpy as np
from pygame import Color
from pygame.freetype import Font

RENDER_TEXT = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789`-=~!@#$%^&*()_+[]\\{}|;':\",./<>?"

def main():
    parser = argparse.ArgumentParser(description='test font')
    parser.add_argument('-f', '--font_dir', type=str, required=True)
    parser.add_argument('-o', '--output_dir', type=str, required=True)
    args = parser.parse_args()

    files = filter(
        (lambda x: x.lower().endswith('.ttf')),
        os.listdir(args.font_dir))

    pygame.init()

    for file in files:
        try:
            font = Font(os.path.join(args.font_dir, file), size=24)
            font.strong = True
            font.oblique = True
            font.antialiased = True
            font.origin = True
            font.strength = 0.01
            surface, _ = font.render(
                RENDER_TEXT,
                fgcolor=Color(255, 255, 255, 255),
                bgcolor=Color(0, 0, 0, 0))
            img = pygame.surfarray.array3d(surface)
            img = np.transpose(img, [1, 0, 2])
            # print(img.shape)
            # cv2.imshow('test', img)
            # cv2.waitKey()
            cv2.imwrite(os.path.join(args.output_dir, file+".png"), img)
            # print(file, img.shape)
        except Exception:
            print(file, "Exception")
            # traceback.print_exc()

if __name__ == '__main__':
    main()
