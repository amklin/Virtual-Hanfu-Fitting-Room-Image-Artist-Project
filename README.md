# Virtual Hanfu Fitting Room: Image Artist Project

## Overview 

This is a project created as part of the Computer Science and Software Engineering course at High Technology High School (Junior Year). This a copy of a project from https://github.com/CSE-HighTechHighSchool/2022_Image6 (private repository). The final presentation for the project, which also includes results and analysis, can be found here: [presentation.pdf](https://github.com/amklin/Virtual-Hanfu-Fitting-Room-Image-Artist-Project/blob/06eebf1fe272e15ba5c4d3740293135c12f9d81a/presentation.pdf).

## Program Description

The program will prompt the user to select a model and dress style. Using a convolutional neural network, the program will locate the position of the model's face annd paste an image of a dress on a model, allowing the user to visualize what the dress would look like on a person. 

## Languages 

* Python

## How to Run

This can be run by downloading the project, installing Python along with the required Python packages listed in [requirements.txt](https://github.com/amklin/Virtual-Hanfu-Fitting-Room-Image-Artist-Project/blob/b3c7a9b07220778f43d49ab87c8b17789608d0e8/requirements.txt), and running the [image_artist.py](https://github.com/amklin/Virtual-Hanfu-Fitting-Room-Image-Artist-Project/blob/b3c7a9b07220778f43d49ab87c8b17789608d0e8/image_artist.py) file. The program will prompt the user to select the model and dress in the command line and save the final result in the Results folder.

## Contributors

This was a collaboration of a group of high school students. We worked together to brainstorm and develop the program, as well as testing all parts and creating the final presentation. In addition, each of us contributed the following individual components:

Amanda Lin (https://github.com/amklin)
* Implementing the convolutional neural network code in the find_face function
* Coding the user_input and select_images functions to allow the user to determine which models and outfits to pick

Jue Gong (https://github.com/happyjoyg)
* Finding images of dresses
* Coding the put_on_dress function (including calculating the body proportions based on face size)
