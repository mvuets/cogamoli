#!/usr/bin/python2

from __future__ import print_function
import random

class World (object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = {}
        self.morgue = set()
        self.kindergarten = set()

    def __contains__(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def __getitem__(self, pos):
        if pos not in self:
            raise KeyError("pos=%s is out of boundaries" % (pos,))
        return self.field.get(pos, -1)

    def __setitem__(self, pos, val):
        self[pos] # boundary check
        if val == 0:
            raise ValueError("val=%s must be a non-zero integer" % (val,))
        self.field[pos] = val

    def step(self):
        self.morgue = set()
        self.kindergarten = set()
        for y in range(self.height):
            for x in range(self.width):
                pos = (x, y)
                surround_poses = (
                    (x-1, y-1), (x, y-1), (x+1, y-1),
                    (x-1, y  ),           (x+1, y  ),
                    (x-1, y+1), (x, y+1), (x+1, y+1),
                )
                count = sum(1 for pos in surround_poses if pos in self and self[pos] > 0)
                cell = self[pos]
                if cell < 0 and count == 3:
                    self.kindergarten.add(pos)
                elif cell > 0 and not 2 <= count <= 3:
                    self.morgue.add(pos)
        for pos in self.kindergarten:
            self.field[pos] = 1
        for pos in self.morgue:
            self.field[pos] = -1


WIDTH = 40
HEIGHT = 30

world = World(width=WIDTH, height=HEIGHT)

# Populate the world randomly
for y in range(HEIGHT):
    for x in range(WIDTH):
        world[x, y] = random.choice((1, -1))


DEAD = object()
CEASING = object()
ARISING = object()
ALIVE = object()
CELL_TO_CHAR = {
    DEAD: " ",
    ARISING: ".",
    ALIVE: "O",
    CEASING: "x",
}

def render(world):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pos = (x, y)
            cell = (pos in world.kindergarten and ARISING) \
                or (pos in world.morgue and CEASING) \
                or (world[x, y] > 0 and ALIVE) \
                or DEAD
            print("%s" % (CELL_TO_CHAR[cell],), end="")
        print()

print("<enter> to step; ^C to quit")
while True:
    raw_input()
    render(world)
    world.step()
