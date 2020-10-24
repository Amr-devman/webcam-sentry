import face_recognition
import numpy as np

from utilities.db_functions import select_query, decode_arr

#wrapper function to get face encodings
def get_face_encodings(image):
	return face_recognition.face_encodings(image)[0]

#wrapper function to get face location
def get_face_locations(image):
	return face_recognition.face_locations(image)

#function that does the main comparison between the unknown face and the stored faces
def detect_and_match_faces(roi, userid):
	face_locations = get_face_locations(roi)

	if len(face_locations) == 0:
		return -99

	unknown_encodings = face_recognition.face_encodings(roi, face_locations)

	#get stored encodings
	db_file = f"{userid}.db"
	whitelist = select_query(db_file, ["name", "embeddings"], "whitelist")

	whitelist_names_np = whitelist["name"].values
	whitelist_embeddings_np = []

	for embedding in whitelist["embeddings"].values:
		whitelist_embeddings_np.append(decode_arr(embedding))

	whitelist_embeddings_np = np.array(whitelist_embeddings_np)

	unmatched_faces = 0
	for suspect_idx, suspect in enumerate(unknown_encodings):
		suspect = np.expand_dims(suspect, axis=0)
		matches = face_recognition.compare_faces(whitelist_embeddings_np, suspect)

		if True in matches:
			continue
		else:
			unmatched_faces += 1

	return unmatched_faces