# -*- coding: utf-8 -*-
"""Playable multiplayer mode for Szüret using the Cloudflare coordinator.

This is intentionally kept separate from the legacy single-player loop for now.
It reuses the existing drawing and scoring functions from szuret.py without
executing its intro() entry point.
"""

import argparse
import copy
from pathlib import Path

from multiplayer_client import MultiplayerClient


WORKER_URL = "https://szuret-multiplayer.legacynotes-fm.workers.dev"


def load_legacy_game():
    """Load definitions from szuret.py but skip the final intro() startup."""
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


def wait_for(client, wanted, show_status=True):
    """Receive messages until one of the requested message types arrives."""
    if isinstance(wanted, str):
        wanted = {wanted}
    else:
        wanted = set(wanted)

    while True:
        message = client.receive()
        if message is None:
            raise ConnectionError("A kapcsolat megszakadt.")

        msg_type = message.get("type")
        if msg_type == "error":
            raise RuntimeError(message.get("message", "Ismeretlen szerverhiba"))

        if show_status and msg_type == "ready_state":
            ready = ", ".join(message.get("ready", [])) or "senki"
            total = message.get("total", "?")
            print(f"Kész játékosok: {ready} / összesen {total}")

        if msg_type in wanted:
            return message


def wait_for_lobby(client, is_host):
    players = []
    while True:
        msg = client.receive()
        if msg is None:
            raise ConnectionError("A kapcsolat megszakadt.")
        if msg.get("type") == "error":
            raise RuntimeError(msg.get("message", "Ismeretlen szerverhiba"))
        if msg.get("type") == "lobby":
            players = msg.get("players", [])
            print("\nLobby:")
            for p in players:
                suffix = " (host)" if p.get("host") else ""
                print(f" - {p.get('name')}{suffix}")
            if is_host and len(players) >= 2:
                input("\nLegalább két játékos csatlakozott. ENTER: játék indítása...")
                client.start_game()
                return
        if not is_host and msg.get("type") == "game_started":
            return msg


def show_farm_splash(ns, round_no, farm):
    """Show the newly active farm before the first road card of the round."""
    ns["kepernyo_torles"]()
    ns["eredmeny"](round_no)
    print(f"{round_no}. birtok: {farm}")
    ns["birtokrajz"](farm)
    input("ENTER: kör indítása...")
    ns["kepernyo_torles"]()


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


def place_or_peek(ns, client, matrix, farm, card, round_no, peek_used, yellow_count):
    ns["kepernyo_torles"]()
    ns["eredmeny"](round_no)
    print(f"{round_no}. birtok: {farm}")
    ns["rajz"](matrix, ns["oszlop"], ns["sor"])
    card_ascii(ns, card)

    print(f"Kihúzott sárga utak száma: {yellow_count}/4")

    x_farm, y_farm = ns["birtok_poziciok"][farm]
    current = ns["zold_lanc"](matrix, x_farm, y_farm) + ns["piros_lanc"](matrix, x_farm, y_farm)
    print(f"Várható pontok a körben: {current}")

    while True:
        answer = input("Hová helyezed az utat? (pl. C3, vagy BIRTOK): ").strip()

        if ns["check"](answer) == 1:
            col_name = answer[:1].upper()
            row_no = int(answer[-1:])
            y = ns["oszlopok"].index(col_name)
            x = row_no - 1
            if matrix[x][y][:4] != [0, 0, 0, 0]:
                print("A megadott mezőn már van út!")
                continue
            matrix[x][y][:4] = card[:4]

            # Azonnal mutassuk meg a frissen lerakott utat.
            ns["kepernyo_torles"]()
            ns["eredmeny"](round_no)
            print(f"{round_no}. birtok: {farm}")
            ns["rajz"](matrix, ns["oszlop"], ns["sor"])
            print(f"Kihúzott sárga utak száma: {yellow_count}/4")
            return peek_used

        if answer.lower() in ("birtok", "farm"):
            if peek_used:
                print("Ebben a körben már megnézted a következő birtokot.")
                continue
            client.peek()
            result = wait_for(client, "peek_result", show_status=False)
            ns["kepernyo_torles"]()
            ns["eredmeny"](round_no)
            print(f"{round_no}. birtok: {farm}")
            print("A BIRTOK akció miatt az aktuális útkártyát nem rakod le.")
            print(f"Következő birtok: {result['farm']}")
            ns["birtokrajz"](result["farm"])
            input("ENTER: folytatás...")
            return True

        print("Érvénytelen parancs.")


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
    zero_penalty = ns["resultkor"][1:6].count(0) * -5
    total = farm_total + green_castle + red_castle + zero_penalty
    return {
        "farm_total": farm_total,
        "green_castle": green_castle,
        "red_castle": red_castle,
        "zero_penalty": zero_penalty,
        "total": total,
    }


def run_game(url, room, name, host):
    ns = load_legacy_game()
    matrix = ns["alaphelyzet"](ns["sor"], ns["oszlop"])
    client = MultiplayerClient(url, room, name, host=host)

    try:
        connected = wait_for(client, "connected", show_status=False)
        actual_host = bool(connected.get("host"))
        print(f"Csatlakozva: {room.upper()} / {name}{' (host)' if actual_host else ''}")

        start_msg = wait_for_lobby(client, actual_host)
        if start_msg is None:
            start_msg = wait_for(client, "game_started", show_status=False)

        round_no = int(start_msg["round"])
        farm = start_msg["farm"]
        show_farm_splash(ns, round_no, farm)

        while True:
            ns["kihuzott_birtokok"][round_no] = farm
            peek_used = False

            while True:
                road = wait_for(client, ["road_revealed", "round_end"])
                if road["type"] == "round_end":
                    break

                card = road["card"]
                yellow_count = road.get("yellowCount", 0)
                peek_used = place_or_peek(
                    ns,
                    client,
                    matrix,
                    farm,
                    card,
                    round_no,
                    peek_used,
                    yellow_count,
                )

                client.ready()

            score = calculate_round_score(ns, matrix, farm, round_no)
            print(f"\n{farm} birtok pontszáma: {score}")
            client.send_round_score(score)

            results = wait_for(client, ["round_results", "request_final_score"])
            if results["type"] == "round_results":
                print("Forduló eredményei:")
                for item in results.get("scores", []):
                    print(f" - {item['name']}: {item['score']} pont")

            if round_no >= 5:
                if results["type"] != "request_final_score":
                    wait_for(client, "request_final_score")
                final = calculate_final_score(ns, matrix)
                print("\nSaját végeredmény:")
                print(f" Birtokok: {final['farm_total']}")
                print(f" Zöld kastély: {final['green_castle']}")
                print(f" Piros kastély: {final['red_castle']}")
                print(f" Nulla pontos körök: {final['zero_penalty']}")
                print(f" ÖSSZESEN: {final['total']}")
                client.send_final_score(final["total"])

                finished = wait_for(client, "game_finished")
                print("\nVÉGEREDMÉNY")
                for index, item in enumerate(finished.get("ranking", []), start=1):
                    print(f" {index}. {item['name']}: {item['score']} pont")
                winners = ", ".join(finished.get("winners", []))
                print(f"Győztes: {winners}")
                return

            next_round = wait_for(client, "farm_revealed")
            round_no = int(next_round["round"])
            farm = next_round["farm"]
            show_farm_splash(ns, round_no, farm)

    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description="Szüret multiplayer")
    parser.add_argument("room", help="Szobakód")
    parser.add_argument("name", help="Játékos neve")
    parser.add_argument("--host", action="store_true", help="Új játék hostja")
    parser.add_argument("--url", default=WORKER_URL, help="Cloudflare Worker URL")
    args = parser.parse_args()
    run_game(args.url, args.room, args.name, args.host)


if __name__ == "__main__":
    main()
