import face_recognition
import cv2
import os
import time
import multiprocessing

num_processadores = 4                                           #num de processos simultaneos que o pc aguenta
num_frames = 3                                                  #1 a cada "num_frames" para processar
path_video = "/home/murilo/Github/Dataset PI/praca4k3sec.mp4"   #caminho onde o video para processar está
output_name = "praca4k3sec.avi"                                 #nome do output do video
acuracia_minima = 0.4                                           #acuracia_minima de 0.4 eh no minimo 60% de ctz
path = "imagens/"                                               #path é onde ta as img do BD


#struct para armazenar as frames, os nomes que apareceram nela, e o id, que é o numero dela, pra organizar na ordem
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
        print("face encoding:")
        print(face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings_recived, face_encoding)

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






if __name__ == '__main__':

    start_time = time.time()        #timer para ver quanto tempo durou o processo, que vai ser removido cepa

    todas_as_frames = []            #vetor com todas as frames ja processadas

    # Tratamento do video de input
    input_movie = cv2.VideoCapture(path_video)
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Tratamento do video de output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output_movie = cv2.VideoWriter(output_name, fourcc, 30, (1280, 720))

    # Carrega o database
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

    # Alguns prints de controle
    print("[INFO] Banco de dados: {} imagens".format(count))    #num de img no bd
    print("[INFO] Frames encontradas: {}".format(length))       #num de frames do video
    print("[INFO] Processadores: {}".format(num_processadores)) #num de processos simultaneos
    print("[INFO] Pegar 1 a cada {} frames".format(num_frames)) #1 a cada x frames pra processar
    
    unknown_face = "Desconhecido"   #da o nome para rostos desconhecidos

    # Inicializando algumas variaveis
    face_locations = []     #aqui guarda onde esta as faces encontradas nas frames
    face_encodings = []     
    face_names = []         
    frame_number = 0        #qual frame eu estou pegando, pra ter a contagem


    process_this_frame = True   #pra saber se tem que processar a frame ou nao

    #nao lembro direito, rs, mas sei que é pra passar as coisas pros processos
    queue = multiprocessing.Queue() 
    queue_images = multiprocessing.Queue()
    queue.put(1)

    while process_this_frame:
        jobs = []   #salva os processos
        counter = 0 
        for i in range(0, num_processadores):   #loop pra fazer os processos
            frames_to_process = []      #frames para processar
        # Grab a single frame of video
            for j in range(0, num_frames):      #um loop para o num de frames totais que um processo vai pegar
                ret, frame = input_movie.read() #pego a frame do video
                if not ret:     #se acabou
                    process_this_frame = False
                    break

                frame_number += 1   #somo 1 na var
                counter += 1        #somo 1 na var

                #pra caso precise flipar o video
                #frame = cv2.flip( frame, 0 ) #uncomment this line if your video is upside down
                #frame = cv2.resize(frame,(1280,720)) #uncomment this line if you want to change the input resolution. 1280x720 = Full HD

                frames_to_process.append(image_queue(frame, frame_number))  #salvo a frame, e o num dela

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