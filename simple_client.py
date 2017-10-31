import socket
from config import HOST, PORT, secret_key
import pickle
import hmac
import os


command = ''
while command != '4':

    command = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print('Команды:\n 1 - вывести всех лекторов\n '
          '2 - добавить лектора\n'
          '')


    command = input('Введите команду:\n')

    if command == '1':
        sock.send(bytes(command, 'utf-8'))
        b_data = sock.recv(1024)
        data = pickle.loads(b_data)
        print(data)
        sock.close()
    elif command == '2':
        lecturer_name = input('Введите Имя нового лектора:\n')
        sock.send(bytes('{}:{}'.format(command, lecturer_name), 'utf-8'))
        b_data = sock.recv(1024)
        print(b_data.decode('utf-8'))
        sock.close()
