#!/usr/bin/env python

import game
from core import Player

import random
from math import ceil, log10
import os

# options : [ opts, ... ]
# question : string
def choose(options, question):
    max_digits = int(ceil(log10(len(options)+1)))
    for i, opt in enumerate(options):
        print "{:{}}: {}".format(i + 1, max_digits, opt)

    print

    selection = None
    while selection == None:
        inp = raw_input(question + "  ")

        # handle invalid input, determine which option
        try:
            selection = int(inp) - 1
            if not 0 <= selection < len(options):
                raise Exception()
        except Exception:
            print "Invalid input, please try again."
            selection = None
            continue

    return options[selection]

def challenge(players, player):
    for other in players:
        if player == other:
            continue

        challenge_inp = None
        while True:
            challenge_inp = raw_input("{}, would you like to challenge? (y/n) ".format(other))
            if challenge_inp == 'y':
                return other
            elif challenge_inp == 'n':
                break
            else:
                print "Invalid input, please try again"

def main():
    players = []
    player_names = [ "Costas", "Cam", "Jeff" ]
    for i, name in enumerate(player_names):
        players.append( Player(name, i + 1) )

    g = game.Game()
    map(g.add, players)

    return g.start()

if __name__ == "__main__":
    main()
