import csv
import datetime
import os
import time

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageTk


# # Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message,text_to_speech):
    """
    Train the face recognition model using images stored in trainimage_path.
    """
    try:
        print(f"Starting image training with:")
        print(f"- Haarcascade path: {haarcasecade_path}")
        print(f"- Training image path: {trainimage_path}")
        print(f"- Training label path: {trainimagelabel_path}")
        
        # Check if haarcascade file exists
        if not os.path.exists(haarcasecade_path):
            error_msg = f"Haarcascade file not found: {haarcasecade_path}"
            print(error_msg)
            message.configure(text=error_msg)
            text_to_speech(error_msg)
            return
            
        # Check if training directory exists
        if not os.path.exists(trainimage_path):
            error_msg = f"Training directory not found: {trainimage_path}"
            print(error_msg)
            message.configure(text=error_msg)
            text_to_speech(error_msg)
            return
            
        # Create recognizer and detector
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)
        
        # Get faces and IDs
        faces, Ids = getImagesAndLables(trainimage_path)
        
        if not faces or not Ids:
            error_msg = "No valid images found for training!"
            print(error_msg)
            message.configure(text=error_msg)
            text_to_speech(error_msg)
            return
            
        # Train the recognizer
        print(f"Training recognizer with {len(faces)} images...")
        recognizer.train(faces, np.array(Ids))
        
        # Save the trained model
        print(f"Saving trained model to {trainimagelabel_path}...")
        recognizer.save(trainimagelabel_path)
        
        # Success message
        success_msg = f"Image Training Successful! Processed {len(faces)} images."
        print(success_msg)
        message.configure(text=success_msg)
        text_to_speech(success_msg)
        
    except Exception as e:
        error_msg = f"Error during training: {str(e)}"
        print(error_msg)
        message.configure(text=error_msg)
        text_to_speech(error_msg)


# def getImagesAndLables(path):
#     # imagePath = [os.path.join(path, f) for d in os.listdir(path) for f in d]
#     newdir = [os.path.join(path, d) for d in os.listdir(path)]
#     imagePath = [
#         os.path.join(newdir[i], f)
#         for i in range(len(newdir))
#         for f in os.listdir(newdir[i])
#     ]
#     faces = []
#     Ids = []
#     for imagePath in imagePath:
#         pilImage = Image.open(imagePath).convert("L")
#         imageNp = np.array(pilImage, "uint8")
#         Id = int(os.path.split(imagePath)[-1].split("_")[1])
#         faces.append(imageNp)
#         Ids.append(Id)
#     return faces, Ids





# import os

# import cv2
# import numpy as np
# from PIL import Image

# def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
#     """
#     Train the face recognition model using images stored in trainimage_path.
#     """
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     detector = cv2.CascadeClassifier(haarcasecade_path)
    
#     faces, Ids = getImagesAndLables(trainimage_path)

#     if not faces or not Ids:
#         res = "No images found for training!"
#         message.configure(text=res)
#         text_to_speech(res)
#         return
    
#     recognizer.train(faces, np.array(Ids))
#     recognizer.save(trainimagelabel_path)
    
#     res = "Image Training Successful!"
#     message.configure(text=res)
#     text_to_speech(res)


def getImagesAndLables(path):
    """
    Retrieve images and corresponding labels from the training directory.
    """
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist!")
        return [], []

    # Get only subdirectories inside `TrainingImage`
    newdir = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    faces = []
    Ids = []

    for folder in newdir:
        for filename in os.listdir(folder):
            img_path = os.path.join(folder, filename)

            try:
                # Convert image to grayscale
                pilImage = Image.open(img_path).convert("L")
                imageNp = np.array(pilImage, "uint8")

                # Extract ID from filename (format: Name_ID_XX.jpg)
                # For example: Simi_26_50.jpg -> ID is 26
                filename_parts = os.path.basename(img_path).split("_")
                if len(filename_parts) >= 2:
                    Id = int(filename_parts[1])
                else:
                    print(f"Invalid filename format: {img_path}")
                    continue

                faces.append(imageNp)
                Ids.append(Id)
                print(f"Processed image: {img_path} with ID: {Id}")

            except Exception as e:
                print(f"Skipping invalid file: {img_path} | Error: {e}")

    print(f"Total images processed: {len(faces)}")
    return faces, Ids
