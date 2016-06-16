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
        self.roles = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return "{}: {}".format(self.name, ", ".join(map(str, self.roles)))

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

    def __init__(self, role):
        self.hidden = True
        self.role = role

    def __str__(self):
        name = Role.names[self.role]
        return "[" + name + "]" if self.hidden else name

bank = 60

players = [ Player("Costas"), Player("Cam") ]

game_over = False

if not 2 <= len(players) <= 6:
    print "Invalid number of players ({})! Game only supports between 2-6 players.".format(len(players))

deck = map(Role, [ Role.duke, Role.assassin, Role.captain, Role.ambassador, Role.contessa ] * 3)
random.shuffle(deck)
# assign initial roles

actions = map(Action, [ Action.income, Action.foreign_aid, Action.coup, Action.tax, Action.assassinate, Action.steal, Action.swap])

for player in players:
    # give each player 2 roles
    player.roles.extend( [deck.pop(), deck.pop()])

while not game_over:
    for player in players:
        print "It's {}'s turn.".format(player)
        print repr(player)

        for action in actions:
            print "{}: {}".format(action.action, action)

        chosen_action = raw_input("Choose an action: ")
        if chosen_action == "q" or chosen_action == "quit" or chosen_action == "exit":
           game_over = True 
           break

        chosen_action = int(chosen_action)
        
        if chosen_action not in [ Action.income, Action.foreign_aid, Action.coup ]:
            challenge = challenge(players, player)
