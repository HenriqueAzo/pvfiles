import socket
import time
import select
import cv2 as cv
import numpy as np


#globais
IP = '45.6.72.207'
PORT = 7777
Header = 30

people = ['Azoubel', 'Fred', 'Neymar']

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind((IP, PORT))
server.listen(5)
sockets_list = [server]
clients = {} #
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
# analise da imagem
def anal(i):
    features = np.load('features.npy', allow_pickle=True)
    labels = np.load('labels.npy', allow_pickle=True)
    face_recognizer= cv.face.LBPHFaceRecognizer_create()
    face_recognizer.read('face_azoubel.yml')
    img = cv.imread(f'file_{i}.jpg')
    resized = cv.resize(img, (500,500), interpolation=cv.INTER_AREA)
    gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
    haar = cv.CascadeClassifier('haar_cascade.xml')
    faces_detected = haar.detectMultiScale(gray, scaleFactor=1.1 , minNeighbors= 5)

    if len(faces_detected) != 1: #interrompe a analise se tiver qualquer numero de faces diferente de 1
        return 0

    for (x,y,a,b) in faces_detected:
        face_roi = gray[y:y+b, x:x+a]
        label, confidence  = face_recognizer.predict(face_roi)
        message = f'Label = {people[label]} with confidence of {confidence}'

    return message

#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------
# _main_
def SERVER():
    i = 1
    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
        for notified_socket in read_sockets:
            if notified_socket == server:
                client_socket, client_address = server.accept()
                print(client_address)
                client_socket.send(bytes('Envie UMA foto para analise', 'utf-8'))

                with open('file_'+ str(i)+".jpg",'wb') as f: #open in byte mode
                    # receive data and write it to file
                    print('Reciving data...')
                    ubytes = client_socket.recv(1024)
                    len_file = int(ubytes.decode())
                    print(len_file)
                    ubytes = client_socket.recv(len_file)
                    file = ubytes
                    print(len(file)) #printando o tamanho do arquivo
                    if len(file) <= len_file:
                        print('File received!')
                        f.write(file)
                        f.close() #linha possivelmente inutil
                    else:
                        print('Transfer Failed')
                        client_socket.close()
                        break

            #try: # tenta abrir a função de analise -
            # basicamente se não for uma imagem ou imagem estiver corronppida o codigo para e a conexão fecha
                message = anal(i)
                print(message)
                i=i+1 #caso queira receber mais de uma foto, mais de um arquivo eh criado e mais de uma mensagem eh recebida de volta
                client_socket.send(bytes(message, 'utf-8'))
                pass
            #except:
                print('Connection closed')
                client_socket.close()
        exit()

if __name__ == '__main__':
    SERVER()
