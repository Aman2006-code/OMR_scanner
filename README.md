# OMR Scanner

OMR Scanner project was my attempt to learn openCV through pratcial work done on scanning an OMR answer sheet to retrive answers marked on a standard OMR Sheet (provided in this repo).
This takes in a properly scanned standard OMR sheet cleans the image pre process it and maps answers with given correct answers.

## The Problem
OMR processing still remains the central problem from small scale to large nation wide exam scale. With the curiousity of finding out how an OMR is actually scanned and the objective to understand 
computer vision I decided to built this basic OMR Scanner.

## How it works?
The repository requires you to save the scanned answer sheet in the same folder with name 'test_1.jpeg'.
The program reads this image and does pre processing on it by converting it into grayscale provide enough blur applying otsu thresholding to convert into a binary image
and use kerneling to remove false positives.
Then the opencv tool is employed to find the contour shapes its edges and its other data (perimeter,area,cover etc).
Since the standard OMR sheet is having a discontinous strip of contours on left margin this sheet is identified as the most continous vertical contour strip.
The bottom of the strip is parellel to identifiers on OMR - which are 4 markings parellel to Section A option - a,c,d and Section B option - d.
This information functions as inputs to find distance between any two options and distance between two sections.
This identifier strip also acts as the lower horizontal margin.
The discontinous vertical strip are discontinous at the same distance as that of the vertical distance between two continous. For accuracy the median distance 
of vertical strip break is took as vertical distance of question.
Half way of the vertical strip acts as the top horizontal margin of the answer region.
Hence the Answer region is cropped out from the OMR sheet with option distance section distance vertical distance and hence position of each options.
Now from the contour data extracted earlier after eliminating false positive using cover, perimeter and area data answers are identified.
This is done by mapping option/section distance with contour data.
Then by mapping section dist with contour data the identified answers are mapped to their respective question numbers.

## Structure
All the functions are stored in utills.py for better reading of omr.py

## How It Works


## Usage

## 0. Pre-Requisites
After forking the repo get a python virtual enviornment and install the pre requisites by running:
```bash
pip install -r requirements.txt
```

### 1. Execution

Run the script in your terminal environment. It will prompt you to enter the actual answers for your questions and will check with the student response.

