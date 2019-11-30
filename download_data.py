import os

if __name__ == '__main__':
  url = 'http://www.robots.ox.ac.uk/~vgg/data/scenetext/preproc/'
  filename = ['imnames.cp', 'bg_img.tar.gz', 'depth.h5', 'seg.h5']
  bg_data_path = 'SynthTextData/'
  for fn in filename:
    os.system('axel -n 10 -o {} {}'.format(bg_data_path, url+fn))
