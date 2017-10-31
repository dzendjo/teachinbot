import socketserver
from config import HOST, PORT, secret_key
import teachinbot
import pickle

class BotServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print('Пришло в данные: {}'.format(self.data))
        self.bot = teachinbot.Teachinbot()

        if self.data.decode('utf-8') == '1':
            data = pickle.dumps(self.bot.get_all_lecturers())
            self.request.send(data)
        elif self.data.decode('utf-8').split(':')[0] == '2':
            lector_name = self.data.decode('utf-8').split(':')[1]
            print(lector_name)
            self.bot.add_lecturer(lector_name)
            self.request.send(bytes('Лектор {} добавлен'.format(lector_name), 'utf-8'))

            # print("Клиент не прошел авторизацию")


        print('{} wrote:'.format(self.client_address[0]))
        print(self.data)

server = socketserver.TCPServer((HOST, PORT), BotServer)
print('Server has run')
server.serve_forever()

