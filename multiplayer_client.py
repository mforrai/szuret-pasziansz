# -*- coding: utf-8 -*-
"""Minimal synchronous WebSocket client for the Cloudflare multiplayer coordinator."""

import json
import threading
from urllib.parse import quote

import websocket


class MultiplayerClient:
    def __init__(self, base_url, room_code, player_name, host=False, connect_timeout=30):
        base_url = base_url.rstrip('/')
        if base_url.startswith('https://'):
            base_url = 'wss://' + base_url[len('https://'):]
        elif base_url.startswith('http://'):
            base_url = 'ws://' + base_url[len('http://'):]

        self.url = (
            f"{base_url}/room/{quote(room_code.upper())}"
            f"?name={quote(player_name)}&host={'1' if host else '0'}"
        )

        self.ws = websocket.create_connection(self.url, timeout=connect_timeout)
        self.ws.settimeout(None)

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

    def receive_timeout(self, timeout):
        """Receive one message, returning None on an idle timeout."""
        self.ws.settimeout(timeout)
        try:
            raw = self.ws.recv()
            if not raw:
                return None
            return json.loads(raw)
        except websocket.WebSocketTimeoutException:
            return None
        finally:
            self.ws.settimeout(None)

    def start_game(self):
        self.send('start_game')

    def ready(self, action='place', card_index=None):
        payload = {'action': action}
        if card_index is not None:
            payload['cardIndex'] = int(card_index)
        self.send('ready', **payload)

    def undo(self, card_index):
        self.send('undo', cardIndex=int(card_index))

    def peek(self):
        self.send('peek')

    def send_round_score(self, score):
        self.send('round_score', score=int(score))

    def send_final_score(self, score):
        self.send('final_score', score=int(score))


def print_help():
    print(
        "Commands:\n"
        "  start              host starts the game\n"
        "  ready              mark current road card as resolved\n"
        "  undo <card>        undo a still-open placement\n"
        "  peek               use the BIRTOK action\n"
        "  score <n>          submit round score\n"
        "  final <n>          submit final score\n"
        "  help               show this help\n"
        "  quit               disconnect\n"
    )


def receiver_loop(client, stop_event):
    while not stop_event.is_set():
        try:
            message = client.receive()
            if message is None:
                break
            print("\n<<<", json.dumps(message, ensure_ascii=False, indent=2))
            print("> ", end="", flush=True)
        except Exception as exc:
            if not stop_event.is_set():
                print(f"\nConnection closed: {exc}")
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Szüret multiplayer connection tester')
    parser.add_argument('url', help='Worker URL, e.g. https://szuret-multiplayer.example.workers.dev')
    parser.add_argument('room', help='Room code')
    parser.add_argument('name', help='Player name')
    parser.add_argument('--host', action='store_true')
    args = parser.parse_args()

    client = MultiplayerClient(args.url, args.room, args.name, args.host)
    stop_event = threading.Event()
    receiver = threading.Thread(target=receiver_loop, args=(client, stop_event), daemon=True)
    receiver.start()

    print(f"Connected to room {args.room.upper()} as {args.name}{' (host)' if args.host else ''}.")
    print_help()

    try:
        while True:
            command = input('> ').strip()
            if not command:
                continue
            if command == 'start':
                client.start_game()
            elif command == 'ready':
                client.ready()
            elif command.startswith('undo '):
                client.undo(int(command.split(maxsplit=1)[1]))
            elif command == 'peek':
                client.peek()
            elif command.startswith('score '):
                client.send_round_score(int(command.split(maxsplit=1)[1]))
            elif command.startswith('final '):
                client.send_final_score(int(command.split(maxsplit=1)[1]))
            elif command == 'help':
                print_help()
            elif command in ('quit', 'exit'):
                break
            else:
                print('Unknown command. Type help.')
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        stop_event.set()
        client.close()
