import socket as sock
import threading


lista_clientes = []


def recebe_dados(sock_cliente, endereco):
    nome = sock_cliente.recv(50).decode()
    lista_clientes.append((sock_cliente, nome))  
    print(f"Conexão bem sucedida com {nome} via endereço: {endereco}")
    

    broadcast(f"O usuário {nome} entrou no chat.", sock_cliente)

    while True:
        try:
            mensagem = sock_cliente.recv(1024).decode()

            if mensagem:
                
                if mensagem.startswith('@'):
                    try:
                        
                        nome_destinatario, conteudo_mensagem = mensagem[1:].split(' ', 1)
                        if nome_destinatario:  
                            unicast(f"{nome} = {conteudo_mensagem}", nome_destinatario)
                        else:
                            sock_cliente.send("Formato de mensagem incorreto. Use @nome mensagem.".encode())
                    except ValueError:
                        sock_cliente.send("Formato de mensagem incorreto. Use @nome mensagem.".encode())
                else:
                    
                    print(f"{nome} = {mensagem}")
                    broadcast(f"{nome} = {mensagem}", sock_cliente)
            else:
                remover(sock_cliente)
                break
        except:
            remover(sock_cliente)
            break


def broadcast(mensagem, cliente_excluido=None):
    for sock_cliente, _ in lista_clientes:
        if sock_cliente != cliente_excluido:  
            try:
                sock_cliente.send(mensagem.encode())
            except:
                remover(sock_cliente)


def unicast(mensagem, nome_destinatario):
    for sock_cliente, nome in lista_clientes:
        if nome == nome_destinatario:  
            try:
                sock_cliente.send(mensagem.encode())
            except:
                remover(sock_cliente)
            return

    for sock_cliente, nome in lista_clientes:
        if nome == nome_destinatario:
            sock_cliente.send(f"Usuário {nome_destinatario} não encontrado.".encode())


def remover(sock_cliente):
    for cliente in lista_clientes:
        if cliente[0] == sock_cliente:
            lista_clientes.remove(cliente)
            sock_cliente.close()
            print(f"{cliente[1]} desconectado.")
            broadcast(f"O usuário {cliente[1]} saiu do chat.")
            break
#127.0.0.1
HOST = '172.20.10.3'
PORTA = 9999


sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
sock_server.bind((HOST, PORTA))
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")


while True:
    sock_conn, ender = sock_server.accept()
    thread_cliente = threading.Thread(target=recebe_dados, args=(sock_conn, ender))
    thread_cliente.start()
