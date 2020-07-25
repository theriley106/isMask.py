import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

while True:
    face_mask = None
    small_frame = cv2.resize(video_capture.read()[1], (0, 0), fx=0.25, fy=0.25)

    if face_recognition.face_locations(small_frame, model="cnn"):
        face_mask = 'top_lip' not in str(face_recognition.face_landmarks(small_frame))

    print({None: "NO FACE", True: "FACE MASK ON", False: "FACE MASK OFF"}[face_mask])

video_capture.release()