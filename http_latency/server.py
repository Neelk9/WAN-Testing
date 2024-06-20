from quart import Quart, request
import hypercorn.asyncio
import time

app = Quart(__name__)

@app.route('/')
async def home():
    receive_time = time.time()
    print(f"Packet received. Time: {receive_time}")
    return 'Hello, client!'

async def run():
    config = hypercorn.Config()
    config.bind = ["Destination IP:12345"]
    await hypercorn.asyncio.serve(app, config)

import asyncio
if __name__ == '__main__':
    asyncio.run(run())
