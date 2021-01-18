#!/usr/bin/env python3

from core import *

import random
import sys
import copy

def clear_screen():
    sys.stdout.write("\x1b[2J")
    sys.stdout.write("\x1b[H")
    sys.stdout.flush()

class Game:
    def __init__(self, log=False, replay=False):
        self.bank = 60
        self.game_over = False
        self.players = []
        self.cpi = -1 # current player index
        self.current = None
        self.status = ""

        self.log = log
        self.log_f = None
        self.log_fn = "[NONE]"

        self.replay = replay

        if self.log and self.replay:
            self.log = False

        if self.log:
            self.log_f = open('log', 'a')

        if self.log_f:
            self.log_fn = self.log_f.name

        if self.replay:
            self.replay_f = open('log', 'r')

        self.deck = [Influence(r) for r in Role for i in range(3)]

        random.shuffle(self.deck)

    def logged_input(self, prompt):
        inp = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()

        try:
            if self.replay:
                inp = self.replay_f.readline(4096)
        except EOFError:
            pass

        # If we have exhausted the replay file (or if there was an error)
        if inp == "":
            inp = sys.stdin.readline()

        try:
            if self.log:
                print(inp, file=self.log_f)
        except IOError:
            print("Could not log input to log file ({}): {}" \
                  .format(self.log_fn, inp), \
                  file=sys.stderr)

        return inp

    def add(self, player):
        if len(self.players) == 5:
            return False

        assert(len(self.deck) > 2)

        player.influence.extend( [self.deck.pop(), self.deck.pop()] )
        self.players.append(player)

        return True

    def prepare_player(self, player):
        clear_screen()

        if self.status != "":
            #print("=== Status Message ===")
            print(self.status)
            self.status = ""

        print("=== Game State ===")
        print(self)

        print("It's {}'s turn.".format(player))
        print(repr(player))
        print()

        for i, action in enumerate(Action):
            print("{}: {}".format(i+1, str(action)))

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

        print("Welcome to Coup!!")
        print()

        # prepare for the first turn
        self.next_player()

        while not self.game_over:
            alive = list(filter(Player.alive, self.players))

            assert len(alive) >= 1

            if not self.current.alive():
                self.next_player()
                continue

            if len(alive) == 1:
                self.game_over = True
                continue

            self.prepare_player(self.current)

            # request player action
            chosen_action = \
                self.logged_input("Choose an action: ").rstrip("\n")
            # TODO: manage non-game actions (quit/exit) uniformly?
            if chosen_action in ["q", "quit", "exit"]:
               game_over = True
               break

            try:
                if chosen_action == "":
                    raise Exception()

                action = Action(int(chosen_action))
            except Exception:
                self.status += "Invalid action, please try again\n"
                continue

            print("{} chooses action {}".format(self.current, action))

            # Should we just have action modify the game state directly if it
            # succeeds? Meld into same framework?

            # Sanity check for validity before selecting target
            target = None
            if not action.valid(self, self.current, target):
                self.status += "Invalid action, please try again\n"
                continue

            if action.requires_target():
                not_self = lambda p: p != self.current
                alive_players = filter(Player.alive, self.players)

                valid_targets = list(filter(not_self, alive_players))
                target = self.choose(valid_targets, "Which player will you target?")

            # Check for full-validity with target in mind
            if not action.valid(self, self.current, target):
                self.status += "Invalid action, please try again\n"
                continue
        
            # resolve challenges if possible
            challenger = None
            if action.can_challenge():
                challenger = self.challenge(self.players, self.current)
            
            if challenger:
                print("{} challenges {}'s action!".format(challenger, self.current))

                # TODO: current player has opportunity to reveal correct action
                # whoever loses the challenge has to forfeit a card
                pass
            else:
                # ask for block?
                # challenge block?
                pass

            action.apply(self, self.current, target)

            self.next_player()

        return True

    # options : [ opts, ... ]
    # question : string
    def choose(self, options, question):
        max_digits = int(ceil(log10(len(options)+1)))

        for i, opt in enumerate(options):
            print("{:{}}: {}".format(i + 1, max_digits, opt))
        print

        selection = None
        while selection == None:
            inp = self.logged_input(question + "  ")

            # handle invalid input, determine which option
            try:
                selection = int(inp) - 1
                if not 0 <= selection < len(options):
                    raise Exception()
            except Exception:
                print("Invalid input, please try again.")
                selection = None
                continue

        return options[selection]

    def challenge(self, players, player):
        for other in players:
            if player == other:
                continue

            challenge_inp = None
            while True:
                challenge_inp = \
                  self.logged_input("{}, would you like to challenge? (y/n) " \
                                    .format(other))
                if challenge_inp == 'y':
                    return other
                elif challenge_inp == 'n':
                    break
                else:
                    print("Invalid input, please try again")

    def kill(self, player):
        influence = player.reveal()
        influence.reveal()
    
    def reveal(self, player, action = None):
        assert player.alive()

        lives = filter(Influence.hidden, self.influence)

        # if the player has multiple Influence, we need to choose between them
        if len(lives) > 1:
            if action and player.honest:
                true_roles = filter(Role.can_perform, lives)
                if len(true_roles) > 0:
                    return true_roles[0]

            influence = choose(lives,
                    "Which hidden Influence would you like to reveal?")
        else:
            influence = lives[0]

        return influence

    def defend(self, action = None):
        pass

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

