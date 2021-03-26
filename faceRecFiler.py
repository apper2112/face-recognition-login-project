import os
import cv2
import pickle
import numpy as np
import face_recognition

# DIRECTORIES,FILE PATHS AND GLOBAL VARS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = BASE_DIR + '/images'
labels_pickle_file = BASE_DIR + '/labels.pickle'


class Dlib_Face_Unlock:
	def __init__(self):
		self.current_id = 0
		self.labels_ids = {}
		self.og_labels = 0
		self.file_startar()

	def file_startar(self):
		try:
			# OPEN PICKLE FILE FOR COMPARING DICTIONARIES
			with open(labels_pickle_file, 'rb') as self.f:
				self.og_labels = pickle.load(self.f)
		except FileNotFoundError:
			print("First Run..After hitting the Submit button")
			print("The webcam may be slow to load at first.")
			if not os.path.exists(IMAGES_DIR):
				os.makedirs(IMAGES_DIR)
			if os.path.exists(labels_pickle_file):
				os.remove(labels_pickle_file)

		# GETTING USERNAMES AND IDS
		for pics in os.listdir(IMAGES_DIR):
			if pics.endswith('png') or pics.endswith('jpg'):
				self.label = pics.split('.')[0]
				if not self.label in self.labels_ids:
					self.labels_ids[self.label] = self.current_id
					self.current_id += 1

		# CHECK FOR ANY NEW USERS/CHANGES BY COMPARING DICTIONARIES
		if self.labels_ids != self.og_labels:
			print('Dictionary changed')
			with open(labels_pickle_file, 'wb') as self.file:
				pickle.dump(self.labels_ids, self.file)
			self.known_faces = []
			for pic in self.labels_ids:
				self.directory = os.path.join(IMAGES_DIR, pic) + '.png'
				self.img = face_recognition.load_image_file(self.directory)
				self.img_encoding = face_recognition.face_encodings(self.img)[0]
				self.known_faces.append([pic, self.img_encoding])
			with open(BASE_DIR + '/KnownFace.pickle','wb') as self.known_faces_file:
				pickle.dump(self.known_faces, self.known_faces_file)
		else:
			print('No dictionary change')
			with open(BASE_DIR + '/KnownFace.pickle','rb') as self.faces_file:
				self.known_faces = pickle.load(self.faces_file)
		# SHOW FACE RECOGNITION VALUES OF PEOPLE
		#print(self.known_faces)


	# TURN ON CAMERA, GET IMAGE AND ENCODE AND COMPARE ENCODINGS IN THE KNOWN FACES FILE
	def ID(self):
		self.cap = cv2.VideoCapture(0)
		self.running = True
		self.face_names = []
		while self.running == True:
			# GRAB PHOTO
			self.ret, self.frame = self.cap.read()
			# RESIZE FRAME
			self.small_frame = cv2.resize(self.frame, (0,0), fx=0.5, fy=0.5)
			# CONVERT TO BLACK AND WHITE
			self.rgb_small_frame = self.small_frame[:, :, ::-1]
			if self.running:
				# SEARCH FOR FACE
				self.face_locations = face_recognition.face_locations(self.frame)
				self.face_encodings = face_recognition.face_encodings(self.frame, self.face_locations)
				self.face_names = []

				# LOOP THROUGH FACE ENCODINGS
				for self.face_encoding in self.face_encodings:
					for self.face in self.known_faces:
						self.matches = face_recognition.compare_faces([self.face[1]], self.face_encoding)
						# COMPARE DISTANCES
						self.face_distances = face_recognition.face_distance([self.face[1]], self.face_encoding)
						# GRAB BEST MATCH
						self.best_match = np.argmin(self.face_distances)
						if self.matches[self.best_match] == True:
							self.running = False
							self.face_names.append(self.face[0])
							break
						next
			self.cap.release()
			cv2.destroyAllWindows()
			break
		return self.face_names
