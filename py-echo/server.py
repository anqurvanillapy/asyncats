#!/usr/bin/env python3

"""\
# server.py

Async/await in tasks and coroutines in Python 3.5 is decent for making a
simple message echoing server in socket programming. If more pragmatic
third-party packages could be accepted, `curio' and `h2/h11' may be my
prominent choices for low-level networking.
"""

from socket import *
import asyncio

async def server(addr, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
    sock.bind((addr, port))
    sock.listen(3)
    sock.setblocking(False)     # equivalent to sock.settimeout(0.0)
    print('Available on {0}:{1}'.format(addr, port))
    while True:
        conn, addr = await loop.sock_accept(sock)
        loop.create_task(conn_handler(conn, addr))


async def conn_handler(conn, addr):
    print('Connection from', addr)
    with conn:
        while True:
            data = await loop.sock_recv(conn, 1024)
            if not data: break
            await loop.sock_sendall(conn, bytes(data))
    print(addr, 'disconnected')


loop = asyncio.get_event_loop()
loop.create_task(server('localhost', 8080))
loop.run_forever()
