from envImpl import Grid
from items import Gold
from items import Trap
from simpleReflexAgent import createSimpleReflexAgent
from modelReflexAgent import createModelReflexAgent
from agents import Direction

import random

FIX_AGENT_LOCATION = (3, 4)
grid = Grid(envType = "PARTIALLY")

# adding Trap
for i in range(random.randint(0, 0)):
  grid.add_thing(Trap())

 # adding Gold
for i in range(random.randint(0, 0)):
    grid.add_thing(Gold())

grid.add_thing(createModelReflexAgent(), FIX_AGENT_LOCATION)

grid.run(4)
