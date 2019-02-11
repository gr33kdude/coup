#!/usr/bin/env python

import random
from math import ceil, log10
import os
import enum

def clear_screen():
    os.system("clear")

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

class Action(enum.IntEnum):
    income = 1
    foreign_aid = 2
    coup = 3
    tax = 4
    assassinate = 5
    steal = 6
    swap = 7

    def __init__(self, action):
        self.action = action

    def can_challenge(self):
        challengeable = {
            Action.income:         False,
            Action.foreign_aid:    True,
            Action.coup:           False,
            Action.tax:            True,
            Action.assassinate:    True,
            Action.steal:          True,
            Action.swap:           True,
        }
        
        return challengeable[self.action]

    def requires_target(self):
        needs_target = {
            Action.income:         False,
            Action.foreign_aid:    False,
            Action.coup:           True,
            Action.tax:            False,
            Action.assassinate:    True,
            Action.steal:          True,
            Action.swap:           False,
        }

        return needs_target[self.action]

    # source : Player
    # target : Player
    def apply(self, game, source, target):
        if self == Action.income:
            source.money += 1
            game.bank -= 1
        elif self == Action.foreign_aid:
            source.money += 2
            game.bank -= 2
        elif self == Action.coup:
            source.money -= 7
            game.bank += 7

            target.kill()
        elif self == Action.tax:
            source.money += 3
            game.bank -= 3
        elif self == Action.assassinate:
            source.money -= 3
            game.bank += 3

            target.kill()
        elif self == Action.steal:
            steal_amt = max(target.money, 2)
            source.money += steal_amt
            target.money -= steal_amt
        elif self == Action.swap:
            pass
        else:
            pass

    def valid(self, game, source, target):
        if source.money >= 10 and self != Action.coup:
            return False

        if self == Action.income:
            return game.bank >= 1
        elif self == Action.foreign_aid:
            return game.bank >= 2
        elif self == Action.coup:
            return source.money >= 7
        elif self == Action.tax:
            return game.bank >= 3
        elif self == Action.assassinate:
            return target.alive()
        elif self == Action.steal:
            return target.money > 0
        elif self == Action.swap:
            return True

        return True

    def __str__(self):
        names = {
            Action.income:         "Income",
            Action.foreign_aid:    "Foreign Aid",
            Action.coup:           "Coup",
            Action.tax:            "Tax",
            Action.assassinate:    "Assassinate",
            Action.steal:          "Steal",
            Action.swap:           "Swap",
        }
        
        return names[self.action]

class Player:
    def __init__(self, name, id):
        self.name = name
        self.money = 2
        self.roles = []
        self.id = id

    def alive(self):
        lives = map(Role.hidden, self.roles)
        # the player is alive if any role is still hidden
        return any(lives)

    def kill(self):
        assert self.alive()
        lives = filter(Role.hidden, self.roles)
        if len(lives) > 1:
            influence = choose(lives, "Which role would you like to reveal?")
        else:
            influence = lives[0]

        influence.reveal()

    def __str__(self):
        return self.name

    def __repr__(self):
        r = "{} ({}): {}".format(self.name, self.money, ", ".join(map(str, self.roles)))

        if not self.alive():
            r = "~~ {} ~~".format(r)

        r = "{{{}}} {}".format(self.id, r)

        return r

class Role:
    duke = 1
    assassin = 2
    captain = 3
    ambassador = 4
    contessa = 5

    names = {
        duke:       "Duke",
        assassin:   "Assassin",
        captain:    "Captain",
        ambassador: "Ambassador",
        contessa:   "Contessa",
    }

    def hidden(self):
        return self.hidden

    def reveal(self):
        self.hidden = False

    def __init__(self, role):
        self.hidden = True
        self.role = role

    def __str__(self):
        name = Role.names[self.role]
        return "[" + name + "]" if self.hidden else name

    def __repr__(self):
        return self.__str__()

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
        if not 2 <= len(self.players) <= 6:
            print "Invalid number of players ({})! Game only supports between 2-6 players.".format(len(self.players))
            return False

        print "Welcome to Coup!!"
        print

        # prepare for the first turn
        self.next_player()

        while not self.game_over:
            alive = filter(Player.alive, self.players)

            if len(alive) <= 1:
                self.game_over = True
                continue

            if not self.current.alive():
                self.next_player()
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

def main():
    players = []
    player_names = [ "Costas", "Cam", "Jeff" ]
    for i, name in enumerate(player_names):
        players.append( Player(name, i + 1) )

    g = Game()
    map(g.add, players)

    return g.start()

if __name__ == "__main__":
    main()
