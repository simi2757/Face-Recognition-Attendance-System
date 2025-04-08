import csv
import datetime
import os
import shutil
import time
import tkinter as tk
import tkinter.font as font
import tkinter.ttk as tkk
from tkinter import *

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageTk

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")
trainimage_path = "TrainingImage"
studentdetail_path = os.path.join("StudentDetails", "studentdetails.csv")
attendance_path = "Attendance"
# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    print(f"Number of faces detected: {len(faces)}")
                    face_detected = False  # Flag to track if any face was recognized
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        print(f"Face detected with confidence: {conf}")
                        if conf < 95:
                            print(f"Recognized face with ID: {Id}")
                            face_detected = True  # Set flag when face is recognized
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                if not face_detected:
                    f = "No Face found for attendance"
                    text_to_speech(f)
                    cv2.destroyAllWindows()
                    return

                print("Attendance data before saving:")
                print(attendance)
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                path = os.path.join(attendance_path, Subject)
                if not os.path.exists(path):
                    os.makedirs(path)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(f"Saving attendance to: {fileName}")
                print("Final attendance data:")
                print(attendance)
                
                if len(attendance) > 0:
                    attendance.to_csv(fileName, index=False)
                    m = "Attendance Filled Successfully of " + Subject
                else:
                    m = "No attendance data to save"
                
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)

                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="black")
                cs = os.path.join(path, fileName)
                print(cs)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:

                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)
            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    ###windo is frame for subject chooser
    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            path = os.path.join(attendance_path, sub)
            if os.path.exists(path):
                # Create a new window to display attendance records
                attendance_window = tkinter.Tk()
                attendance_window.title(f"Attendance Records - {sub}")
                attendance_window.geometry("800x600")
                attendance_window.configure(background="black")
                
                # Create a frame with scrollbar
                frame = tkinter.Frame(attendance_window, bg="black")
                frame.pack(fill=tkinter.BOTH, expand=True)
                
                # Create a canvas with scrollbar
                canvas = tkinter.Canvas(frame, bg="black")
                scrollbar = tkinter.Scrollbar(frame, orient="vertical", command=canvas.yview)
                scrollable_frame = tkinter.Frame(canvas, bg="black")
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Pack the scrollbar and canvas
                scrollbar.pack(side="right", fill="y")
                canvas.pack(side="left", fill="both", expand=True)
                
                # Get all CSV files in the subject directory
                csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
                csv_files.sort(reverse=True)  # Sort by name (newest first)
                
                if not csv_files:
                    label = tkinter.Label(
                        scrollable_frame,
                        text="No attendance records found",
                        fg="yellow",
                        bg="black",
                        font=("times", 15, "bold")
                    )
                    label.pack(pady=10)
                else:
                    # Display each attendance record
                    for csv_file in csv_files:
                        file_path = os.path.join(path, csv_file)
                        date_str = csv_file.split('_')[1]  # Get date from filename
                        
                        # Create a frame for each attendance record
                        record_frame = tkinter.Frame(scrollable_frame, bg="black")
                        record_frame.pack(pady=10, padx=10, fill="x")
                        
                        # Add date label
                        date_label = tkinter.Label(
                            record_frame,
                            text=f"Date: {date_str}",
                            fg="green",
                            bg="black",
                            font=("times", 12, "bold")
                        )
                        date_label.pack()
                        
                        # Create a frame for the table
                        table_frame = tkinter.Frame(record_frame, bg="black")
                        table_frame.pack(pady=5)
                        
                        # Read and display the CSV data
                        with open(file_path, newline="") as file:
                            reader = csv.reader(file)
                            for r, row in enumerate(reader):
                                for c, cell in enumerate(row):
                                    label = tkinter.Label(
                                        table_frame,
                                        width=15,
                                        height=1,
                                        fg="yellow",
                                        font=("times", 12),
                                        bg="black",
                                        text=cell,
                                        relief=tkinter.RIDGE
                                    )
                                    label.grid(row=r, column=c, padx=2, pady=2)
                
                attendance_window.mainloop()
            else:
                t = f"No attendance records found for {sub}"
                text_to_speech(t)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="dark blue",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="white",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="white",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="dark blue",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()