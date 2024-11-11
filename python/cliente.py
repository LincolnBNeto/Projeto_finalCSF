import socket as sock
import threading


def recebe_mensagens(socket_cliente):
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            if mensagem:
                print(mensagem)
            else:
                break
        except:
            break

#127.0.0.1
HOST = '172.20.10.3'
PORTA = 9999
socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)


socket_cliente.connect((HOST, PORTA))
print(5*"-" + "CHAT INICIADO" + 5*"-")
print(2*"-" + "Digite @ para mandar uma mensagem pessoal" + 2*"-")
print(3*"-" + "Digite /sair para sair" + 3*"-")
print()


nome = input("Informe seu nome para entrar no chat: ")
socket_cliente.sendall(nome.encode())


thread_recebe = threading.Thread(target=recebe_mensagens, args=(socket_cliente,))
thread_recebe.start()


while True:
    mensagem = input('')
    if mensagem.lower() == '/sair':
        socket_cliente.close()
        break
    else:
        socket_cliente.sendall(mensagem.encode())
