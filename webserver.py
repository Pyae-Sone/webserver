import socket
import os
from fileupload import upload_file
import logging
from mime import MimeTypes

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    ip = '0.0.0.0'
    port = 5554
    client_count = 0
    uploaded_files = []
    logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    s.listen(50)
    print(f"Server is established on host:{ip} and port:{port}.")

    while True:
        client, c_adds = s.accept()
        logging.info(f"Connection from {c_adds}")
        client_count += 1
        print(f'New client connected. There are now {client_count} clients connected.')
        request = client.recv(1024).decode()
        if not request:
            continue

        headers = request.split('\n')
        if len(headers) < 2:
            continue

        filename = headers[0].split()[1]
        file_extension = os.path.splitext(filename)[1]
        mime_type = MimeTypes.get(file_extension, 'application/octet-stream')

        if filename == '/':
            filename = 'index.html' 
        else:
            filename = filename[1:]

        try:
            www = open(filename, 'rb')
            content = www.read()
            www.close()

            response = f'HTTP/1.1 200 OK\nContent-Type: {mime_type}\n\n'.encode() + content

        except FileNotFoundError:
            file = open('404.html')
            error = file.read()
            file.close()
            response = 'HTTP/1.0 404 Not Found\n\n ' + error

        client.sendall(response.encode())
        client.close()
        client_count -= 1
        print(f'Client disconnected. There are now {client_count} clients connected.')

    s.close()