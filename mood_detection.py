import cv2
import face_recognition
import numpy as np
import os  # Import os module
from deepface import DeepFace
from weather import get_weather_and_aqi
from location import get_location

# Load known faces and their names
known_face_encodings = []
known_face_names = []

# Specify the directory containing your face images
base_face_dir = r"F:\Project\face_files"  # Base directory

# Loop through all user folders in the specified directory
for user_folder in os.listdir(base_face_dir):
    user_folder_path = os.path.join(base_face_dir, user_folder)
    
    # Check if the path is a directory
    if os.path.isdir(user_folder_path):
        for filename in os.listdir(user_folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(user_folder_path, filename)
                try:
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        known_face_encodings.append(face_encodings[0])
                        known_face_names.append(user_folder)  # Use the folder name as the name
                    else:
                        print(f"No face encodings found in the provided image: {filename}")
                except Exception as e:
                    print(f"Error processing image {filename}: {e}")

def recognize_faces_and_mood():
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture frame.")
            break

        rgb_frame = frame[:, :, ::-1]

        # Find faces and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = []

        if face_locations:
            for face_location in face_locations:
                top, right, bottom, left = face_location
                
                if top < bottom and left < right:
                    face_image = rgb_frame[top:bottom, left:right]
                    face_image = np.array(face_image, dtype=np.uint8)

                    encodings = face_recognition.face_encodings(face_image)

                    if encodings:
                        face_encodings.append(encodings[0])

        if len(face_encodings) > 0:
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    # Mood detection
                    try:
                        analysis = DeepFace.analyze(face_image, actions=['emotion'], enforce_detection=False)
                        mood = analysis[0]['dominant_emotion']
                    except Exception as e:
                        mood = "Unknown"
                        print(f"Error detecting mood: {e}")

                    # Get weather and AQI
                    weather_info = get_weather_and_aqi()
                    location = get_location()

                    # Display the name, mood, and weather info
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, f"{name}: {mood}", (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(frame, weather_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    cv2.putText(frame, location, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

recognize_faces_and_mood()