from envImpl import Grid
from items import Gold
from items import Trap
from simpleReflexAgent import createSimpleReflexAgent
from agents import Direction

import random

FIX_AGENT_LOCATION = (3, 4)
grid = Grid()

# adding Trap
for i in range(random.randint(5, 8)):
  grid.add_thing(Trap())

 # adding Gold
for i in range(random.randint(5, 8)):
    grid.add_thing(Gold())

grid.add_thing(createSimpleReflexAgent(), FIX_AGENT_LOCATION)

grid.run(40)