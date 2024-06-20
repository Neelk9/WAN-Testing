import pyshark
import time

PROXY_SERVER_IP = ""  # Proxy servers IP

def analyze_packet(packet):
    try:
        if 'quic' in packet:
            if packet.ip.src == PROXY_SERVER_IP:
                rtt = packet.sniff_timestamp - CLIENT_START_TIME
                print(f"Success! Round-trip time: {rtt} seconds")
                print(f"Packet details: {packet}")
                return True
    except AttributeError:
        pass
    return False

def capture_and_analyze():

    capture = pyshark.LiveCapture(interface='any', display_filter='quic')

    for packet in capture.sniff_continuously():
        print(f'Packet captured: {packet}')

        if analyze_packet(packet):
            break

if __name__ == '__main__':
    capture_and_analyze()
