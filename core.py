#!/usr/bin/env python

import enum

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
        return self.action not in [Action.income, Action.coup]

    def requires_target(self):
        return self.action in [Action.coup, Action.assassinate, Action.steal]

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

