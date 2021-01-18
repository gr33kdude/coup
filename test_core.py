#!/usr/bin/env python3

from core import *

def test_influence_hidden_by_default():
    for role in Role:
        infl = Influence(role)
        assert infl.hidden

def test_role_action_perform():
    # All roles should be able to perform the basic actions
    for role in Role:
        assert role.can_perform(Action.INCOME)
        assert role.can_perform(Action.FOREIGN_AID)
        assert role.can_perform(Action.COUP)

    assert     Role.DUKE.can_perform(Action.TAX)
    assert not Role.DUKE.can_perform(Action.ASSASSINATE)
    assert not Role.DUKE.can_perform(Action.STEAL)
    assert not Role.DUKE.can_perform(Action.SWAP)
    
    assert not Role.ASSASSIN.can_perform(Action.TAX)
    assert     Role.ASSASSIN.can_perform(Action.ASSASSINATE)
    assert not Role.ASSASSIN.can_perform(Action.STEAL)
    assert not Role.ASSASSIN.can_perform(Action.SWAP)

    assert not Role.CAPTAIN.can_perform(Action.TAX)
    assert not Role.CAPTAIN.can_perform(Action.ASSASSINATE)
    assert     Role.CAPTAIN.can_perform(Action.STEAL)
    assert not Role.CAPTAIN.can_perform(Action.SWAP)

    assert not Role.AMBASSADOR.can_perform(Action.TAX)
    assert not Role.AMBASSADOR.can_perform(Action.ASSASSINATE)
    assert not Role.AMBASSADOR.can_perform(Action.STEAL)
    assert     Role.AMBASSADOR.can_perform(Action.SWAP)

    assert not Role.CONTESSA.can_perform(Action.TAX)
    assert not Role.CONTESSA.can_perform(Action.ASSASSINATE)
    assert not Role.CONTESSA.can_perform(Action.STEAL)
    assert not Role.CONTESSA.can_perform(Action.SWAP)

def test_role_action_blocked():
    # All roles should not be able to block some of the basic actions
    for role in Role:
        assert not role.can_block(Action.INCOME)
        assert not role.can_block(Action.COUP)
        assert not role.can_block(Action.TAX)
        assert not role.can_block(Action.SWAP)

    assert     Role.DUKE.can_block(Action.FOREIGN_AID)
    assert not Role.DUKE.can_block(Action.ASSASSINATE)
    assert not Role.DUKE.can_block(Action.STEAL)
    
    assert not Role.ASSASSIN.can_block(Action.FOREIGN_AID)
    assert not Role.ASSASSIN.can_block(Action.ASSASSINATE)
    assert not Role.ASSASSIN.can_block(Action.STEAL)

    assert not Role.CAPTAIN.can_block(Action.FOREIGN_AID)
    assert not Role.CAPTAIN.can_block(Action.ASSASSINATE)
    assert     Role.CAPTAIN.can_block(Action.STEAL)

    assert not Role.AMBASSADOR.can_block(Action.FOREIGN_AID)
    assert not Role.AMBASSADOR.can_block(Action.ASSASSINATE)
    assert     Role.AMBASSADOR.can_block(Action.STEAL)

    assert not Role.CONTESSA.can_block(Action.FOREIGN_AID)
    assert     Role.CONTESSA.can_block(Action.ASSASSINATE)
    assert not Role.CONTESSA.can_block(Action.STEAL)
