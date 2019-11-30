import os
import argparse
import pickle

import pygame, pygame.locals
from pygame import freetype
import numpy as np

def clean_fonts(font_dir, fonts):
    pygame.init()
    newfontlist = []
    ys = np.arange(8,200).astype(np.float)
    A = np.c_[ys,np.ones_like(ys)]
    models = {}
    for fontname in fonts:
        font = freetype.Font('{}/{}'.format(font_dir, fontname), size=12)
        h = []
        for y in ys:
            h.append(font.get_sized_glyph_height(y))
        h = np.array(h)
        m,_,_,_ = np.linalg.lstsq(A,h)
        models[font.name] = m
        rect = font.get_rect('O')
        if rect.width:
            newfontlist.append(fontname)
    font_model = models
    print('Total: {}, filtered: {}, saved: {}'.format(len(fonts), len(fonts) - len(newfontlist), len(newfontlist)))
    return font_model, newfontlist


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--font_dir', type=str)
    parser.add_argument('--data_dir', type=str)
    args = parser.parse_args()
    font_dir = args.font_dir
    data_dir = args.data_dir
    with open('{}/{}'.format(font_dir, 'fontlist.txt'), 'r') as infile:
        font_list = []
        while True:
            line = infile.readline().strip()
            if not line:
                break
            font_list.append(line)
    for filename in os.listdir('{}/{}'.format(font_dir, 'newfonts')):
        if filename.endswith('.ttf'):
            font_list.append('{}/{}'.format('newfonts', filename))
    font_model, font_list = clean_fonts(font_dir, font_list)
    with open('{}/{}'.format(font_dir, 'fontlist.txt'), 'w') as infile:
        for filename in font_list:
            infile.write(filename+'\n')
    with open(os.path.join(data_dir, 'models/font_px2pt.cp'), 'wb') as outfile:
        pickle.dump(font_model, outfile)
