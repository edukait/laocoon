<p align="center">
  <img width="100%" src="images/header.png"/>
</p>

## Introduction
Inspired by the seer from ancient Greek/Roman mythology, Laocoön, this package
synthesizes different packages and methods available in the field of computer
vision to create an automatic and efficient means of counting the number of cells
in fluorescently stained Fucci cells.
### What are Fucci cells?
To put it briefly, Fucci cells are stained with certain fluorescent proteins where
a certain color corresponds with a certain part of the cell cycle. Comparing the
proportion of cells in one part of the cell cycle to another part of the cell cycle
can prove to be useful for clinical applications and can serve as an initial quantitative
look at potentially diseased cells.
### Why do we care?
The only way that we can get these quantitative analyses is by actually counting the cells.
There can be a lot (and I mean a _lot_) of cells in a given image. Though there are existing
methods of automatic cell counting, these functionalities are restricted to plugins only
available in [ImageJ](https://imagej.nih.gov/ij/), a Java-based image processing program
developed by the National Institute of Health. However, these methods are not used mainly because
they require tedious amounts of user input and are neither accurate nor efficient enough for
regular use (no shade).`laocoon` serves to address this problem by providing researchers
with a newer means of counting cells without staring at a screen for hours on end.

## Features
* Histogram equalization and counting the connected components.
* Gaussian filters and counting the regional maxima.
* Optional additions for quality control.

## Usage
### Import
To download `laocoon`, you can either fork this repository or use PyPi via `pip`.
```
pip install laocoon
```
You must have `mahotas`, `numpy`, and `pandas` installed.
### Execution
Input the path to the folder containing your images, as well as the filetype of
your images (acceptable image types are PNG, JPEG, JPG, and TIF). Each image must have
four different channels: DAPI, EdU, RFP, and GFP in the folder, and all similar images must
have the same prefix. Here's an example of how to execute the code:
```
python gausreg.py /Users/name/Documents/fucci_images tif
```
You also have the option of implementing the quality control features:
the epsilon value, as well as the boolean array (read the paper for more information on
these features). The default `gausreg.py` does not implement any form of quality control.
`gausreg_eps.py` implements the epsilon value, `gausreg_bool.py` implements the boolean array,
and `gausreg_both.py` implements both. These files are executed in the same manner on a command
terminal as demonstrated above:
```
python gausreg_eps.py /Users/name/Documents/fucci_images tif
python gausreg_bool.py /Users/name/Documents/fucci_images tif
python gausreg_both.py /Users/name/Documents/fucci_images tif
```
All files will be saved with a .csv extension in the same directory as `fucci_images`.
The files will also contain calculations of proportions of cells in certain parts of
the cell cycle, as well as the original counts from the different image channels.

## Concerns? Questions? Suggestions?
This package is far from perfect! If you have any questions, comments, or suggestions, or
if you're interested in contributing, please contact me at kaitlin.y.lim@gmail.com.
Response times may vary!
