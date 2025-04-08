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
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Id = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Id))
    recognizer.save(trainimagelabel_path)
    res = "Image Trained successfully"  # +",".join(str(f) for f in Id)
    message.configure(text=res)
    text_to_speech(res)


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

                # Extract ID from filename (assuming format: ID_Name_XX.jpg)
                Id = int(os.path.split(img_path)[-1].split("_")[1])

                faces.append(imageNp)
                Ids.append(Id)

            except Exception as e:
                print(f"Skipping invalid file: {img_path} | Error: {e}")

    return faces, Ids
