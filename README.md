# Camouflage Image

This project was developed in the discipline of Fundamentals of Image Processing.

The goal is to implement a basic version of the algorithm show in the paper [Camouflage Images](http://www.graphics.stanford.edu/~niloy/research/camouflage/camouflage_images_sig_10.html) presented at SIGGRAPH.

## Setup

Python 2.7.*

`make setup` to install the dependencies.

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
