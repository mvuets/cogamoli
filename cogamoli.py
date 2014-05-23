#!/usr/bin/python2

import random

class World (object):
    DEAD = -2
    ARISING = -1
    ALIVE = 1
    CEASING = 2

    def __init__(self, width, height):
        self.field = {}
        self.width = width
        self.height = height

    def __contains__(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def __getitem__(self, pos):
        if pos not in self:
            raise KeyError("pos=%s is out of boundaries" % (pos,))
        return self.field.get(pos, World.DEAD)

    def __setitem__(self, pos, val):
        self[pos] # boundary check
        if not any(val == o for o in (World.DEAD, World.ARISING, World.ALIVE, World.CEASING)):
            raise ValueError("val=%s is unknown" % (val,))
        if val == World.DEAD:
            if pos in self.field:
                del self.field[pos]
        else:
            self.field[pos] = val

    def step(self):
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
                if cell == World.DEAD:
                    if count == 3:
                        self[pos] = World.ARISING
                elif cell == World.ALIVE:
                    if not 2 <= count <= 3:
                        self[pos] = World.CEASING
                else:
                    raise NotImplementedError("cell type %s is unhandled" % (cell,))
        for pos, cell in self.field.items():
            if cell == World.ARISING:
                self[pos] = World.ALIVE
            elif cell == World.CEASING:
                self[pos] = World.DEAD


WIDTH = 40
HEIGHT = 30

world = World(width=WIDTH, height=HEIGHT)

# Populate the world randomly
for y in range(HEIGHT):
    for x in range(WIDTH):
        world[x, y] = random.choice((World.DEAD, World.ALIVE))


def render(world):
    CELL_TO_CHAR = {
        World.DEAD: " ",
        World.ALIVE: "O",
    }
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print "%s" % (CELL_TO_CHAR[world[x, y]],),
        print

print "<enter> to step; ^C to quit"
while True:
    raw_input()
    render(world)
    world.step()