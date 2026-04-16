#!/usr/bin/env python3
"""
Secure WebSocket server (wss://) using the `websockets` library + TLS.
Install: pip install websockets

TLS certificate setup (choose one):
  - Development: generate a self-signed cert (see below)
  - Production:  use a cert from Let's Encrypt or your CA

Generate a self-signed cert for local dev:
  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
    -days 365 -nodes -subj "/CN=localhost"
"""

import asyncio
import json
import logging
import signal
import ssl
from pathlib import Path
from websockets.server import serve, WebSocketServerProtocol

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# Track all connected clients
connected_clients: set[WebSocketServerProtocol] = set()

# --- TLS configuration ---
CERT_FILE = Path("cert.pem")   # Your TLS certificate
KEY_FILE  = Path("key.pem")    # Your private key
# CA_FILE = Path("ca.pem")     # Uncomment to require client certificates


def build_ssl_context() -> ssl.SSLContext:
    """Create and configure the server-side SSL context."""
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    if not CERT_FILE.exists() or not KEY_FILE.exists():
        raise FileNotFoundError(
            f"TLS cert/key not found ({CERT_FILE}, {KEY_FILE}).\n"
            "Generate one with:\n"
            "  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \\\n"
            "    -days 365 -nodes -subj '/CN=localhost'"
        )

    ctx.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    # Enforce modern TLS — disallow TLS 1.0 / 1.1
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2

    # Prefer server cipher order and use a secure set
    ctx.set_ciphers("ECDH+AESGCM:ECDH+CHACHA20:!aNULL:!MD5")

    # Uncomment to require clients to present a certificate (mTLS):
    # ctx.verify_mode = ssl.CERT_REQUIRED
    # ctx.load_verify_locations(cafile=CA_FILE)

    return ctx


async def broadcast(message: str, exclude: WebSocketServerProtocol | None = None) -> None:
    """Send a message to all connected clients, optionally excluding one."""
    targets = connected_clients - {exclude} if exclude else connected_clients
    if targets:
        await asyncio.gather(*[client.send(message) for client in targets])


async def handle_message(websocket: WebSocketServerProtocol, data: str) -> None:
    """Process an incoming message from a client."""
    try:
        payload = json.loads(data)
        logger.info("Received: %s", payload)

        # --- Your message handling logic goes here ---
        msg_type = payload.get("type")

        if msg_type == "echo":
            await websocket.send(json.dumps({"type": "echo", "data": payload.get("data")}))

        elif msg_type == "broadcast":
            await broadcast(
                json.dumps({"type": "broadcast", "data": payload.get("data")}),
                exclude=websocket,
            )

        else:
            await websocket.send(json.dumps({"type": "error", "message": f"Unknown type: {msg_type}"}))

    except json.JSONDecodeError:
        await websocket.send(json.dumps({"type": "error", "message": "Invalid JSON"}))


async def handler(websocket: WebSocketServerProtocol) -> None:
    """Lifecycle handler for each client connection."""
    client_id = id(websocket)
    connected_clients.add(websocket)
    logger.info("Client connected: %s (total: %d)", client_id, len(connected_clients))

    try:
        await websocket.send(json.dumps({"type": "welcome", "message": "Connected to secure WebSocket server"}))

        async for message in websocket:
            await handle_message(websocket, message)

    except Exception as e:
        logger.warning("Client %s error: %s", client_id, e)

    finally:
        connected_clients.discard(websocket)
        logger.info("Client disconnected: %s (total: %d)", client_id, len(connected_clients))


async def main() -> None:
    host = "localhost"
    port = 8765
    ssl_context = build_ssl_context()

    stop = asyncio.get_event_loop().create_future()

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set_result, None)

    async with serve(handler, host, port, ssl=ssl_context) as server:
        logger.info("Secure WebSocket server listening on wss://%s:%d", host, port)
        await stop
        logger.info("Shutting down...")
        server.close()
        await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())