import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.connection import END_STATES
import time

async def quic_client(proxy_ip, proxy_port):
    configuration = QuicConfiguration(is_client=True)
    configuration.verify_mode = False

    start_time = time.time()
    async with connect(proxy_ip, proxy_port, configuration=configuration) as connection:
        stream_id = connection.get_next_available_stream_id()
        connection.send_stream_data(stream_id, b'Hello, server!', end_stream=True)
        await connection.wait_closed()
    return time.time() - start_time

loop = asyncio.get_event_loop()
proxy_ip = "Proxy IP"
proxy_port = 4433
loop.run_until_complete(quic_client(proxy_ip, proxy_port))
