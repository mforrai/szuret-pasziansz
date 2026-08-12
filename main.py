# -*- coding: utf-8 -*-
"""Common launcher for Szüret single-player and multiplayer modes."""

import os
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def run_script(filename):
    """Run one game mode with the same Python interpreter."""
    script = BASE_DIR / filename
    try:
        subprocess.run([sys.executable, str(script)], cwd=str(BASE_DIR), check=False)
    except KeyboardInterrupt:
        # Ctrl+C inside a game mode returns to the launcher when possible.
        print()


def show_menu():
    clear_screen()
    print("────────────────────────────────────────────────────────────────────────")
    print("                              SZÜRET")
    print("────────────────────────────────────────────────────────────────────────")
    print()
    print("  1. Single player")
    print("  2. Multiplayer")
    print()
    print("  0. Kilépés")
    print()


def main():
    while True:
        show_menu()
        choice = input("Választás [1/2/0]: ").strip().lower()

        if choice in {"1", "s", "single", "singleplayer", "single player"}:
            run_script("szuret.py")
            continue

        if choice in {"2", "m", "multi", "multiplayer"}:
            run_script("multiplayer_game.py")
            continue

        if choice in {"0", "q", "quit", "exit", "kilepes", "kilépés"}:
            clear_screen()
            return


if __name__ == "__main__":
    main()
