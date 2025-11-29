#!/usr/bin/env python3
"""
terminal_game.py

Thin wrapper to run the Lost Scroll of Eldoria adventure game.
This is a Codédex checkpoint project.
"""

from codex_adventure import Game


if __name__ == "__main__":
    game = Game(sleep=0.8)
    game.run_cli()
