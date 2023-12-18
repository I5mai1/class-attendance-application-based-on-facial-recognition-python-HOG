Face Recognition App
Overview

The Face Recognition App is a Python script (mainIMP.py) that utilizes the Tkinter library for the graphical user interface, OpenCV for capturing video frames, and face_recognition for facial recognition. The script integrates SQLite for database operations and stores facial encodings in a pickle file.
Features

    Real-time face recognition using a webcam.
    Attendance marking for recognized faces.
    Database integration for student information.

Prerequisites

Ensure that you have the required Python libraries installed. You can install them using the following command:

bash

pip install tkinter pillow opencv-python numpy face_recognition

Usage

    Run the script:

    bash

    python mainIMP.py

    The Tkinter window will open, displaying real-time face recognition.

    If a face is recognized, the attendance is marked.

    Click the "Register" button to add a new student to the attendance list.

Configuration

    Camera Index: You can modify the camera_index variable in the script to specify the camera index.

    Pickle File Location: The script uses a pickle file (faceModel.pickle) to store facial encodings. Update the pickle_file_location variable if needed.

    Detection Model: The detection model used for face recognition is specified by the detection_model variable. You can change it to 'hog' or 'cnn' based on your preference.

Database

    The script connects to an SQLite database (students_book.db) to store student information.

Author

    ARAR Ismail
