#!/usr/bin/env python

from core import *

import random
import sys

def clear_screen():
    sys.stdout.write("\x1b[2J")
    sys.stdout.write("\x1b[H")
    sys.stdout.flush()

class Game:
    actions = map(Action, [ Action.income, Action.foreign_aid, Action.coup, Action.tax, Action.assassinate, Action.steal, Action.swap ])

    def __init__(self):
        self.bank = 60
        self.game_over = False
        self.players = []
        self.cpi = -1 # current player index
        self.current = None
        self.status = ""

        self.deck = map(Role, [ Role.duke, Role.assassin, Role.captain, Role.ambassador, Role.contessa ] * 3)
        random.shuffle(self.deck)

    '''
    def active_players(self):
        return filter(self
    '''

    def add(self, player):
        if len(self.players) == 5:
            return False

        assert(len(self.deck) > 2)

        player.roles.extend( [self.deck.pop(), self.deck.pop()] )
        self.players.append(player)

        return True

    def prepare_player(self, player):
        clear_screen()

        if self.status != "":
            #print "=== Status Message ==="
            print self.status
            self.status = ""

        print "=== Game State ==="
        print self

        print "It's {}'s turn.".format(player)
        print repr(player)
        print

        for i, action in enumerate(self.actions):
            print "{}: {}".format(i+1, str(action))

    def play_turn(self, player):
        pass

    def next_player(self):
        self.cpi = (self.cpi + 1) % len(self.players)
        self.current = self.players[self.cpi]

    # how should this be structured in order to accommodate an AI?
    # players in a game should be represented using an ID that does not change
    # 
    def start(self):
        if not 3 <= len(self.players) <= 6:
            return False

        print "Welcome to Coup!!"
        print

        # prepare for the first turn
        self.next_player()

        while not self.game_over:
            alive = filter(Player.alive, self.players)

            assert len(alive) >= 1

            if not self.current.alive():
                self.next_player()
                continue

            if len(alive) == 1:
                self.game_over = True
                continue

            self.prepare_player(self.current)

            # request player action
            chosen_action = raw_input("Choose an action: ").rstrip("\n")
            if chosen_action == "q" or chosen_action == "quit" or chosen_action == "exit":
               game_over = True
               break

            try:
                if chosen_action == "":
                    raise Exception()

                action = Action(int(chosen_action))
            except Exception:
                self.status += "Invalid action, please try again\n"
                continue

            print "{} chooses action {}".format(self.current, action)

            # TODO: manage non-game actions (quit/exit) uniformly?
            # Should we just have action modify the game state directly if it succeeds?
            # Meld into same framework?

            target = None
            if action.requires_target():
                valid_players = filter(lambda p: p != self.current, filter(Player.alive, self.players))
                target = choose(valid_players, "Which player will you target?")

                print target

            if not action.valid(self, self.current, target):
                self.status += "Invalid action, please try again\n"
                continue
        
            '''
            # resolve challenges if possible
            challenger = None
            if action.can_challenge():
                challenger = challenge(self.players, self.current)
            
            if challenger != None:
                print "{}, {} would like to challenge your action!".format(self.current, challenger)
            '''

            action.apply(self, self.current, target)

            self.next_player()

        return True

    def __str__(self):
        s = ""

        s += "Players:\n"
        for i, p in enumerate(self.players):
            s += "\t"
            s += "=> " if p == self.current else "   "
            s += repr(p)
            s += "\n"

        s += "Deck: {}\n".format(self.deck)

        return s

