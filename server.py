import socket
SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5

def handle_request(client_connection):
    request = client_connection.recv(1024)
    print(request.decode())
    http_response=b"""HTTP/1.1 200 OK\n\nHello World!"""
    client_connection.sendall(http_response)

def serve_forever():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind(SERVER_ADDRESS)
    listen_sock.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port}'.format(port=PORT))
    
    while True:
        client_conn, _ = listen_sock.accept()
        handle_request(client_conn)
        client_conn.close()

if __name__ == '__main__':
    serve_forever()