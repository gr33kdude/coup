#!/usr/bin/env python3

from math import ceil, log10
import enum

class Role(enum.IntEnum):
    DUKE = 1
    ASSASSIN = 2
    CAPTAIN = 3
    AMBASSADOR = 4
    CONTESSA = 5

    def can_perform(self, action):
        if action in [Action.INCOME, Action.FOREIGN_AID, Action.COUP]:
            return True

        allowed = {
            Role.DUKE: Action.TAX,
            Role.ASSASSIN: Action.ASSASSINATE,
            Role.CAPTAIN: Action.STEAL,
            Role.AMBASSADOR: Action.SWAP,
            Role.CONTESSA: None,
        }
        return action == allowed[self]

    def can_block(self, action):
        if action in [Action.INCOME, Action.COUP]:
            return False

        blocked = {
            Role.DUKE: Action.FOREIGN_AID,
            Role.ASSASSIN: None,
            Role.CAPTAIN: Action.STEAL,
            Role.AMBASSADOR: Action.STEAL,
            Role.CONTESSA: Action.ASSASSINATE,
        }
        return action == blocked[self]

    def __str__(self):
        return {
            Role.DUKE:       "Duke",
            Role.ASSASSIN:   "Assassin",
            Role.CAPTAIN:    "Captain",
            Role.AMBASSADOR: "Ambassador",
            Role.CONTESSA:   "Contessa",
        } [self]

    def __repr__(self):
        return self.__str__()

class Influence:
    def __init__(self, role):
        self.hidden = True
        self.role = role

    def hidden(self):
        return self.hidden

    def reveal(self):
        self.hidden = False

    def __str__(self):
        name = str(self.role)
        return "[" + name + "]" if self.hidden else name

    def __repr__(self):
        return self.__str__()

class Action(enum.IntEnum):
    INCOME = 1
    FOREIGN_AID = 2
    COUP = 3
    TAX = 4
    ASSASSINATE = 5
    STEAL = 6
    SWAP = 7

    def can_challenge(self):
        return self not in [Action.INCOME, Action.COUP]

    def requires_target(self):
        return self in [Action.COUP, Action.ASSASSINATE, Action.STEAL]

    # source : Player
    # target : Player
    def apply(self, game, source, target):
        if self == Action.INCOME:
            source.money += 1
            game.bank -= 1
        elif self == Action.FOREIGN_AID:
            source.money += 2
            game.bank -= 2
        elif self == Action.COUP:
            source.money -= 7
            game.bank += 7

            # TODO: THIS IS BROKEN
            target.kill()
        elif self == Action.TAX:
            source.money += 3
            game.bank -= 3
        elif self == Action.ASSASSINATE:
            source.money -= 3
            game.bank += 3

            target.kill()
        elif self == Action.STEAL:
            steal_amt = max(target.money, 2)
            source.money += steal_amt
            target.money -= steal_amt
        elif self == Action.SWAP:
            pass
        else:
            raise Exception()

    def valid(self, game, source, target):
        if source.money >= 10 and self != Action.COUP:
            return False

        if self == Action.INCOME:
            return game.bank >= 1 # due to game design, always True
        elif self == Action.FOREIGN_AID:
            return game.bank >= 2 # due to game design, always True
        elif self == Action.COUP:
            return source.money >= 7
        elif self == Action.TAX:
            return game.bank >= 3 # due to game design, always True
        elif self == Action.ASSASSINATE:
            if source.money < 3:
                return False
            if target:
                return target.alive()
        elif self == Action.STEAL:
            if target:
                return target.money >= 0
        elif self == Action.SWAP:
            return True

        return True

    def __str__(self):
        return {
            Action.INCOME:         "Income",
            Action.FOREIGN_AID:    "Foreign Aid",
            Action.COUP:           "Coup",
            Action.TAX:            "Tax",
            Action.ASSASSINATE:    "Assassinate",
            Action.STEAL:          "Steal",
            Action.SWAP:           "Swap",
        } [self]

    def __repr__(self):
        return self.__str__()

class Player:
    def __init__(self, name, id):
        self.name = name
        self.honest = True
        self.money = 2
        self.influence = []
        self.id = id

    def alive(self):
        lives = map(Influence.hidden, self.influence)
        # the player is alive if any role is still hidden
        return any(lives)

    def __str__(self):
        return self.name

    def __repr__(self):
        r = "{} ({}): {}" \
            .format(self.name,
                    self.money,
                    ", ".join(map(str, self.influence)))

        if not self.alive():
            r = "~~ {} ~~".format(r)

        r = "{{{}}} {}".format(self.id, r)

        return r
