#!/usr/bin/env python3

import game
from core import Player

import argparse

def main():
    # Parse arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('--players', '-p', type=int, default=3)
    parser.add_argument('--log', '-l', action='store_true')
    parser.add_argument('--replay', '-r', action='store_true')

    args = parser.parse_args()

    player_names = [ "Costas", "Cam", "Jeff", "Evan", "Alex" ]

    if not 3 <= args.players <= 5:
        print("Invalid number of players requested ({}); " + \
              "must be between 3 and 5 inclusive".format(args.players))
        sys.exit(1)
    assert 3 <= len(player_names) <= 5

    players = [ Player(name, i + 1) for i, name in enumerate(player_names[:args.players]) ]

    g = game.Game(args.log, args.replay)
    success = map(g.add, players)
    assert all(success)

    try:
        g.start()
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
