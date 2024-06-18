import socket
import threading
import subprocess
import os

HOST = 'localhost'
PORT = 5000

def obter_ultimo_id(name_file):
    try:
        with open(name_file, 'r') as arquivo:
            linhas = arquivo.readlines()
            if linhas:
                for linha in reversed(linhas):
                    if linha.startswith("ID:"):
                        ultimo_id = int(linha.split(':')[1].strip())
                        return ultimo_id
            return 0
    except FileNotFoundError:
        return 0

def handle_client(conn, addr):
    print(f"Conectado por {addr}")
    conn.sendall("Olá, seja bem vindo a VLTech Informática!\n Pressione Enter\n".encode())

    while True:
        conn.sendall("1 - Realizar Orçamento\n2 - Sair\nEscolha uma opção: ".encode())
        option_user = conn.recv(1024).decode().strip()

        if option_user == '1':
            last_id = obter_ultimo_id('users.txt')
            new_id = last_id + 1

            conn.sendall("Insira seu nome: ".encode())
            name_user = conn.recv(1024).decode().strip()

            conn.sendall("Insira Seu Telefone: ".encode())
            tel_user = conn.recv(1024).decode().strip()

            with open('users.txt', 'a') as arquivo:
                arquivo.write(f"ID: {new_id}\n")
                arquivo.write(f"Nome: {name_user}\n")
                arquivo.write(f"Telefone: {tel_user}\n")
                arquivo.write("\n")

            conn.sendall("Cadastro realizado com sucesso!\n\nSelecione o que deseja fazer:\n1 - Manutenção de Smartphones\n2 - Manutenção de Computadores\n".encode())
            get_manutencao = conn.recv(1024).decode().strip()

            if get_manutencao == '1':
                id_manutencao = obter_ultimo_id('manutencao.txt')
                id_smart = id_manutencao + 1

                conn.sendall("Qual o modelo de seu smartphone?\n".encode())
                smartphone = conn.recv(1024).decode().strip()

                conn.sendall("Descreva seu problema em poucas palavras\n".encode())
                problem = conn.recv(1024).decode().strip()

                with open('manutencao.txt', 'a') as arquivo:
                    arquivo.write("Tipo: Smartphone\n")
                    arquivo.write(f"ID: {id_smart}\n")
                    arquivo.write(f"Nome: {name_user}\n")
                    arquivo.write(f"Telefone: {tel_user}\n")
                    arquivo.write(f"Modelo Smartphone: {smartphone}\n")
                    arquivo.write(f"Descricao do Problema: {problem}\n")
                    arquivo.write("\n")

                conn.sendall("Entraremos em contato em instantes!\nVolte sempre!\n Pressione Enter para inserir novo orçamento ou digite 'exit' para sair\n".encode())

            elif get_manutencao == '2':
                conn.sendall("1 - Computador de mesa/ Desktop\n2 - Computador portátil/ Notebook\n".encode())
                pctype = conn.recv(1024).decode().strip()

                tipo_pc = "Desktop" if pctype == '1' else "Notebook Portátil" if pctype == '2' else "Nao informado"

                id_manutencao = obter_ultimo_id('manutencao.txt')
                id_pc = id_manutencao + 1

                conn.sendall("Qual a marca de seu computador?\n".encode())
                pc = conn.recv(1024).decode().strip()

                conn.sendall("Descreva seu problema em poucas palavras\n".encode())
                problem = conn.recv(1024).decode().strip()

                with open('manutencao.txt', 'a') as arquivo:
                    arquivo.write(f"Tipo: Computador\n")
                    arquivo.write(f"ID: {id_pc}\n")
                    arquivo.write(f"Nome: {name_user}\n")
                    arquivo.write(f"Telefone: {tel_user}\n")
                    arquivo.write(f"Marca Computador: {pc}\n")
                    arquivo.write(f"Descricao do Problema: {problem}\n")
                    arquivo.write("\n")

                conn.sendall("Entraremos em contato em instantes!\nVolte sempre!\n Pressione Enter para inserir novo orçamento ou digite 'exit' para sair\n".encode())

        elif option_user == '2' or option_user.lower() == 'exit':
            conn.sendall("Obrigado!\n".encode())
            conn.close()
            abrir_arquivo_apos_termino()
            break
        else:
            conn.sendall("Opção não encontrada\n".encode())

        # Após o orçamento, verificar se o usuário deseja continuar ou sair
        post_process(conn)

    conn.close()
    print(f"Conexão fechada por {addr}")

def post_process(conn):
    additional_input = conn.recv(1024).decode().strip()
    if additional_input.lower() == 'exit':
        conn.sendall("Obrigado!\n".encode())
        conn.close()
        abrir_arquivo_apos_termino()
    else:
        conn.sendall("Continuando...\n".encode())

def abrir_arquivo_apos_termino():
    if os.path.exists('manutencao.txt') and os.stat('manutencao.txt').st_size == 0:
        subprocess.run(['notepad', 'manutencao_backup.txt'])
    else:
        subprocess.run(['notepad', 'manutencao.txt'])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor iniciado e aguardando conexões...")

    try:
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Servidor encerrado.")
    finally:
        abrir_arquivo_apos_termino()
