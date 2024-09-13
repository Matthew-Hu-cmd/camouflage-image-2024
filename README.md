# Camouflage Image

This project was developed in the discipline of Fundamentals of Image Processing.

The goal is to implement a basic version of the algorithm show in the paper [Camouflage Images](http://www.graphics.stanford.edu/~niloy/research/camouflage/camouflage_images_sig_10.html) presented at SIGGRAPH.

## Setup2024

```bash
conda create --name camouflage_env python=3.10.9
conda activate camouflage_env
pip install numpy==1.23.5
pip install opencv-python #4.10.0.84
```

## Execute

To execute, run the following, replacing the fields between `<>`:

```
python src/camouflage_image.py <BACKGROUND IMAGE PATH> <OVERLAY IMAGE PATH>
```

Working example:

要保证前景和背景的尺寸是一致的，更改了一些python2.7时代不兼容的接口，比如print
```
python src/camouflage_image.py assets/background/mountain.jpg assets/overlay/dog.png
```
