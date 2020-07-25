# Copy of http://stackoverflow.com/a/20104705
from flask import Flask, render_template
from flask_sockets import Sockets
import datetime
import time
import face_recognition

import base64
from PIL import Image
import cv2
from io import StringIO
import numpy as np

app = Flask(__name__)

sockets = Sockets(app)

def readb64(uri):
	encoded_data = uri.split(',')[1]
	nparr = np.fromstring(base64.b64encode(bytes(encoded_data, 'utf-8')), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img

@sockets.route('/echo')
def echo_socket(ws):
	while True:
		message = ws.receive()
		# print(message)
		try:
			message = str(message).split(",")[1]
			with open("imageToSave.png", "wb") as fh:
				fh.write(base64.b64decode(str(message)))
			small_frame = face_recognition.load_image_file("imageToSave.png")
			if face_recognition.face_locations(small_frame, model="cnn"):
				print("FACE MASK ON" if "top_lip" not in str(face_recognition.face_landmarks(small_frame)) else "FACE MASK OFF")
			else:
				print("NO FACE")
			# cv2.imshow("decoded", decoded_img)
		except Exception as exp:
			print(exp)
		ws.send(str(datetime.datetime.now()))
		time.sleep(.1)

@app.route('/')
def hello():
	return 'Hello World!'

@app.route('/echo_test', methods=['GET'])
def echo_test():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()
	# Start with gunicorn -k flask_sockets.worker app:app