from envImpl import Grid
from envImpl import FULLY_OBSERVABLE
from envImpl import PARTIALLY_OBSERVABLE
from items import Gold
from items import Trap
from simpleReflexAgent import createSimpleReflexAgent
from modelReflexAgent import createModelReflexAgent
from agents import Direction

import random

FIX_AGENT_LOCATION = (3, 4)
grid = Grid(envType = PARTIALLY_OBSERVABLE)

# adding Trap
for i in range(random.randint(4, 8)):
  grid.add_thing(Trap())

 # adding Gold
for i in range(random.randint(4, 8)):
    grid.add_thing(Gold())

grid.add_thing(createModelReflexAgent(), FIX_AGENT_LOCATION)

grid.run(4)
