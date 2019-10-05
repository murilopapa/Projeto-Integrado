import face_recognition
import cv2
import os
import requests
import numpy as np

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# 0 é a webcam nativa, ver o print do loop abaixo para ver as webcans disponiveis

escale = 0.5
camera_default = 0
path = "imagens/"
unknown_face = "Unknown"




cams_test = 10
for i in range(0, cams_test):
    cap = cv2.VideoCapture(i)
    test, frame = cap.read()
    print("i : "+str(i)+" /// result: "+str(test))



video_capture = cv2.VideoCapture(camera_default)

directory = os.fsencode(path)
count = 0
known_face_encodings = []
known_face_names = []
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".jpg") or filename.endswith(".png"):
        known_face_encodings.append(face_recognition.face_encodings(
            face_recognition.load_image_file(path+filename))[0])
        known_face_names.append(filename[:-4])
        count = count + 1
        continue

print("Banco de dados: {} imagens".format(count))


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = 0

while True:
    # Grab a single frame of video
    # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) Descomentar essa linha e trocar frame por gray para gerar imagem em preto e branco 
    ret, frame = video_capture.read()
    #frame = cv2.flip( frame, 0 )
    # Resize frame of video to "escale" size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=escale, fy=escale)
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame % 7 == 0:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = unknown_face

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = process_this_frame + 1

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face lopathd to 1/4 size
        top *= int(1/escale)
        right *= int(1/escale)
        bottom *= int(1/escale)
        left *= int(1/escale)
        
        color = (0, 0, 255)
        if unknown_face in name:
            color = (0, 255, 0)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)
        print(name + " encontrado!")
    # Display the resulting image
    
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
