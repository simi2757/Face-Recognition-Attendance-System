import csv
import datetime
import os
import shutil
import time
import tkinter as tk
import tkinter.font as font
from tkinter import *

import cv2
import numpy as np
import pandas as pd
import pyttsx3
from PIL import Image, ImageTk

import automaticAttedance
# project module
import show_attendance
import takeImage
import trainImage

engine = pyttsx3.init()
engine.say("Welcome!")
engine.say("Please browse through your options..")
engine.runAndWait()


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "./TrainingImageLabel/Trainner.yml"
)
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path,exist_ok=True)

studentdetail_path = (
    "./StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"

# Function to create a gradient background
def create_gradient(canvas, width, height, color1, color2):
    for i in range(height):
        r1, g1, b1 = canvas.winfo_rgb(color1)
        r2, g2, b2 = canvas.winfo_rgb(color2)
        r = int(r1 + (r2 - r1) * (i / height)) // 256
        g = int(g1 + (g2 - g1) * (i / height)) // 256
        b = int(b1 + (b2 - b1) * (i / height)) // 256
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color)

# Function to add hover effects to buttons
def add_hover_effects(button, hover_bg, hover_fg, normal_bg, normal_fg):
    def on_enter(event):
        button.config(bg=hover_bg, fg=hover_fg)

    def on_leave(event):
        button.config(bg=normal_bg, fg=normal_fg)

    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

window = Tk()
window.title("Face Recognizer")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="#1c1c1c")  # Dark theme

# Create gradient background
canvas = Canvas(window, width=1280, height=720)
canvas.pack(fill="both", expand=True)
create_gradient(canvas, 1280, 720, "#4b0082", "#000000")  # Purple to Black gradient

# to destroy screen
def del_sc1():
    sc1.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",  # Dark background for the error window
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",  # Darker button color
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True


logo = Image.open("UI_Image/0001.png")
logo = logo.resize((50, 47), Image.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="#4b0082",)
l1.place(x=470, y=10)


titl = tk.Label(
    window, text="CLASS VISION", bg="#4b0082", fg="yellow", font=("Verdana", 27, "bold"),
)
titl.place(x=500, y=25)

a = tk.Label(
    window,
    text="Welcome to CLASS VISION",
    bg="#1c1c1c",  # Dark background for the main text
    fg="yellow",  # Bright yellow text color
    bd=10,
    font=("Verdana", 35, "bold"),
)
a.place(x=300, y=100)  # Adjust x and y values as needed to position it at the top


ri = Image.open("UI_Image/register.png")
r = ImageTk.PhotoImage(ri)
label1 = Label(window, image=r)
label1.image = r
label1.place(x=100, y=270)

ai = Image.open("UI_Image/attendance.png")
a = ImageTk.PhotoImage(ai)
label2 = Label(window, image=a)
label2.image = a
label2.place(x=980, y=270)

vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)
label3 = Label(window, image=v)
label3.image = v
label3.place(x=600, y=270)


def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")  # Dark background for the image window
    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)
    # image and title
    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#1c1c1c", fg="green", font=("Verdana", 30, "bold"),
    )
    titl.place(x=270, y=12)

    # heading
    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",  # Dark background for the details label
        fg="yellow",  # Bright yellow text color
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(x=280, y=75)

    # ER no
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl1.place(x=120, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        validate="key",
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",  # Dark input background
        fg="yellow",  # Bright text color for input
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",  # Dark background for messages
        fg="yellow",  # Bright text color for messages
        relief=RIDGE,
        font=("Verdana", 14, "bold"),
    )
    message.place(x=250, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # take Image button
    # image
    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="dark blue",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # train Image function call
    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",  # Dark background for the button
        fg="dark blue",  # Bright text color for the button
        height=2,
        width=12,
        relief=RIDGE,
    )
    trainImg.place(x=360, y=350)

def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)





def view_attendance():
    show_attendance.subjectchoose(text_to_speech)

# Register Button
register_btn = tk.Button(
    canvas,
    text="Register a new student",
    font=("Verdana", 16, "bold"),  # Bold text
    bg="#4b0082",  # Purple background
    fg="black",  # White text
    height=2,
    width=17,
    command=lambda: TakeImageUI(),
)
register_btn.place(x=100, y=520)
add_hover_effects(register_btn, hover_bg="#6a0dad", hover_fg="purple", normal_bg="#4b0082", normal_fg="black")

# Attendance Button
attendance_btn = tk.Button(
    canvas,
    text="Take Attendance",
    font=("Verdana", 16, "bold"),  # Bold text
    bg="#4b0082",  # Purple background
    fg="black",  # White text
    height=2,
    width=17,
    command=lambda: automaticAttedance.subjectChoose(text_to_speech),
)
attendance_btn.place(x=600, y=520)
add_hover_effects(attendance_btn, hover_bg="#6a0dad", hover_fg="purple", normal_bg="#4b0082", normal_fg="black")

# View Attendance Button
view_btn = tk.Button(
    canvas,
    text="View Attendance",
    font=("Verdana", 16, "bold"),  # Bold text
    bg="#4b0082",  # Purple background
    fg="black",  # White text
    height=2,
    width=17,
    command=lambda: show_attendance.subjectchoose(text_to_speech),
)
view_btn.place(x=1000, y=520)
add_hover_effects(view_btn, hover_bg="#6a0dad", hover_fg="purple", normal_bg="#4b0082", normal_fg="black")

# Exit Button
exit_btn = tk.Button(
    canvas,
    text="EXIT",
    font=("Verdana", 16, "bold"),  # Bold text
    bg="#ff0000",  # Red background
    fg="black",  # White text
    height=2,
    width=17,
    command=window.quit,
)
exit_btn.place(x=600, y=660)
add_hover_effects(exit_btn, hover_bg="#ff4d4d", hover_fg="purple", normal_bg="#ff0000", normal_fg="black")
window.mainloop()






