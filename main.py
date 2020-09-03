from envImpl import Grid
from items import Gold
from items import Trap
from agentsImpl import SimpleReflexAgent

import random

grid = Grid()

print(grid)
# adding Trap
for i in range(random.randint(5, 8)):
  grid.add_thing(Trap())

# adding Gold
for i in range(random.randint(5, 8)):
  grid.add_thing(Gold())

grid.add_thing(SimpleReflexAgent())

print('env things: ' + str(len(grid.things)))
print('env agents: ' + str(len(grid.agents)))
print(grid)
