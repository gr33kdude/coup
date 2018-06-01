#!/usr/bin/env python

import random

def challenge(players, player):
    challenge = False
    for other in players:
        if player == other:
            continue

        while True:
            challenge_inp = raw_input("{}, would you like to challenge? (y/n) ".format(other))
            if challenge_inp in [ 'y', 'n' ]:
                challenge = map(lambda s: {'y': True, 'n': False}[s], challenge_inp)
                break
            print "Invalid input"

        if challenge:
            break

    return challenge

class Action:
    income = 1
    foreign_aid = 2
    coup = 3
    tax = 4
    assassinate = 5
    steal = 6
    swap = 7

    names = {
        income:         "Income",
        foreign_aid:    "Foreign Aid",
        coup:           "Coup",
        tax:            "Tax",
        assassinate:    "Assassinate",
        steal:          "Steal",
        swap:           "Swap",
    }

    def __init__(self, action):
        self.action = action

    def __str__(self):
        return Action.names[self.action]

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 2
        self.roles = []

    def alive(self):
        lives = map(Role.hidden, self.roles)
        # the player is alive if any role is still hidden
        return any(lives)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{} ({}): {}".format(self.name, self.money, ", ".join(map(str, self.roles)))

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

        self.deck = map(Role, [ Role.duke, Role.assassin, Role.captain, Role.ambassador, Role.contessa ] * 3)
        random.shuffle(self.deck)

    def add(self, player):
        if len(self.players) == 5:
            return False

        assert(len(self.deck) > 2)

        player.roles.extend( [self.deck.pop(), self.deck.pop()] )
        self.players.append(player)

        return True

    def start(self):
        if not 2 <= len(self.players) <= 6:
            print "Invalid number of players ({})! Game only supports between 2-6 players.".format(len(self.players))
            return False

        print "Welcome to Coup!!"
        print

        print "Here are our players:"
        for p in self.players:
            print repr(p)
        print

        print "Deck:"
        print self.deck
        print

        while not self.game_over:
            if not any(map(Player.alive, self.players)):
                self.game_over = True
                continue

            for player in self.players:
                if not player.alive():
                    print "Skipping player {} (dead)".format(player)
                    continue

                print "It's {}'s turn.".format(player)
                print repr(player)
                print

                for action in self.actions:
                    print "{}: {}".format(action.action, action)

                chosen_action = raw_input("Choose an action: ")
                if chosen_action == "q" or chosen_action == "quit" or chosen_action == "exit":
                   game_over = True
                   break

                chosen_action = int(chosen_action)

                if chosen_action not in [ Action.income, Action.foreign_aid, Action.coup ]:
                    challenge = challenge(players, player)

        return True

def main():
    players = [ Player("Costas"), Player("Cam") ]

    g = Game()
    map(g.add, players)

    return g.start()

if __name__ == "__main__":
    main()
