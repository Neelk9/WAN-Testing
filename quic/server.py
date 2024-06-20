import argparse
import asyncio
import struct
from collections import defaultdict
from aioquic.asyncio import serve, QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import DatagramFrameReceived, StreamDataReceived, QuicEvent

class CounterHandler:
    def __init__(self, connection) -> None:
        self.connection = connection
        self.counters = defaultdict(int)

    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, StreamDataReceived):
            self.counters[event.stream_id] += len(event.data)
            if event.end_stream:
                response = str(self.counters[event.stream_id]).encode('ascii')
                self.connection.send_stream_data(event.stream_id, response, end_stream=True)
                del self.counters[event.stream_id]

class QuicServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = None

    def quic_event_received(self, event: QuicEvent):
        if self.handler is None:
            self.handler = CounterHandler(self._quic)
        self.handler.quic_event_received(event)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate')
    parser.add_argument('key')
    args = parser.parse_args()

    configuration = QuicConfiguration()
    configuration.load_cert_chain(args.certificate, args.key)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        serve(
            '0.0.0.0', 4433, configuration=configuration, create_protocol=QuicServerProtocol
        ))
    loop.run_forever()
