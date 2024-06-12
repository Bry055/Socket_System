import socket

HOST = 'localhost'
PORT = 5000

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
        print(f"Tentando conectar ao servidor em {HOST}:{PORT}")
        c.connect((HOST, PORT))
        print("Conectado ao servidor")

        while True:
            server_message = c.recv(1024).decode()
            print(server_message)
            if "Escolha uma opção" in server_message:
                option_user = input()
                c.sendall(option_user.encode())
                option_user = int(option_user)
                if option_user == 2:
                    break
            else:
                user_input = input()
                c.sendall(user_input.encode())
except Exception as e:
    print(f"Ocorreu um erro: {e}")
