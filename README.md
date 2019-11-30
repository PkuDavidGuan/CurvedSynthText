# SynthText
Code for generating synthetic text images as described in ["Synthetic Data for Text Localisation in Natural Images", Ankush Gupta, Andrea Vedaldi, Andrew Zisserman, CVPR 2016](http://www.robots.ox.ac.uk/~vgg/data/scenetext/).


**Synthetic Scene-Text Image Samples**
![Synthetic Scene-Text Samples](samples.png "Synthetic Samples")

The library is written in Python. The main dependencies are:

```
pygame, opencv (cv2), PIL (Image), numpy, matplotlib, h5py, scipy
```

### Generating samples

```
source run_gen.sh
```

All parameters:
  - begin_index: the index of the first background image.
  - end_index: the index of the last background image.
  - max_time: the time limit to generate a image.
  - gen_data_path: the directory to store dset.h5, models, fonts and newsgroup.
  - bg_data_path: the directory to store imnames.cp,bg_img.tar.gz,depth.h5,seg.h5.
  - jobs: the number of process.
  - output_path: the absolute path to stored generated images.
  - instance_per_image: the number each background images used to genearte synthetic images.

### Convert binary files into images.

In the last step, only binary files are generated. To generate png files, you should run:

```
source to_image.sh
```

### Add new fonts.

Add new fonts to the generater, since the official project only provide three sample fonts. ** You should first add ttf files into {font_dir}/newfonts. **

```
source add_new_fonts.sh
```

All parameters:
  - font_dir: the directory to store fonts.
  - data_dir: the directory to store dset.h5, models, fonts and newsgroup. Same as the **gen_data_path**.

### Download links
**You must download these files before the generation.**

  1. [here](http://www.robots.ox.ac.uk/~ankush/data.tar.gz) This data file includes:

    - **dset.h5**: This is a sample h5 file which contains a set of 5 images along with their depth and segmentation information. Note, this is just given as an example; you are encouraged to add more images (along with their depth and segmentation information) to this database for your own use.
    - **data/fonts**: three sample fonts (do not update fontlist.txt, just add ttf fonts to newfonts directory, see text_utils.py for detail information.).
    - **data/newsgroup**: Text-source (from the News Group dataset). This can be subsituted with any text file. Look inside `text_utils.py` to see how the text inside this file is used by the renderer.
    - **data/models/colors_new.cp**: Color-model (foreground/background text color model), learnt from the IIIT-5K word dataset.
    - **data/models**: Other cPickle files (**char\_freq.cp**: frequency of each character in the text dataset; **font\_px2pt.cp**: conversion from pt to px for various fonts).
  2. The 8,000 background images used in the paper, along with their segmentation and depth masks:
  `http://www.robots.ox.ac.uk/~vgg/data/scenetext/preproc/<filename>`, where, <filename> can be:
    - `imnames.cp` [180K]: names of filtered files, i.e., those files which do not contain text
    - `bg_img.tar.gz` [8.9G]: compressed image files (more than 8000, so only use the filtered ones in imnames.cp)
    - `depth.h5` [15G]: depth maps
    - `seg.h5` [6.9G]: segmentation maps

Note: I do not own the copyright to these images.

### Pre-generated Dataset
A dataset with approximately 800000 synthetic scene-text images generated with this code can be found [here](http://www.robots.ox.ac.uk/~vgg/data/scenetext/).

### Adding New Images
Segmentation and depth-maps are required to use new images as background. Sample scripts for obtaining these are available [here](https://github.com/ankush-me/SynthText/tree/master/prep_scripts).

* `predict_depth.m` MATLAB script to regress a depth mask for a given RGB image; uses the network of [Liu etal.](https://bitbucket.org/fayao/dcnf-fcsp/) However, more recent works (e.g., [this](https://github.com/iro-cp/FCRN-DepthPrediction)) might give better results.
* `run_ucm.m` and `floodFill.py` for getting segmentation masks using [gPb-UCM](https://github.com/jponttuset/mcg).

For an explanation of the fields in `dset.h5` (e.g.: `seg`,`area`,`label`), please check this [comment](https://github.com/ankush-me/SynthText/issues/5#issuecomment-274490044).

### Generating Samples with Text in non-Latin (English) Scripts
@JarveeLee has modified the pipeline for generating samples with Chinese text [here](https://github.com/JarveeLee/SynthText_Chinese_version).

### Further Information
Please refer to the paper for more information, or contact me (email address in the paper).

