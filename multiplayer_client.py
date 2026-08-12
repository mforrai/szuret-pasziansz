# -*- coding: utf-8 -*-
"""Minimal synchronous WebSocket client for the Cloudflare multiplayer coordinator."""

import json
from urllib.parse import quote

import websocket


class MultiplayerClient:
    def __init__(self, base_url, room_code, player_name, host=False, timeout=30):
        base_url = base_url.rstrip('/')
        if base_url.startswith('https://'):
            base_url = 'wss://' + base_url[len('https://'):]
        elif base_url.startswith('http://'):
            base_url = 'ws://' + base_url[len('http://'):]

        self.url = (
            f"{base_url}/room/{quote(room_code.upper())}"
            f"?name={quote(player_name)}&host={'1' if host else '0'}"
        )
        self.ws = websocket.create_connection(self.url, timeout=timeout)

    def close(self):
        self.ws.close()

    def send(self, message_type, **payload):
        message = {'type': message_type}
        message.update(payload)
        self.ws.send(json.dumps(message, ensure_ascii=False))

    def receive(self):
        raw = self.ws.recv()
        if not raw:
            return None
        return json.loads(raw)

    def start_game(self):
        self.send('start_game')

    def ready(self):
        self.send('ready')

    def peek(self):
        self.send('peek')

    def send_round_score(self, score):
        self.send('round_score', score=int(score))

    def send_final_score(self, score):
        self.send('final_score', score=int(score))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Szüret multiplayer connection tester')
    parser.add_argument('url', help='Worker URL, e.g. https://szuret-multiplayer.example.workers.dev')
    parser.add_argument('room', help='Room code')
    parser.add_argument('name', help='Player name')
    parser.add_argument('--host', action='store_true')
    args = parser.parse_args()

    client = MultiplayerClient(args.url, args.room, args.name, args.host)
    print('Connected. Incoming messages:')
    try:
        while True:
            print(json.dumps(client.receive(), ensure_ascii=False, indent=2))
    except KeyboardInterrupt:
        client.close()
