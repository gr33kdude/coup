#!/usr/bin/env python

from core import *
from game import *

from collections import defaultdict

# Deck tests

def test_deck_complete():
    g = Game()
    assert len(g.deck) == 15

def test_deck_distribution():
    g = Game()

    role_counts = defaultdict(int)
    for role in g.deck:
        role_counts[role.role] += 1

    for role in Role:
        assert role_counts[role] == 3
    
def test_deck_unique():
    g = Game()
    
    deck_ids = map(id, g.deck)
    unique_role_objects = set(deck_ids)

