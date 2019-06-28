import face_recognition
import cv2
import time
import os
# This code finds all faces in a list of images using the CNN model.
#
# This demo is for the _special case_ when you need to find faces in LOTS of images very quickly and all the images
# are the exact same size. This is common in video processing applications where you have lots of video frames
# to process.
#
# If you are processing a lot of images and using a GPU with CUDA, batch processing can be ~3x faster then processing
# single images at a time. But if you aren't using a GPU, then batch processing isn't going to be very helpful.
#
# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read the video file.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Open video file
start_total_time = time.time()

video_capture = cv2.VideoCapture("/home/murilo/Github/Dataset PI/praca4k20sec.mp4")
length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

batch_size = 2
frames = []
frame_count = 0

output_name = "GPUoutput1.avi"
path = "imagens/"
acuracia_minima = 0.5
# Load some sample pictures and learn how to recognize them.
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

print("[INFO] Banco de dados: {} imagens".format(count))
unknown_face = "Desconhecido"
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
frame_number = 0


fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter(output_name, fourcc, 30, (1280, 720))






while video_capture.isOpened():
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Bail out when the video file ends
    if not ret:
        break
    #frame = cv2.resize(frame,(1080,720))
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    #frame = frame[:, :, ::-1]

    # Save each frame of the video to a list
    frame_count += 1
    frames.append(frame)
    # Every 128 frames (the default batch size), batch process the list of frames to find faces
    if len(frames) == batch_size:
        batch_time = time.time()
        batch_of_face_locations = face_recognition.batch_face_locations(frames, number_of_times_to_upsample=0, batch_size=batch_size)
        final_batch_time = time.time() - batch_time

        tempo_restante = (length-frame_count)/batch_size * final_batch_time
        tempo_restante_h = tempo_restante / 3600
        tempo_restante_m = (tempo_restante / 60) % 60
        tempo_restante_s = tempo_restante % 60
        print("Tempo restante: {:.0f}:{:.0f}:{:.0f}".format(tempo_restante_h, tempo_restante_m, tempo_restante_s), end='\r')
        #print("Tempo do batch_face_locations para {} frames: {}".format(batch_size, final_batch_time))
        

        aux = 0
        for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
            face_encodings = face_recognition.face_encodings(frames[aux], face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                name = unknown_face

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                menor_dist = 1
                name_index = -1
                for i, face_distance in enumerate(face_distances):
                    if face_distance < menor_dist:
                        if face_distance < acuracia_minima:
                            menor_dist = face_distance
                            name_index = i
                    


                    # If a match was found in known_face_encodings, just use the first one.
                if name_index != -1:
                    name = '{} | {:.2f}'.format(known_face_names[name_index], ((1-menor_dist)*100))

                face_names.append(name)


            # Label the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                if not name:
                    continue
                color = (0,0,255)
                if "Unknown" in name:
                    color = (0,255,0)
                else:
                    face_names.append(name)

                    # Draw a box around the face
                cv2.rectangle(frames[aux], (left, top), (right, bottom), color, 2)

                    # Draw a label with a name below the face
                cv2.rectangle(frames[aux], (left, bottom - 25), (right, bottom), color, 2)
                cv2.putText(frames[aux], name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
            frame_to_write = frames[aux]
            frame_to_write = cv2.resize(frames[aux],(1280,720))
            output_movie.write(frame_to_write)
            i+=1

        # Clear the frames array to start the next batch
        frames = []

final_total_time = time.time() - start_total_time
print("Tempo total: {}".format(final_total_time))