#Importing necessary libraries, mainly the OpenCV, and PyQt libraries
import cv2
import numpy as np
import sys
import os
import face_recognition
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
 
class ShowVideo(QtCore.QObject):
 
    #initiating the built in camera
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)
    
 
    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)
 
    @QtCore.pyqtSlot()
    def startVideo(self):
        path = "imagens/"
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
        
        video_capture = self.camera
        unknown_face = "Unknown"
        escale = 0.5

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = 0
        print("pre while")
        while True:
            # Grab a single frame of video
            # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) Descomentar essa linha e trocar frame por gray para gerar imagem em preto e branco 
            print("while")
            ret, frame = video_capture.read()
            #frame = cv2.flip( frame, 0 )
            # Resize frame of video to "escale" size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=escale, fy=escale)
            
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
            if process_this_frame % 15 == 0:
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
            
            
            image = frame
 
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
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
    #push_button2 = QtWidgets.QPushButton('Test')
    push_button1.clicked.connect(vid.startVideo)
    vertical_layout = QtWidgets.QVBoxLayout()
    
 
    vertical_layout.addWidget(image_viewer)
    vertical_layout.addWidget(push_button1)
    #vertical_layout.addWidget(push_button2)
 
    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)
 
    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())