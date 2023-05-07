import socket
import os

# fungsi untuk menangani request yang masuk
def handle_request(request):
    headers = request.split('\n')
    filename = headers[0].split()[1]
    if filename == '/':
        filename = '/index.html'

    try:
        with open('.' + filename, 'rb') as fin:
            content = fin.read()
        response = 'HTTP/1.0 200 OK\n\n'.encode() + content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'.encode()

    return response

# definisikan host dan port
HOST = 'localhost'
PORT = 8080

# buat socket dan pasang ke host dan port tertentu
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f'Listening on port {PORT} ...')

while True:
    # tunggu koneksi dari client
    client_connection, client_address = server_socket.accept()

    # terima request dari client
    request = client_connection.recv(1024).decode()
    print(request)

    # kirim response ke client
    response = handle_request(request)
    client_connection.sendall(response)

    # tutup koneksi
    client_connection.close()

# tutup socket
server_socket.close()
