# OSSP
## Open Source Sea-ice Processing
### Open Source Algorithm for Detecting Sea Ice Surface Features in High Resolution Optical Imagery

### Initial Developer: Nicholas Wright and Chris Polashenski
### Secondary Developer: Dexuan Sha

## Introduction

Welcome to OSSP; a set of tools for detecting surface features in high resolution optical imagery of sea ice. The primary focus is on the detection of and differentiation between open water, melt ponds, and snow/ice. 

For this version, the training dataset is specifically labelled based on Arctic DMS Sea Ice Imagery during Spring Season, classification schema is combined with thick ice, thin ice, shadow feature and open water. Melt ponds mainly present among summer melting season, and more features related to weather and illumination condition will be developed in the next step.  

The Anaconda distribution of Python is recommended, but any distribution with the appropriate packages will work. You can download Anaconda for Linux and Windows environment, version 3.6 (3.7, 3.8), here: https://www.continuum.io/downloads


## Dependencies

* gdal (v2.0 or above)
* numpy
* scipy
* h5py
* scikit-image
* sklearn
* matplotlib
* tkinter
```bash
conda install -y gdal numpy h5py scikit-learn scikit-image matplotlib cython
```
gdal package installation is not stable for all enviroment. If you are working on windows, we highly suggest you to use pre-compiled .whl file to install directly. For example, download the GDAL-3.0.2-cp37-cp37m-win_amd64.whl (http://pypi.naturalcapitalproject.org/simple/gdal/index.html) and type `pip install GDAL-3.0.2-cp37-cp37m-win_amd64.whl` for GDAL installation. Otherwise a VS software is required for compile in local environment.

#### Optional
* tqdm (for progress bar)
* PGC imagery_utils (for WV pansharpening) (https://github.com/PolarGeospatialCenter/imagery_utils)

## Usage

For detailed usage and installation instructions, see the pdf document 'Algorithm_Instructions.pdf'

### setup.py

The first step is to run the setup.py script to compile C libraries. Run `python setup.py build_ext --build-lib .` from the OSSP directory. Be sure to include the period after `--build-lib. `

### ossp_process.py

This combines all steps of the image classification scheme into one script and should be the only script to call directly. If given a folder of images, this script finds all appropriately formatted files directory (.tif(f)) and queues them for processing. If given an image file, this script processes that single image alone. This script processes images as follows: Image preprocessing (histogram stretch or pansharpening if chosen) -> segmentation (segment.py) -> classification (classify.py) -> calculate statistics. Output results are saved as a geotiff with the same georeference of the input image. 

#### Required Arguments
* __input directory__: directory containing all of the images you wish to process. Note that all .jpg and .tif images in the input directory as well as all sub-directories of it will be processed. Can also provide the path and filename to a single image to process only that image.
* __image type__: {‘srgb’, ‘wv02_ms’, ‘pan'}: the type of imagery you are processing. 
  1. 'srgb': RGB imagery taken by a typical camera
  2. 'wv02_ms': DigitalGlobe WorldView 2 multispectral imagery
  3. 'pan': High resolution panchromatic imagery
* __training dataset file__: filepath of the training dataset you wish to use to analyze the input imagery

#### Optional Arguments

* __-o | --output_dir__: Directory to write output files. 
* __-v | --verbose__: Display text output as algorithm progresses. 
* __-c | --stretch__: {'hist', 'pansh', 'none'}: Apply an image correction prior to classification. Pansharpening / orthorectification option requires PGC scripts. *Default = hist*.
* __-t | --threads__: Number of subprocesses to spawn for classification. Threads > 2 is only utilized for images larger than ~10,000x10,000 pixels. 
* __--pgc_script__: Path for the PGC imagery_utils folder if 'pansh' was chosen for the image correction.
* __--training\_label__: The label of a custom training dataset. See advanced section for details. *Default = image\_type*.

#### Notes:

Example: `ossp\_process.py input\_dir im\_type training\_dataset\_file -v`

This example will process all .tif and .jpg files in the input\_dir.


### training_gui.py

Graphical user interface for creating a custom training dataset. Provide a directory of images that you wish to use as the basis of your training set. The GUI will present a random segment each time a classification is assigned. The display images can also be clicked classify a specific area. The segments themselves are automatically generated. The highlighted region corresponds to the segment that will be labeled.

Output is a .h5 file that can be provided to ossp\_process.py.

Note: Images are segmented prior to display on the GUI, and as such may take up to a minute to load (depending on image size and computer specs)

#### Positional Arguments:
* __input__: A directory containing the images you wish to use for training.
* __image type__: {‘srgb’, ‘wv02_ms’, ‘pan'}: the type of imagery you are processing. 
  1. 'srgb': RGB imagery taken by a typical camera
  2. 'wv02_ms': DigitalGlobe WorldView 2 multispectral imagery,
  3. 'pan': High resolution panchromatic imagery

#### Optional arguments:
* __--tds_file__: Existing training dataset file. Will create a new one with this name if none exists. If a path is not provided, file is created in the image directory.  *Default = <image_type>\_training\_data.h5*.
* __--username__: A specific label to attach to the training set. The --training\_label argument of ossp_\process references this value. *Default = <image\_type>*

For Example,
`python input\_dir\training_gui.py training\_image\_dir im\_type`