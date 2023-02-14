import os
import dlib
import cv2
import numpy as np

# Create a face detector and predictor using dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Load the target image of the person you want to find
target_image = cv2.imread("target_image.jpg")

# Get the face landmarks of the target image
target_faces = detector(target_image)
if len(target_faces) != 1:
    raise Exception("Target image should contain exactly one face")

target_landmarks = predictor(target_image, target_faces[0]).parts()
target_points = np.array([[p.x, p.y] for p in target_landmarks])


# Define a function to search for photos recursively
def search_for_photos(directory):
    # Loop through the contents of the directory
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)

        # If the path is a directory, search it recursively
        if os.path.isdir(path):
            search_for_photos(path)

        # If the path is a photo, try to find the target face in it
        elif (
            filename.endswith(".jpg")
            or filename.endswith(".jpeg")
            or filename.endswith(".png")
        ):
            current_photo = cv2.imread(path)
            current_faces = detector(current_photo)

            for face in current_faces:
                
                current_landmarks = predictor(current_photo, face).parts()
                current_points = np.array([[p.x, p.y] for p in current_landmarks])
                distance = np.linalg.norm(target_points - current_points)
                
                if distance < threshold:
                    print("Found a match in {}".format(path))


# Set the threshold for the face recognition
threshold = 0.6

# Start the search in the root directory
root_directory = "../../Downloads/test_album"
search_for_photos(root_directory)
