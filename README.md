# backdoor-python-only-cmd-control-


#aplicativos necessários:
#-Ngrok


#Bibliotecas:
#-os
#-requests
#-beautifulsoup4
#-subprocess
#-socket


# esse backdoor tem um "server.py" e um "cliente .py", quando um "cliente.py" é executado em uma máquina, a mesma começa a fazer requisições para
# https://cmdrequ3st.wixsite.com/request    em busca de um ip e uma porta publicados nessa página.
# caso o ip e porta estejam errados, ou até mesmo seja de um servidor diferente o cliente cancela a conexão e tenta novamente, e esse processo se repete
# infinitamente até que o servidor seja aberto e publicado no site, para assim a conexão se estabelecer, e o servidor ter controle sobre o cmd do cliente.

# para abrir o servidor, você precisa transformar um localhost em público utilizando ngrok, basta baixar o executável do ngrok, autorizar com seu auth token
# fornecido pelo site, e quando autorizado, basta digitar "ngrok tcp 8221"  (8221 é a porta que o servidor está utilizando da sua máquina, caso deseje alterar a porta
# altere também dentro do script "server.py" e mude quando for iniciar o ngrok.
# uma vez iniciado, o ngrok vai gerar um "fowarding link" parecido com tcp://4.tcp.ngrok.io:16738  você vai precisar descobrir o ip do servidor do ngrok que está
# por trás desse link, para isso, basta digitar no cmd "ping 4.tcp.ngrok.io" que vai retornar o ip da máquina. Logo em seguida você deve fazer upload da porta que
# se encontra no link acima e o ip encontrado, exemplo: "13.59.15.185 13710"  com espaço entre os dois.
# feito isso, com ngrok ativo, ip e portas publicados, basta rodar o server.py que todos os clientes que estão rodando o cliente.py irão se conectar ao servidor
# assim que a conexão for estabelecida com todos os clientes, o servidor.py mostrará um menu com todos os clientes disponíveis para controle de cmd
# basta digitar o número correspondente do cliente, e aparecerá um "$" apartir daí tudo que você digitar será um comando na máquina do cliente.
# caso queira "sair" desse cliente e ir para outro, basta digitar "leave"
# a lista de clientes aparecerá novamente.
# comandos durante o menu:
# [free] liberta todos os clientes, parando de executar o cliente.py nas máquinas.
# [fim, finish, end] encerra o servidor mas os clientes continuam tentando se reconectar para uma futura nova conexão
# [reload] atualiza a lista de clientes conectados



# esse documento é privado e não será publicado, também não foi feito com fins maliciosos, apenas de estudo.
