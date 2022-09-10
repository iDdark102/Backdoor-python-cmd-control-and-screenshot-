import os
import socket

host = '127.0.0.1'
port = 8221
tupla=(host,port)


while True:
    #-----Configurações do socket---------
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host,port))
    servidor.settimeout(3)
    servidor.listen()
    #---------Definindo variáveis---------
    conectados = []


    while True:
        try:
            print('Server escutando')
            chave_conexao, endereco = servidor.accept()
            print(f'O cliente {endereco} se conectou ao servidor!')
            conectados.append([endereco, chave_conexao])
            chave_conexao.send(str.encode('Você se conectou com o servidor!'))
            
        except:
            qtde = len(conectados)
            
            if qtde == 0:
                print('Nenhum cliente conectado, prucurando conexão novamente!')
            else:
                break
                
    for i, content in enumerate(conectados):
        print(f'[{i}] {conectados[i-1][0]}')

    print('[fim, end, finish] desligar o servidor.\n[free] encerra o programa de todos os clientes ativos.\n[reload] reinicia o servidor e atualiza lsita de clientes ativos.')
    com_qual = input('Conectar com:')


    if str(com_qual) == 'reload':
        for i, content in enumerate(conectados):
            enviar = conectados[i-1][1]
            try:
                enviar.send(str.encode("reload"))
            except:
                continue
    elif com_qual == 'fim' or com_qual == 'end' or com_qual == 'finish':
        for i, content in enumerate(conectados):
            enviar = conectados[i-1][1]
            try:
                enviar.send(str.encode("reload"))
            except:
                continue
        break
    elif com_qual == 'free':
        for i, content in enumerate(conectados):
            enviar = conectados[i-1][1]
            try:
                enviar.send(str.encode("free"))
            except:
                continue

    #mensagem = chave_conexao.recv(1024).decode()
    #print(mensagem)
    
print('Servidor finalizado!')
servidor.close()