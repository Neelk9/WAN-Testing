import proxies.pproxy as pproxy
import asyncio

server = pproxy.Server('http+socks4+socks5://:8080/')  # HTTP, SOCKS4, and SOCKS5 on port 8080
udp_relay = pproxy.Connection('udp://:53')  # UDP relay on port 53 (DNS)
tcp_relay = pproxy.Connection('tcp://:80')  # TCP relay on port 80 (HTTP)

async def main():
    await server.start_server(relays=[udp_relay, tcp_relay])

if __name__ == '__main__':
    asyncio.run(main())
