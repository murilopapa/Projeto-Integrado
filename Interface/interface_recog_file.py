#Importing necessary libraries, mainly the OpenCV, and PyQt libraries
import face_recognition
import os
import time
import multiprocessing


import cv2
import numpy as np
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

firstarg=sys.argv[1]

known_face_names = [] 
num_processadores = 2
num_frames = 7
path_video = firstarg
output_name = "praca4k3sec.avi"
acuracia_minima = 0.5
length = 0
#acuracia_minima de 0.6 eh no minimo 40% de ctz
#num_frames equivale á: quero pegar 1 frame a cada 3, logo, o valor de num_frames = 3


class image_queue:
        def __init__(self, frame, id):
            self.frame = frame
            self.id = id
            self.names = []

def func(frames_to_process_recived, known_face_encodings_recived, queue_recived, queue_images_recived):
    face_locations = []
    face_encodings = []
    face_names = []
    unknown_face = "Unknown"
    first_frame = frames_to_process_recived[0]
    del frames_to_process_recived[0]

    rgb_frame = first_frame.frame[:, :, ::-1]

    start_time = time.time()
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    elapsed_time = time.time() - start_time
    print("[INFO][{}] Tempo para achar rostos: {}".format(first_frame.id,elapsed_time))
    face_names = []
    start_time = time.time()
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        name = unknown_face
        
        face_distances = face_recognition.face_distance(known_face_encodings_recived, face_encoding)

        menor_dist = 1
        name_index = -1
        for i, face_distance in enumerate(face_distances):
            if face_distance < menor_dist:
                if face_distance < acuracia_minima:
                    menor_dist = face_distance
                    name_index = i
            


            # If a match was found in known_face_encodings, just use the first one.
        print("Valor do i: {}".format(i))
        if name_index != -1:
            name = '{} | {:.2f}'.format(known_face_names[name_index], ((1-menor_dist)*100))

        face_names.append(name)

    elapsed_time = time.time() - start_time
    print("[INFO][{}] Tempo para localizar faces: {}".format(first_frame.id,elapsed_time))

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue
        color = (0,0,255)
        if "Unknown" in name:
            color = (0,255,0)
        else:
            first_frame.names.append(name)

            # Draw a box around the face
        cv2.rectangle(first_frame.frame, (left, top), (right, bottom), color, 2)

            # Draw a label with a name below the face
        cv2.rectangle(first_frame.frame, (left, bottom - 25), (right, bottom), color, 2)
        cv2.putText(first_frame.frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        
    # Write the resulting image to the output video file
    queue_images_recived.put(first_frame)
    print("[INFO][{}] Sending processed frame {} / {}".format(first_frame.id, first_frame.id, length))

    for j in frames_to_process_recived:
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if not name:
                continue
            color = (0,0,255)
            if "Unknown" in name:
                color = (0,255,0)
                # Draw a box around the face
            cv2.rectangle(j.frame, (left, top), (right, bottom), color, 2)

                # Draw a label with a name below the face
            cv2.rectangle(j.frame, (left, bottom - 25), (right, bottom), color, 2)
            cv2.putText(j.frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        
    # Write the resulting image to the output video file
        print("[INFO][{}] Sending unprocessed frame {} / {}".format(j.id, j.id, length))
        queue_images_recived.put(j)


    return


class ShowVideo(QtCore.QObject):
 
    #initiating the built in camera
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)
    
 
    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)
 
    @QtCore.pyqtSlot()
    def startVideo(self):
 
        start_time = time.time()

        todas_as_frames = []

        # Open the input movie file
        input_movie = cv2.VideoCapture(path_video)
        length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

        # Create an output movie file (make sure resolution/frame rate matches input video!)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_movie = cv2.VideoWriter(output_name, fourcc, 30, (1280, 720))

        path = "imagens/"

        # Load some sample pictures and learn how to recognize them.
        directory = os.fsencode(path)
        count = 0
        known_face_encodings = []
        #known_face_names = []
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".jpg") or filename.endswith(".png"):
                known_face_encodings.append(face_recognition.face_encodings(
                    face_recognition.load_image_file(path+filename))[0])
                known_face_names.append(filename[:-4])
                count = count + 1
                continue

        print("[INFO] Banco de dados: {} imagens".format(count))
        print("[INFO] Frames encontradas: {}".format(length))
        print("[INFO] Processadores: {}".format(num_processadores))
        print("[INFO] Pegar 1 a cada {} frames".format(num_frames))
        unknown_face = "Desconhecido"
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        frame_number = 0


        process_this_frame = True

        queue = multiprocessing.Queue()
        queue_images = multiprocessing.Queue()
        queue.put(1)
        while process_this_frame:
            jobs = []
            counter = 0
            for i in range(0, num_processadores):
                frames_to_process = []
            # Grab a single frame of video
                for j in range(0, num_frames):
                    ret, frame = input_movie.read()
                    if not ret:
                        process_this_frame = False
                        break

                    frame_number += 1
                    counter += 1
                    #frame = cv2.flip( frame, 0 ) #uncomment this line if your video is upside down
                    #frame = cv2.resize(frame,(1280,720)) #uncomment this line if you want to change the input resolution. 1280x720 = Full HD
                    frames_to_process.append(image_queue(frame, frame_number))

                if frames_to_process:
                    process = multiprocessing.Process(target=func, args=(frames_to_process, known_face_encodings, queue, queue_images))
                    jobs.append(process)
                    process.start()
                    print("[INFO] Processo da frame {} ate {}  iniciado".format(frame_number-num_frames+1, frame_number))
                
            to_write = []
            for i in range(0,counter):
                to_write.append(queue_images.get())
                
            for i in range(0, counter):
                for t in to_write:
                    if t.id == (frame_number - counter + i + 1):
                        print("[INFO] Escrevendo frame :{}".format(t.id))
                        frame_write = cv2.resize(t.frame,(1280,720))
                        color_swapped_image = cv2.resize(t.frame,(640,360))
                        color_swapped_image = cv2.cvtColor(color_swapped_image, cv2.COLOR_BGR2RGB)
                        height, width, _ = color_swapped_image.shape
                        
                        #width = camera.set(CAP_PROP_FRAME_WIDTH, 1600)
                        #height = camera.set(CAP_PROP_FRAME_HEIGHT, 1080)
                        #camera.set(CAP_PROP_FPS, 15)
            
                        qt_image = QtGui.QImage(color_swapped_image.data,
                                                width,
                                                height,
                                                color_swapped_image.strides[0],
                                                QtGui.QImage.Format_RGB888)
            
                        self.VideoSignal.emit(qt_image)
                        
                        t.frame = None
                        todas_as_frames.append(t)
                        output_movie.write(frame_write)

            
            #print("Aguardando fim dos processos")
            for j in jobs:
                j.join()
            #print("Processos encerrados") 

        # All done!

        class reconhecidos:
            def __init__(self, name):
                self.names = name
                self.vezes = 1
                
        vetor_reconhecidos = []

        elapsed_time = time.time() - start_time
        print("[INFO] Benchmark status:")
        print("--- Tempo total: {}".format(elapsed_time))
        for t in todas_as_frames:
            #print("Verificando frame {}".format(t.id))
            for n in t.names:
                #print("Verificando nome {}".format(n))
                achou_nome = False
                for v in vetor_reconhecidos:
                    if n in v.names:
                        v.vezes += 1
                        achou_nome = True
                if not achou_nome:
                    vetor_reconhecidos.append(reconhecidos(n))

        for v in vetor_reconhecidos:
            print("--- {} apareceu em {} frames processadas".format(v.names, v.vezes))

        print("--- Banco de Dados: {} imagens".format(count))
        print("--- Total de Frames: {}".format(length))
        print("--- Processadores usados: {}".format(num_processadores))
        print("--- Processando 1 frame a cada {} frames".format(num_frames))

        input_movie.release()
        cv2.destroyAllWindows()
        os.system("python3 video.py " + output_name)
 
 
class ImageViewer(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
 
 
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0,0, self.image)
        self.image = QtGui.QImage()
 
    def initUI(self):
        self.setWindowTitle('Test')
 
    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")
 
        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()
 
 
if __name__ == '__main__':
 
    app = QtWidgets.QApplication(sys.argv)
    thread = QtCore.QThread()
    thread.start()
    vid = ShowVideo()
    vid.moveToThread(thread)
    image_viewer = ImageViewer()
 
    vid.VideoSignal.connect(image_viewer.setImage)
 
    #Button to start the videocapture:
 
    push_button1 =QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Test')
    push_button1.clicked.connect(vid.startVideo)
    vertical_layout = QtWidgets.QVBoxLayout()
    
 
    vertical_layout.addWidget(image_viewer)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)
 
    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)
 
    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())