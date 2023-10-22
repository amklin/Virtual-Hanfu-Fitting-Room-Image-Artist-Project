'''
Name: Amanda Lin and Jue Gong
Program: Image Artist
Purpose: Runs through all possible parameter selections in the image_artist file
'''

from fileinput import filename
from select import select
from mtcnn import MTCNN 
import numpy as np
import os, sys, PIL
import matplotlib.pyplot as plt
import image_artist as ia

# iterates through dresses and models
for dress in range (1,11):
    for model in range (1,6):
        file_name = "para" + str(dress) + "_" + str(model)
        user_info = [dress, model, file_name]
        # print(user_info)

        # selects the images based on data previously provided
        images = ia.select_images(user_info)

        # finds the face location of the image of the person
        image_data = ia.find_face(images[1])
        # print(image_data)

        img_person = PIL.Image.open(images[3])
        img_dress = PIL.Image.open(images[2])

        # pastes the dress onto the person
        person_with_dress = ia.put_on_dress(image_data, img_dress, img_person)

        # saves the image
        new_image_filename = os.path.join("all_parameters", user_info[2] + '.png')
        person_with_dress.save(new_image_filename)

        print("done", dress, model)
        
print ("All iterations completed,")