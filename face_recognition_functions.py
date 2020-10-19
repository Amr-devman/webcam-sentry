import face_recognition
import numpy as np


def get_face_encodings(image):
	return face_recognition.face_encodings(image)[0]

