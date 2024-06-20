import socket
import time

def send_tcp_packet(proxy_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_time = time.time()
    client_socket.connect((proxy_ip, port))
    message = b'Hello, server!'
    client_socket.sendall(message)
    client_socket.close()
    return start_time

proxy_ip = "Proxy IP"
proxy_port = 12345
send_tcp_packet(proxy_ip, proxy_port)
