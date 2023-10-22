'''
Name: Amanda Lin and Jue Gong
Program: Image Artist
Purpose: To allow a client to promote their clothing (specifically, traditional hanfu) 
by demonstrating how they look on different people. This program will paste an image
of an dress on a person. The client can select parameters for which model and which dress
is used. 
'''

from fileinput import filename
from select import select
from mtcnn import MTCNN 
import numpy as np
import os, sys, PIL
import matplotlib.pyplot as plt

def user_input():
    """
    Prompts user to input parameters for outfit and model

    Outfit must be an integer between 1 and 10, Model must be an integer between 1 and 5
    
    Each number is associated with a different outfit/model

    Returns a list  with the user-inputted outfit (int), model number (int), and file name (str)
    """

    print("你好! 欢迎来到虚拟汉服试衣间!")
    print("Hello and welcome to our virtual fitting room! Using this program, you will be able to see how a variety of outfits look on different models.")
    
    # prompts user for integer input for outfit choice
    # checks to make sure that the input is between 1 and 10
    # uses try-except to ensure that the program doesn't crash if the user inputs a non-integer
    try:
        outfit = int(input("Select an outfit by entering an integer 1-10: "))
        while outfit not in range(1,11):
            outfit = int(input("Please enter an integer 1-10: "))
    except:
        outfit = int(input("Please enter an integer 1-10: "))
        while outfit not in range(1,11):
            outfit = int(input("Please enter an integer 1-10: "))

    try:
        model = int(input("Select an model by entering an integer 1-6: "))
        while model not in range(1,7):
            model = int(input("Please enter an integer 1-6: "))
    except:
        model = int(input("Please enter an integer 1-6: "))
        while model not in range(1,7):
            model = int(input("Please enter an integer 1-6: "))

    file_name = input("Please enter a file name that your image will be saved as: ")

    return [outfit, model, file_name]

def select_images (image_nums):
    """
    input should be a list of two integers in the form of [outfit, model]

    designed to work with the user_input function within the image_artist file

    output is a list of the image file for the dress, for the model, the filename for the dress, for the model
    
    """ 
    
    # dictionaries for the dresses and the models in order to associate user input with a specific file
    dress_dict = {
        1: "boy1.png",
        2: "boy2.png",
        3: "boy3.png",
        4: "girl1.png",
        5: "girl2.png",
        6: "girl3.png",
        7: "girl4.png",
        8: "girl5.png", 
        9: "unisex1.png",
        10: "unisex2.png",
    }

    model_dict = {
        1: "amanda.jpg",
        2: "jue.jpg",
        3: "stockphoto1.jpg",
        4: "stockphoto2.jpg",
        5: "michael.jpg",
        6: "egg.jpg", # the program is unable to detect a face with this image, which is kept for demonstration purposes
    }

    dress_num = image_nums[0]
    model_num = image_nums[1]

    # gets the filename and opens the images
    dress_filename = os.path.join("Dresses", dress_dict[dress_num])
    model_filename = os.path.join("People", model_dict[model_num])

    dress_img = plt.imread(dress_filename)
    model_img = plt.imread(model_filename)

    # returns the images and the filenames as a list
    images = [dress_img, model_img, dress_filename, model_filename]
    return images

def find_face(image):
    """
    finds the location of the face as jpg or png image

    original_image must be a jpg or png image

    Returns the bounding box of the face as a list of 4 2-tuples 
    (order of tuples: bottom left, bottom right, top right, top left)
    """

    # use MTCNN library to find and locate face, data returned as JSON 
    # The MTCNN library uses a CNN (machine learning) to determine the location of the face
    detector = MTCNN()
    face_data = detector.detect_faces(image)

    # extracts pertinent information from the data, which is in JSON format
    try:
        x_value = face_data[0]["box"][0]
        y_value = face_data[0]["box"][1]
        width = face_data[0]["box"][2]
        height = face_data[0]["box"][3]
    # If there is no face, an index error will occur (because there are no indices in the JSON)
    except IndexError:
        print("No face found!")
        sys.exit()

    # uses above data to create a list of tuples 
    # with the corners of the box containing the face
    face_box = [(x_value, y_value+height), (x_value+width, y_value+height),
                (x_value+width, y_value), (x_value, y_value)]

    return face_box

def put_on_dress(coordinates, dress_image, original_person_image):
    
    """

    This function uses the input and returns the final image with the dress and model.

    The coordinates should be a list of 4 2-tuples in the same format as what is returned from the find_face() function
    (ie the order of the tuples: bottom left, bottom right, top right, top left)

    The dress_image should be a PIL.Image of the dress that is to be put on the model

    The original_person_image should be a PIL.Image of the person that the dress is being put on.

    The function returns a PIL.Image with the dress pasted on the person.

    """

    # scale factors based on general body proportions
    # can be changed for specific body proportions 

    # the width of the dress image compared to the 
    
    shoulder_width_scale_factor = 2.5
    height_scale_factor = 6.5

    # calculates head width and head heights in pixels from head coordinates input 
    # (which, in combination with other code, are obtained by the neural networks)
    head_width = coordinates[1][0]-coordinates[0][0]
    # print(head_width) # prints for checking
    head_height = coordinates[0][1]-coordinates[3][1]
    # print(head_height) # prints for checking

    # estimate shoulder width and neck height based on head width and head height
    shoulder_width = 2.5*head_width
    neck_height = (head_height)/10

    # finding the center of the shoulder
    shoulder_center_coordinates = (coordinates[1][0]+coordinates[0][0])/2, coordinates[1][1]+neck_height
    shoulder_center_y_coordinate = shoulder_center_coordinates[1]
    # print(shoulder_center_coordinates) # prints for checking
    # print(shoulder_center_y_coordinate) # prints for checking

    # finding the location on the body where the dress is posted
    # with slight offset from the center of the shoulder to adjust for the size of the dress image
    # offset calculated based on shoulder width and shoulder_width_scale_factor
    paste_x_coordinate = shoulder_center_coordinates[0]-(shoulder_width*shoulder_width_scale_factor/2)
    # print(paste_x_coordinate) # prints for checking

    # location on the original person where the dress is pasted
    new_size = (int(paste_x_coordinate), int(shoulder_center_y_coordinate))

    original_dress_image_width = dress_image.size[0]
    original_dress_image_height = dress_image.size[1]

    # dress size and lengths estimation for the person with scale factors with respect to head size 
    # dress_length = head_height * height_scale_factor
    dress_width = shoulder_width*shoulder_width_scale_factor
    dress_size = (int(dress_width), int((dress_width/original_dress_image_width)* original_dress_image_height))
    # resizing the dress image to the size determined above 
    dress_image = dress_image.resize(dress_size)

    # creating an empty and transparent image as the backdrop
    result = PIL.Image.new('RGBA', original_person_image.size, (0,0,0,0))

    # pasting the original image of the person into the backdrop
    result.paste(original_person_image, (0,0))

    # pastes on the dress with dress as mask to eliminate transparency background problems
    result.paste(dress_image, new_size, dress_image)
    return result


def main():
    
    # runs the user_input function, which prompts user for parameters
    user_info = user_input()
    # print(user_info)

    # selects the images based on user data
    images = select_images(user_info)

    # finds the face location of the image of the person
    image_data = find_face(images[1])
    # print(image_data)

    img_person = PIL.Image.open(images[3])
    img_dress = PIL.Image.open(images[2])

    # pastes the dress onto the person
    person_with_dress = put_on_dress(image_data, img_dress, img_person)

    # saves the image
    new_image_filename = os.path.join("Results", user_info[2] + '.png')
    person_with_dress.save(new_image_filename)

    # prints a goodbye statement
    print("Thank you for visiting our virtual fitting room!")

if __name__ == "__main__":
    main()

