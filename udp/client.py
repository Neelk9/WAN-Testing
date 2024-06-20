import socket
import time

def send_udp_packet(proxy_ip, port):
    message = b'Hello, server!'
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start_time = time.time()
    client_socket.sendto(message, (proxy_ip, port))
    client_socket.close()
    return start_time

proxy_ip = "Proxy IP"
proxy_port = 12345
send_udp_packet(proxy_ip, proxy_port)
