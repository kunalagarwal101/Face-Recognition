# -*- coding: utf-8 -*-
"""facerecognition_dlib.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TgwyzU48mYAldIVtv-WhJtT0P6I4WM1u
"""

import dlib
import scipy.misc
from imageio import imread
import numpy as np
import os

!pip install face_recognition
import face_recognition

# Get Face Detector from dlib
# This allows us to detect faces in images
face_detector = dlib.get_frontal_face_detector()

# mounting the google drive with the file to load data in google colab

from google.colab import drive
drive.mount('/content/drive')

# Get Pose Predictor from dlib
# This allows us to detect landmark points in faces and understand the pose/angle of the face

# This is a 68 point landmarking model
# This object is a tool that takes in an image region containing some object and outputs a set of point locations that define the pose of the object. 
# The classic example of this is human face pose prediction, where you take an image of a human face as input 
# and are expected to identify the locations of important facial landmarks such as the corners of the mouth and eyes, tip of the nose, and so forth. 

shape_predictor = dlib.shape_predictor('/content/drive/My Drive/Colab Notebooks/face_recognition_dlibmodel/shape_predictor_68_face_landmarks (2).dat')

# Get the face recognition model
# This is what gives us the face encodings (numbers that identify the face of a particular person)

# This model is a ResNet network with 29 conv layers. It's essentially a version of the ResNet-34 network from the paper Deep Residual 
# Learning for Image Recognition by He, Zhang, Ren, and Sun with a few layers removed and the number of filters per layer reduced by half.

face_recognition_model = dlib.face_recognition_model_v1('/content/drive/My Drive/Colab Notebooks/face_recognition_dlibmodel/dlib_face_recognition_resnet_model_v1 (1).dat')

# This is the tolerance for face comparisons
# The lower the number - the stricter the comparison
# To avoid false matches, use lower value
# To avoid false negatives (i.e. faces of the same person doesn't match), use higher value
# 0.5-0.6 works well
TOLERANCE = 0.6

# This function will take an image and return its face encodings using the neural network

def get_face_encodings(path_to_image):
    # Load image using imageio
    image = imread(path_to_image)

    # Detect faces using the face detector
    # The 1 in the second argument indicates that we should upsample(increasing the size of the image) the image 1 time. 
    # This will make everything bigger and allow us to detect more faces.
    detected_faces = face_detector(image, 1)
    
    # Get pose/landmarks of those faces
    # Will be used as an input to the function that computes face encodings
    # This allows the neural network to be able to produce similar numbers for faces of the same people, regardless of camera angle and/or face positioning in the image
    shapes_faces = [shape_predictor(image, face) for face in detected_faces]
    
    # For every face detected, compute the face encodings
    # 1 is the num_jitters, the array will be shuffed approx this much times if >1 and then average is taken
    encodings=[np.array(face_recognition_model.compute_face_descriptor(image, face_pose, 1)) for face_pose in shapes_faces]

    return encodings

def box_image(img_loc,detection):
    """
    Input
    --------
    img_loc: str
        The path to the image we want to encode
    Output
    --------
    boxes: list of tuples
        The list of tuples of locations of faces found in the image.
        (top,right,bottom,left)
    """

    # Load image using imageio
    image = imread(path_to_image)

    # Detect faces
    # Gives (x,y) coordinates of faces in the image
    box = face_recognition.face_locations(image, model=detection)

    return box

# This function takes a list of known faces

def compare_face_encodings(known_faces, face):

    # Finds the difference between each known face and the given face (that we are comparing)
    # Calculate norm for the differences with each known face
    # Return an array with True/Face values based on whether or not a known face matched with the given face
    # A match occurs when the (norm) difference between a known face and the given face is less than or equal to the TOLERANCE value

    return face_recognition.compare_faces(known_faces,face,tolerance=0.5)

# this function will give the distance between the faces
# how similar are the faces

# Given a list of face encodings, compare them to a known face encoding and 
# get a euclidean distance for each comparison face. The distance tells you how similar the faces are.

# distance 0 means exact similar image

def get_face_distance(known_faces, face):

    #getting the numpy ndarray of the distance between the known faces and face to compare
    distance=face_recognition.face_distance(known_faces,face);

    return distance

# This function returns the name of the person whose image matches with the given face (or 'Not Found')
# known_faces is a list of face encodings
# names is a list of the names of people (in the same order as the face encodings - to match the name with an encoding)
# face is the face we are looking for (real time capture)

def find_match(known_faces, names, face):

    # Call compare_face_encodings to get a list of True/False values indicating whether or not there's a match
    matches = compare_face_encodings(known_faces, face)
    
    # Return the name of the first match
    count = 0
    for match in matches:
        if match:
            return names[count], count
        count += 1

    # Return not found if no match found
    return 'Not Found', -1

def show_output_image(img_loc,name,box,distance,index,num_test):
    """
    Outputs output image with employee details
    Input
    ------
    img_loc: str
        The path to the input image
    name: str
        name of the person detected in the unknown image
    box: list
        A list of tuples containing bounding box of faces
        (top,right,bottom,left)
    """
    import cv2

    #Looping over face in the image
    for (top,right,bottom,left) in box:
        #Draw bounding box over the face
        image = cv2.imread(img_loc)
        cv2.rectangle(image,(left,top),(right,bottom),(0,255,0),2)
        y = top - 15 if top - 15 > 15 else top + 15

        #Preparing what to write
        if index == -1:
            text = "Unknown face" + str(num_test)
        else:
            text = ''
            text += name +': similarity( '+ str(1-distance[index]) + ' )'

        #Writing to image
        cv2.putText(image,text,(left,y),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),2)

        #Showing image
        """
        cv2.imshow("Face Recognition Results", image)
        cv2.waitKey(0)
        """
        result_path='/content/drive/My Drive/Colab Notebooks/face_recognition_dlibmodel/result/'
        if os.path.exists(result_path) ==  False:
                os.mkdir(result_path)
        filename = result_path + name + '.jpg'
        # Using cv2.imwrite() method 
        # Saving the image 
        cv2.imwrite(filename, image)

# Get path to all the known images
# Filtering on .jpg extension - so this will only work with JPEG images ending with .jpg
images_path='/content/drive/My Drive/Colab Notebooks/face_recognition_dlibmodel/images'

image_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir(str(images_path)))

# Sort in alphabetical order
image_filenames = sorted(image_filenames)

# Get full paths to images (according to the sorted images names)
paths_to_images = [images_path +'/'+ x for x in image_filenames]

# List of face encodings we have
face_encodings = []

# Loop over images to get the encoding one by one
for path_to_image in paths_to_images:
    # Get face encodings from the image
    face_encodings_in_image = get_face_encodings(path_to_image)
    
    # Make sure there's exactly one face in the image
    if len(face_encodings_in_image) != 1:
        print("Please change image: " + path_to_image + " - it has " + str(len(face_encodings_in_image)) + " faces; it can only have one")
        exit()
    
    # Append the face encoding found in that image to the list of face encodings we have
    face_encodings.append(get_face_encodings(path_to_image)[0])

# Get path to all the test images
# Filtering on .jpg extension - so this will only work with JPEG images ending with .jpg

test_path='/content/drive/My Drive/Colab Notebooks/face_recognition_dlibmodel/test'

test_filenames = filter(lambda x: x.endswith('.jpg'), os.listdir(test_path))

# Get full paths to test images
paths_to_test_images = [test_path +'/' + x for x in test_filenames]

# Get list of names of people by eliminating the .JPG extension from image filenames
names = [x[:-4] for x in image_filenames]

num_test=1
# Iterate over test images to find match one by one
for path_to_image in paths_to_test_images:
    # Get face encodings from the test image
    face_encodings_in_image = get_face_encodings(path_to_image)
    
    # Make sure there's exactly one face in the image
    if len(face_encodings_in_image) != 1:
        print("Please change image: " + path_to_image + " - it has " + str(len(face_encodings_in_image)) + " faces; it can only have one")
        exit()
    
    box = box_image(path_to_image,"cnn")

    distance=get_face_distance(face_encodings,face_encodings_in_image[0])
    
    # Find match for the face encoding found in this test image
    name , index= find_match(face_encodings, names, face_encodings_in_image[0])
    
    show_output_image(path_to_image,name,box,distance,index,num_test)


    # Print the path of test image and the corresponding match
    print(path_to_image, name)

    num_test = num_test + 1
