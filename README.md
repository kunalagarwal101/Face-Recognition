# Face-Recognition
Face Recognition model developed using the dlib library. For an unknown image as an input, 
the model outputs the image with the face recognized with the name of the person in the image along with a similarity coefficient.

The model is developed in the python language.

## Acknowledgement:
- @davisking for the dlib library
- @ageitgey for the face_recognition library

## Input:
- directory path for the known images
- path of the unknown images that are to be recognized

## Output:
- a folder is created in the current working directory which contains all the unknown images 
  and the images are marked with the either the name of the face recognized or Unknown with a similarity cofficient.
  value for the coffiecint will be 1.0 for identical images.
  
## Dependencies:
- dlib
- face_recognition
- numpy
- openCV (cv2)
- os

## Used two pre-trained model from the dlib library for fetching the face encodings for all the faces in the images (if any).

The pre-trained models can be downloaded from the links below:
- http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
  This gives us the face encodings (numbers that identify the face of a particular person)
  This model is a ResNet network with 29 conv layers. It's essentially a version of the ResNet-34 network from the paper Deep Residual Learning 
  for Image Recognition by He, Zhang, Ren, and Sun with a few layers removed and the number of filters per layer reduced by half.

- http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
  This allows us to detect landmark points in faces and understand the pose/angle of the face. This is a 68 point landmarking model
  It takes in an image region containing some object and outputs a set of point locations that define the pose of the object.

Alternative for above two model is using the face_recognition library module "face_recognition.get_encoding(face_image, known_face_locations=None, num_jitters=1, model='small')"

##
In the later part, I have the known face encoding with unknown one and got a euclidean distance for each comparison face. 
The distance tells you how similar the faces are. using this the similarity coefficient is deterined and displaced the output image.

Using openCV, a rectangle is enclosed around the face and name or unknown is mentioned at top of the rectangle in the image with the similarity coefficient.
