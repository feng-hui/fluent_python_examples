#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @time   : 2018-11-19 21:00
# @author : feng_hui
# @email  : capricorn1203@126.com
import random
from chapter_11.tombola import Tombola


class BingoCage(Tombola):

    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        self.pick()