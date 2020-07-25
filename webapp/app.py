from flask import Flask, render_template
from flask_sockets import Sockets
import time
import face_recognition
import base64
import cv2
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
		try:
			message = str(message).split(",")[1]
			with open("tmp", "wb") as fh:
				fh.write(base64.b64decode(str(message)))
			small_frame = face_recognition.load_image_file("tmp")
			if face_recognition.face_locations(small_frame, model="cnn"):
				ws.send("FACE MASK ON" if "top_lip" not in str(face_recognition.face_landmarks(small_frame)) else "FACE MASK OFF")
			else:
				ws.send("NO FACE")
		except Exception as exp:
			pass
		time.sleep(.1)

@app.route('/', methods=['GET'])
def echo_test():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()
	# Start with gunicorn -k flask_sockets.worker app:app