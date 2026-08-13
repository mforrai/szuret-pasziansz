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


def read_key():
    """Read and return one key without requiring Enter."""
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


def show_menu():
    clear_screen()
    print("────────────────────────────────────────────────────────────────────────")
    print("                              Szüret-CLI")
    print("────────────────────────────────────────────────────────────────────────")
    print()
    print("  1. Single player")
    print("  2. Multiplayer")
    print()
    print("  0. Kilépés")
    print()
    print("Választás [1/2/0]: ", end="", flush=True)


def main():
    while True:
        show_menu()
        try:
            choice = read_key().lower()
        except KeyboardInterrupt:
            clear_screen()
            return

        if choice in {"1", "s"}:
            run_script("szuret.py")
            continue

        if choice in {"2", "m"}:
            run_script("multiplayer_game.py")
            continue

        if choice in {"0", "q"}:
            clear_screen()
            return


if __name__ == "__main__":
    main()
