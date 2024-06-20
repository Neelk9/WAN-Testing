import socket
import time

def tcp_server(destination_ip, destination_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((destination_ip, destination_port))
    server_socket.listen(1)
    
    conn, addr = server_socket.accept()
    receive_time = time.time()
    data = conn.recv(1024)
    if data:
        print(f"Packet received. Time: {receive_time}")
    conn.close()
    server_socket.close()

destination_ip = "Destination IP"
destination_port = 12345
tcp_server(destination_ip, destination_port)
