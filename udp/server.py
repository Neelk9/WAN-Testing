import socket
import time

def udp_server(destination_ip, destination_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((destination_ip, destination_port))
    
    while True:
        data, addr = server_socket.recvfrom(1024)
        if data:
            receive_time = time.time()
            print(f"Packet received. Time: {receive_time}")
            break
    server_socket.close()

destination_ip = "Destination IP"
destination_port = 12345
udp_server(destination_ip, destination_port)
