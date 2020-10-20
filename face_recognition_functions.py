import face_recognition
import numpy as np

from db_functions import select_query, convert_array

def get_face_encodings(image):
	return face_recognition.face_encodings(image)[0]

def get_face_locations(image):
	return face_recognition.face_locations(image)

def detect_and_match_faces(roi, userid):
	face_locations = get_face_locations(roi)

	if len(face_locations) == 0:
		return -99

	unknown_encodings = face_recognition.face_encodings(roi, face_locations)

	#get stored encodings
	db_file = f"{userid}.db"
	whitelist = select_query(db_file, ["name", "embeddings"], "whitelist")

	whitelist["embeddings"] = np.vectorize(convert_array)(whitelist["embeddings"])
	whitelist_names_np = whitelist["name"].values
	whitelist_embeddings_np = whitelist["embeddings"].values

	unmatched_faces = 0

	for suspect_idx, suspect in enumerate(unknown_encodings):
		matches = face_recognition.compare_faces(whitelist_embeddings_np, suspect)

		if True in matches:
			continue
		else:
			unmatched_faces += 1

	return unmatched_faces