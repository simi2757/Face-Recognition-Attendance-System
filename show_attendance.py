import csv
import os
import tkinter
import tkinter as tk
from glob import glob
from tkinter import *

import pandas as pd


def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
            return

        # Use os.path.join for cross-platform compatibility
        subject_path = os.path.join("Attendance", Subject)
        if not os.path.exists(subject_path):
            t = f"No attendance records found for {Subject}"
            text_to_speech(t)
            return

        # Get all CSV files for the subject
        filenames = glob(os.path.join(subject_path, f"{Subject}*.csv"))
        if not filenames:
            t = f"No attendance records found for {Subject}"
            text_to_speech(t)
            return

        try:
            # Read all CSV files
            df = [pd.read_csv(f) for f in filenames]
            newdf = df[0]
            
            # Merge all dataframes
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
            
            # Fill NaN values with 0
            newdf.fillna(0, inplace=True)
            
            # Calculate attendance percentage
            newdf["Attendance"] = 0
            for i in range(len(newdf)):
                # Calculate percentage based on attendance columns (excluding Enrollment, Name, and Attendance columns)
                attendance_cols = newdf.columns[2:-1]  # Exclude Enrollment, Name, and Attendance columns
                if len(attendance_cols) > 0:
                    attendance_percentage = str(int(round(newdf.iloc[i][attendance_cols].mean() * 100))) + '%'
                else:
                    attendance_percentage = "0%"
                newdf["Attendance"].iloc[i] = attendance_percentage

            # Save the combined attendance
            output_file = os.path.join(subject_path, "attendance.csv")
            newdf.to_csv(output_file, index=False)

            # Display the attendance in a new window
            root = tkinter.Tk()
            root.title(f"Attendance of {Subject}")
            root.configure(background="black")
            
            # Create a frame with scrollbar
            frame = tkinter.Frame(root, bg="black")
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

            # Display the data
            with open(output_file) as file:
                reader = csv.reader(file)
                for r, col in enumerate(reader):
                    for c, row in enumerate(col):
                        label = tkinter.Label(
                            scrollable_frame,
                            width=15,
                            height=1,
                            fg="white",
                            font=("times", 12),
                            bg="black",
                            text=row,
                            relief=tkinter.RIDGE
                        )
                        label.grid(row=r, column=c, padx=2, pady=2)

            root.mainloop()
            print(newdf)
        except Exception as e:
            print(f"Error processing attendance: {str(e)}")
            t = "Error processing attendance records"
            text_to_speech(t)

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
        text="Which Subject of Attendance?",
        bg="black",
        fg="pink",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
            f"Attendance\\{sub}"
            )


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
        text="View Attendance",
        command=calculate_attendance,
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