import socket
import time

img = 'user_photo.jpg'
Header = 30
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 7777))


msg = client.recv(2048)
print(msg.decode())

with open("user_photo.jpg", "rb") as F:
    by = F.read() # lê o arquivo inteiro, como é uma imagem tá de boa mas se chegar nos megabytes ferrou
    print('Sending data...')
    client.send(bytes(f'{len(by)}','utf-8')) #envia o tamanho primeiro para poder ajustar o recv no servidor
    time.sleep(1) #uma pausa para o servidor se ajustar 1seg
    client.send(by) # envia todo arquivo

msg = client.recv(1024) #esperando o resultado da analise
print(msg.decode())

client.close()
