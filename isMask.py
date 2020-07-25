import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

while True:
    small_frame = cv2.resize(video_capture.read()[1], (0, 0), fx=0.25, fy=0.25)

    if face_recognition.face_locations(small_frame, model="cnn"):
        print({True: "FACE MASK ON", False: "FACE MASK OFF"}["top_lip" not in str(face_recognition.face_landmarks(small_frame))])
    else:
    	print("NO FACE")

video_capture.release()