import socket
from fileupload import upload_file
import logging

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    ip = '0.0.0.0'
    port = 5554
    client_count = 0
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

        headers = request.split('\n')
        filename = headers[0].split()[1]

        if filename == '/':
            filename = 'index.html'
        elif filename == '/upload,html':
            u_content = 'upload.html'
            response = 'HTTP/1.0 200 OK\n\n ' + u_content.encode()
            client.sendall(response)

            filedata = b''

            while True:
                data = client.recv(1024)
                if not data:
                    break
                filedata += data
            upload_file(filedata)
            # Send response back to client
            response = 'HTTP/1.0 200 OK\n\nFile uploaded successfully'
            client.sendall(response.encode())
            client.close()
            continue


        try:
            www = open(filename)
            content = www.read()
            www.close()

            response = 'HTTP/1.0 200 OK\n\n ' + content

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