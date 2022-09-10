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







#--------configuracoes do socket cliente -------------------



while True:
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #        cliente.settimeout(0)
            tupla = pegando_ip_com_webscrapping()
            cliente.connect(tupla)
            
            mensagem = cliente.recv(1024).decode()
            
            if mensagem != 'Você se conectou com o servidor!':
                print('Tráfego cruzado! refazendo conexão!')
                pass
            else:
                print(mensagem)
                break
        except:
            
            print('Servidor fechado, tentando novamente...')
    comando = cliente.recv(1024).decode()
    print(comando)
    if comando == 'reload':
        pass
    elif comando == 'free':
        break
print('free')
#cliente.send(str.encode(str(input('Digite sua mensagem:'))))
    
    
    



