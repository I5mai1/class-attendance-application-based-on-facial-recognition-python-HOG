import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition
import pickle
import sqlite3
from datetime import datetime

class FaceRecognitionApp:
    def __init__(self, camera_index=0, pickle_file_location="faceModel.pickle", detection_model="hog"):
        self.camera_index = camera_index
        self.pickle_file_location = pickle_file_location
        self.detection_model = detection_model

        self.data = pickle.loads(open(self.pickle_file_location, "rb").read())

        self.root = tk.Tk()
        self.root.geometry("500x400")
        self.root.title("Face Recognition App")

        self.label = Label(self.root)
        self.label.grid(row=0, column=0)

        self.cap = cv2.VideoCapture(self.camera_index)

        self.create_database_connection()

        self.create_gui_elements()

    def create_database_connection(self):
        self.conn = sqlite3.connect('students_book.db')
        self.cursor = self.conn.cursor()

    def create_gui_elements(self):
        tk.Label(self.root, text="IF YOU ARE NOT A PART OF THIS CLASS").grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
        tk.Label(self.root, text="------------------------------------").grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        add_button = Button(self.root, text="Register", command=self.add_student)
        add_button.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

        self.show_frames()

    def add_student(self):
        add_window = tk.Toplevel(self.root)
        add_window.title('Add Student')
        add_window.geometry("400x200")

        tk.Label(add_window, text="First Name").grid(row=0, column=0)
        tk.Label(add_window, text="Last Name").grid(row=1, column=0)
        tk.Label(add_window, text="Email").grid(row=2, column=0)

        first_name_entry = tk.Entry(add_window, width=30)
        last_name_entry = tk.Entry(add_window, width=30)
        email_entry = tk.Entry(add_window, width=30)

        first_name_entry.grid(row=0, column=1, padx=20)
        last_name_entry.grid(row=1, column=1)
        email_entry.grid(row=2, column=1)

        submit_button = Button(add_window, text="Add to Attendance List", command=lambda: self.submit_student(first_name_entry.get()))
        submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    def submit_student(self, first_name):
        self.mark_attendance(first_name)

    def mark_attendance(self, name):
        # Your attendance marking logic goes here
        pass

    def show_frames(self):
        rgb = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, (0, 0), None, 0.25, 0.25)
        img = Image.fromarray(rgb)

        boxes = face_recognition.face_locations(rgb, model=self.detection_model)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        for encoding in encodings:
            matches = face_recognition.compare_faces(self.data["encodings"], encoding)
            face_dis = face_recognition.face_distance(self.data["encodings"], encoding)

            name = "Unknown"
            if True in matches:
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matched_idxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)

            if min(face_dis > 0.5):
                name = "Unknown"
            else:
                name = name
                names.append(name)
                self.mark_attendance(name)

        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.label.after(20, self.show_frames)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FaceRecognitionApp()
    app.run()
