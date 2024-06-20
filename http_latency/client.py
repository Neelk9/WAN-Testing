from hyper import HTTP20Connection
import time

def send_http2_request(proxy_ip, port):
    conn = HTTP20Connection(proxy_ip, port)
    start_time = time.time()
    conn.request('GET', '/')
    response = conn.get_response()
    print(response.read())
    conn.close()
    return start_time

proxy_ip = "Proxy IP"
proxy_port = 12345
send_http2_request(proxy_ip, proxy_port)
