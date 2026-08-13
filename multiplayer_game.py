# -*- coding: utf-8 -*-
"""Playable multiplayer mode for Szüret using the Cloudflare coordinator."""

import argparse
import copy
import json
import os
import secrets
import select
import string
import sys
from collections import deque
from pathlib import Path

from multiplayer_client import MultiplayerClient


WORKER_URL = "https://szuret-multiplayer.legacynotes-fm.workers.dev"
PROFILE_FILE = Path.home() / ".szuret_multiplayer.json"
ROOM_ALPHABET = string.ascii_uppercase + string.digits


def load_legacy_game():
    path = Path(__file__).with_name("szuret.py")
    source = path.read_text(encoding="utf-8")
    marker = "##############################################################################\n# \u00a0START"
    if marker not in source:
        marker = "##############################################################################\n#  START"
    if marker not in source:
        raise RuntimeError("Could not find START marker in szuret.py")
    source = source.split(marker, 1)[0]
    namespace = {"__name__": "szuret_legacy_multiplayer"}
    exec(compile(source, str(path), "exec"), namespace)
    namespace["kihuzott_birtokok"] = [None, None, None, None, None, None]
    namespace["resultkor"] = [None, None, None, None, None, None]
    return namespace


def load_saved_name():
    try:
        return json.loads(PROFILE_FILE.read_text(encoding="utf-8")).get("name", "")
    except Exception:
        return ""


def save_name(name):
    try:
        PROFILE_FILE.write_text(json.dumps({"name": name}, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def choose_player_name():
    saved = load_saved_name()
    prompt = f"Játékosnév [{saved}]: " if saved else "Játékosnév: "
    name = input(prompt).strip() or saved
    while not name:
        name = input("Játékosnév: ").strip()
    name = name[:32]
    save_name(name)
    return name


def read_key():
    """Read one key without requiring Enter on Windows, Linux and macOS."""
    if os.name == "nt":
        import msvcrt
        key = msvcrt.getwch()
    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    if key == "\x03":
        raise KeyboardInterrupt
    return key


def generate_room_code():
    return "".join(secrets.choice(ROOM_ALPHABET) for _ in range(8))


def choose_room():
    print("\nMULTIPLAYER")
    print("1. Új játék indítása")
    print("2. Csatlakozás meglévő játékhoz")
    print("Választás [1/2]: ", end="", flush=True)
    while True:
        choice = read_key()
        if choice == "1":
            room = generate_room_code()
            print(f"\n\nJÁTÉKSZÁM: {room}")
            print("Ezt a 8 karakteres kódot add meg a másik játékosnak.\n")
            return room, True
        if choice == "2":
            print()
            room = input("Játékszám: ").strip().upper()
            if len(room) == 8 and room.isalnum():
                return room, False
            print("A játékszám 8 alfanumerikus karakter legyen.")
            print("Választás [1/2]: ", end="", flush=True)


def wait_for(client, wanted, pending, show_status=True):
    if isinstance(wanted, str):
        wanted = {wanted}
    else:
        wanted = set(wanted)

    for index, message in enumerate(list(pending)):
        if message.get("type") in wanted:
            del pending[index]
            return message

    while True:
        message = client.receive()
        if message is None:
            raise ConnectionError("A kapcsolat megszakadt.")
        msg_type = message.get("type")
        if msg_type == "error":
            raise RuntimeError(message.get("message", "Ismeretlen szerverhiba"))
        if show_status and msg_type == "ready_state":
            continue
        if msg_type in wanted:
            return message
        pending.append(message)


def wait_for_lobby(client, is_host, pending, room):
    while True:
        msg = wait_for(client, ["lobby", "game_started"], pending, show_status=False)
        if msg.get("type") == "lobby":
            players = msg.get("players", [])
            print(f"\nJáték: {room}")
            print("Lobby:")
            for p in players:
                suffix = " (host)" if p.get("host") else ""
                print(f" - {p.get('name')}{suffix}")
            if is_host and len(players) >= 2:
                input("\nLegalább két játékos csatlakozott. ENTER: játék indítása...")
                client.start_game()
                return None
        elif not is_host:
            return msg


def print_game_header(room, name, round_no=None, farm=None, next_farm=None):
    left = f"Játék: {room} | Játékos: {name}"
    print(left)
    if round_no is not None and farm is not None:
        suffix = f" (Következő: {next_farm})" if next_farm else ""
        print(f"{round_no}. birtok: {farm}{suffix}")


def show_farm_splash(ns, room, name, round_no, farm):
    ns["kepernyo_torles"]()
    ns["eredmeny"](round_no)
    print_game_header(room, name, round_no, farm)
    ns["birtokrajz"](farm)


def card_ascii(ns, card):
    lap = copy.deepcopy(card)
    key = str(lap[:4]).replace(" ", "")
    drawing = ns["d"].get(key)
    if drawing is None:
        raise ValueError(f"Ismeretlen útkártya: {card}")
    if card[4] == 99:
        ns["laprajz_sarga"](drawing, 5)
    else:
        ns["laprajz"](drawing, 5)


def render_turn_screen(ns, matrix, room, name, farm, card, round_no, yellow_count,
                       next_farm=None, status=None, last_coord=None, undo_available=False):
    ns["kepernyo_torles"]()
    ns["eredmeny"](round_no)
    print_game_header(room, name, round_no, farm, next_farm)
    ns["rajz"](matrix, ns["oszlop"], ns["sor"])
    card_ascii(ns, card)
    print(f"Kihúzott sárga utak száma: {yellow_count}/4")
    x_farm, y_farm = ns["birtok_poziciok"][farm]
    current = ns["zold_lanc"](matrix, x_farm, y_farm) + ns["piros_lanc"](matrix, x_farm, y_farm)
    print(f"Várható pontok a körben: {current}")
    if last_coord:
        print(f"Utolsó lerakás: {last_coord}")
    if undo_available:
        print("VISSZA + ENTER: utolsó lerakás visszavonása")
    if status:
        print(status)


def place_or_peek(ns, client, pending, matrix, room, name, farm, card, round_no,
                  peek_used, yellow_count, next_farm):
    render_turn_screen(ns, matrix, room, name, farm, card, round_no, yellow_count, next_farm)
    while True:
        answer = input(ns["txt"]["where_road"][ns["nyelv"]]).strip()
        if ns["check"](answer) == 1:
            coord = answer[:1].upper() + answer[-1:]
            y = ns["oszlopok"].index(coord[0])
            x = int(coord[1]) - 1
            if matrix[x][y][:4] != [0, 0, 0, 0]:
                print("A megadott mezőn már van út!")
                continue
            matrix[x][y][:4] = card[:4]
            return {
                "action": "place",
                "coord": coord,
                "x": x,
                "y": y,
                "peek_used": peek_used,
                "next_farm": next_farm,
            }

        if answer.lower() in ("birtok", "farm"):
            if peek_used:
                print("Ebben a körben már megnézted a következő birtokot.")
                continue
            client.peek()
            result = wait_for(client, "peek_result", pending, show_status=False)
            next_farm = result["farm"]
            ns["kepernyo_torles"]()
            ns["eredmeny"](round_no)
            print_game_header(room, name, round_no, farm, next_farm)
            print("A BIRTOK akció miatt az aktuális útkártyát nem rakod le.")
            ns["birtokrajz"](next_farm)
            return {
                "action": "peek",
                "coord": None,
                "peek_used": True,
                "next_farm": next_farm,
            }

        print("Érvénytelen parancs.")


def wait_for_undo_window(ns, client, pending, matrix, room, name, farm, card, round_no,
                         yellow_count, next_farm, action, player_id, card_index):
    """Allow VISSZA while nobody else has completed the active card."""
    coord = action["coord"]
    render_turn_screen(
        ns, matrix, room, name, farm, card, round_no, yellow_count, next_farm,
        status="Várakozás a többi játékosra...",
        last_coord=coord,
        undo_available=True,
    )

    while True:
        try:
            readable, _, _ = select.select([sys.stdin], [], [], 0)
        except Exception:
            readable = []
        if readable:
            command = sys.stdin.readline().strip().lower()
            if command in ("vissza", "undo"):
                client.undo(card_index)
                result = wait_for(client, "undo_result", pending, show_status=False)
                if result.get("accepted"):
                    x, y = action["x"], action["y"]
                    matrix[x][y][:4] = [0, 0, 0, 0]
                    return True
                render_turn_screen(
                    ns, matrix, room, name, farm, card, round_no, yellow_count, next_farm,
                    status="Visszavonás nem lehetséges: " + result.get("reason", "ismeretlen ok"),
                    last_coord=coord,
                    undo_available=False,
                )
                return False

        message = client.receive_timeout(0.15)
        if message is None:
            continue
        msg_type = message.get("type")
        if msg_type == "error":
            raise RuntimeError(message.get("message", "Ismeretlen szerverhiba"))
        if msg_type == "ready_state":
            other_ready = any(pid != player_id for pid in message.get("readyIds", []))
            if other_ready:
                render_turn_screen(
                    ns, matrix, room, name, farm, card, round_no, yellow_count, next_farm,
                    status="A másik játékos befejezte ezt az útkártyát. Visszavonás már nem lehetséges.",
                    last_coord=coord,
                    undo_available=False,
                )
                return False
            continue
        pending.append(message)
        if msg_type in ("road_revealed", "round_end"):
            return False


def calculate_round_score(ns, matrix, farm, round_no):
    x, y = ns["birtok_poziciok"][farm]
    score = int(ns["zold_lanc"](matrix, x, y)) + int(ns["piros_lanc"](matrix, x, y))
    previous = ns["resultkor"][round_no - 1]
    if previous is not None and score <= previous:
        score = 0
    ns["resultkor"][round_no] = score
    ns["kihuzott_birtokok"][round_no] = farm
    return score


def calculate_final_score(ns, matrix):
    farm_total = sum(ns["resultkor"][1:6])
    green_castle = ns["zold_lanc"](matrix, 0, 5)
    red_castle = ns["piros_lanc"](matrix, 6, 0)
    zero_count = ns["resultkor"][1:6].count(0)
    zero_penalty = zero_count * -5
    total = farm_total + green_castle + red_castle + zero_penalty
    return {
        "farm_total": farm_total,
        "green_castle": green_castle,
        "red_castle": red_castle,
        "zero_count": zero_count,
        "zero_penalty": zero_penalty,
        "total": total,
    }


def render_final_results(ns, matrix, room, name, final, ranking=None, winners=None, status=None):
    ns["kepernyo_torles"]()
    print_game_header(room, name)
    ns["rajz"](matrix, ns["oszlop"], ns["sor"])
    nyelv = ns["nyelv"]
    txt = ns["txt"]
    pont = txt["pont"][nyelv]
    birtok_label = txt["birtok"][nyelv]
    ns["teljessorszoveggel"]("szimpla", txt["results"][nyelv], "kozep", 1)
    ns["teljessor"]("dupla")
    for i in range(1, 6):
        f = ns["kihuzott_birtokok"][i]
        s = ns["resultkor"][i]
        print(f"{f} {birtok_label}:                       {str(s).zfill(2)}{pont}")
    ns["teljessor"]("szimpla")
    print(txt["every_birtok"][nyelv] + "               " + str(final["farm_total"]).zfill(3) + pont)
    ns["teljessor"]("szimpla")
    print(txt["green_castle"][nyelv] + "                 " + str(final["green_castle"]).zfill(2) + pont)
    print(txt["red_castle"][nyelv] + "                " + str(final["red_castle"]).zfill(2) + pont)
    ns["teljessor"]("szimpla")
    print(txt["zero_point_rounds"][nyelv] + " (" + str(final["zero_count"]) + txt["db"][nyelv] + "):   " + str(final["zero_penalty"]).zfill(2) + pont)
    ns["teljessor"]("dupla")
    assessment = ns["szoveges_ertekeles"](final["total"], nyelv)
    print(txt["total"][nyelv] + "                    " + str(final["total"]).zfill(3) + pont + " - " + assessment)
    ns["teljessor"]("dupla")
    if ranking is not None:
        ns["teljessorszoveggel"]("szimpla", "MULTIPLAYER RANGSOR", "kozep", 1)
        ns["teljessor"]("szimpla")
        for index, item in enumerate(ranking, start=1):
            marker = "  <-- TE" if item.get("name") == name else ""
            print(f" {index}. {item['name']}: {item['score']} pont{marker}")
        if winners:
            ns["teljessor"]("szimpla")
            print("Győztes: " + ", ".join(winners))
        ns["teljessor"]("dupla")
    if status:
        print(status)


def run_game(url, room, name, host):
    ns = load_legacy_game()
    matrix = ns["alaphelyzet"](ns["sor"], ns["oszlop"])
    client = MultiplayerClient(url, room, name, host=host)
    pending = deque()

    try:
        connected = wait_for(client, "connected", pending, show_status=False)
        player_id = connected.get("playerId")
        actual_host = bool(connected.get("host"))
        print(f"Csatlakozva: {room} / {name}{' (host)' if actual_host else ''}")
        start_msg = wait_for_lobby(client, actual_host, pending, room)
        if start_msg is None:
            start_msg = wait_for(client, "game_started", pending, show_status=False)

        round_no = int(start_msg["round"])
        farm = start_msg["farm"]
        next_farm = None
        show_farm_splash(ns, room, name, round_no, farm)

        while True:
            ns["kihuzott_birtokok"][round_no] = farm
            peek_used = False

            while True:
                road = wait_for(client, ["road_revealed", "round_end"], pending)
                if road["type"] == "round_end":
                    break

                card = road["card"]
                card_index = int(road.get("cardIndex", 0))
                yellow_count = road.get("yellowCount", 0)

                while True:
                    action = place_or_peek(
                        ns, client, pending, matrix, room, name, farm, card, round_no,
                        peek_used, yellow_count, next_farm,
                    )
                    peek_used = action["peek_used"]
                    next_farm = action["next_farm"]

                    if action["action"] == "peek":
                        client.ready(action="peek", card_index=card_index)
                        render_turn_screen(
                            ns, matrix, room, name, farm, card, round_no, yellow_count, next_farm,
                            status="BIRTOK akció: az aktuális út eldobva. Várakozás a többi játékosra...",
                        )
                        break

                    client.ready(action="place", card_index=card_index)
                    undone = wait_for_undo_window(
                        ns, client, pending, matrix, room, name, farm, card, round_no,
                        yellow_count, next_farm, action, player_id, card_index,
                    )
                    if undone:
                        continue
                    break

            score = calculate_round_score(ns, matrix, farm, round_no)
            print(f"\n{farm} birtok pontszáma: {score}")
            client.send_round_score(score)
            results = wait_for(client, ["round_results", "request_final_score"], pending)
            if results["type"] == "round_results":
                print("Forduló eredményei:")
                for item in results.get("scores", []):
                    print(f" - {item['name']}: {item['score']} pont")

            if round_no >= 5:
                if results["type"] != "request_final_score":
                    wait_for(client, "request_final_score", pending)
                final = calculate_final_score(ns, matrix)
                client.send_final_score(final["total"])
                render_final_results(ns, matrix, room, name, final, status="Várakozás a többi játékos végeredményére...")
                finished = wait_for(client, "game_finished", pending)
                render_final_results(
                    ns, matrix, room, name, final,
                    ranking=finished.get("ranking", []),
                    winners=finished.get("winners", []),
                )
                input("\nENTER: kilépés...")
                return

            input("\nENTER: következő birtok felfedése...")
            next_round = wait_for(client, "farm_revealed", pending)
            round_no = int(next_round["round"])
            farm = next_round["farm"]
            next_farm = None
            show_farm_splash(ns, room, name, round_no, farm)

    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description="Szüret multiplayer")
    parser.add_argument("--url", default=WORKER_URL, help="Cloudflare Worker URL")
    args = parser.parse_args()
    name = choose_player_name()
    room, host = choose_room()
    run_game(args.url, room, name, host)


if __name__ == "__main__":
    main()
