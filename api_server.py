import datetime
import logging
import os
import time

import cv2
import pandas as pd
from flask import Flask, jsonify, request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load your paths
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Attendance API'}), 200

@app.route('/attendance', methods=['POST'])
def fill_attendance():
    try:
        data = request.json
        subject = data.get('subject', 'Math')  # Default subject to "Math" if not provided
        if not subject:
            return jsonify({'error': 'Subject is required'}), 400

        # Check if webcam is available
        logger.info("Attempting to access webcam...")
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            logger.error("Could not open webcam")
            return jsonify({'error': 'Could not access webcam. Please check if it is connected and accessible.'}), 500

        # Test webcam by reading a frame
        ret, test_frame = cam.read()
        if not ret:
            logger.error("Could not read frame from webcam")
            cam.release()
            return jsonify({'error': 'Could not read from webcam. Please check if it is working properly.'}), 500

        logger.info("Webcam accessed successfully")

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainimagelabel_path)
        facecasCade = cv2.CascadeClassifier(haarcasecade_path)
        df = pd.read_csv(studentdetail_path)

        col_names = ["Enrollment", "Name"]
        attendance = pd.DataFrame(columns=col_names)

        end_time = time.time() + 15
        while time.time() < end_time:
            ret, im = cam.read()
            if not ret:
                logger.error("Failed to grab frame")
                continue
                
            try:
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if conf < 70:
                        name = df.loc[df['Enrollment'] == id]['Name'].values[0]
                        attendance.loc[len(attendance)] = [id, name]
                cv2.imshow('Attendance', im)
                if cv2.waitKey(1) == 27:
                    break
            except Exception as e:
                logger.error(f"Error processing frame: {str(e)}")
                continue

        cam.release()
        cv2.destroyAllWindows()

        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        Hour, Minute, Second = timeStamp.split(":")

        attendance[date] = 1
        attendance.drop_duplicates(['Enrollment'], keep='first', inplace=True)

        subject_folder = os.path.join(attendance_path, subject)
        os.makedirs(subject_folder, exist_ok=True)

        file_name = f"{subject}_{date}_{Hour}-{Minute}-{Second}.csv"
        file_path = os.path.join(subject_folder, file_name)
        attendance.to_csv(file_path, index=False)

        return jsonify({'message': f'Attendance filled for {subject}', 'file': file_name}), 200

    except Exception as e:
        logger.error(f"Error in fill_attendance: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
