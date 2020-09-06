from agents import Agent
from agents import Direction
from items import Trap
from allowActions import TURN
from allowActions import ADVANCED
from allowActions import STAY
"""
The result of executing an action is as follows:
• The performance measure of the agent starts with 100 points.
• Every Turn and Advance action reduce one point from the agent’s performance measure.
• The Turn action changes the direction of the agent in clockwise, i.e. from Up to Right or
from Right to Down or from Down to Left or from Left to Up.
• The Advance action changes the agent location to the next cell in its current direction if it
is not outside the grid. Trying to move outside the grid reduces its performance but
maintains its location and direction.
• Entering a previous visited cell cost the agent 2 points but staying in a cell does not cost.
• Entering or staying in a cell containing gold pieces gives 10 points to the agent.
• Entering or staying in a cell containing traps takes 5 points from the agent.
• Getting a gold piece or falling in a trap remove these things from the environment.
• Even when one cell contains multiple gold pieces or multiple traps, the agent entering or
staying in that cell will be affected once by these things after executing each action.
"""

def rankUnvisited(origen, notVisited):
  bestDestino = None
  bestSuma = 10000000
  suma = 0

  for destino in notVisited:
    suma = abs(destino[0]-origen[0])+abs(destino[1]-origen[1])
    if destino[0] > origen[0]: # Esta abajo el destino
      if origen[2] == Direction.R:
        suma += 1
      if origen[2] == Direction.U:
        suma += 2
      if origen[2] == Direction.L:
        suma += 3
    if destino[0] < origen[0]: # esta arriba el destino
      if origen[2] == Direction.R:
        suma += 3
      if origen[2] == Direction.D:
        suma += 2
      if origen[2] == Direction.L:
        suma += 1
    if destino[1] > origen[1]: # esta a la derecha el destino
      if origen[2] == Direction.U:
        suma += 1
      if origen[2] == Direction.D:
        suma += 3
      if origen[2] == Direction.L:
        suma += 2
    if destino[1] < origen[1]: # esta a la izquierda el destino
      if origen[2] == Direction.U:
        suma += 3
      if origen[2] == Direction.D:
        suma += 1
      if origen[2] == Direction.R:
        suma += 2

    if suma < bestSuma:
      bestSuma = suma
      bestDestino = destino

  return bestDestino

def rank(origen, destinos, notVisited):
  bestDestino = None
  bestSuma = 10000000
  suma = 0
  destino = None
  for thing in destinos:
    if isinstance(thing, Trap):
      continue

    destino = thing.location
    suma = abs(destino[0]-origen[0])+abs(destino[1]-origen[1])
    if destino[0] > origen[0]: # Esta abajo el destino
      if origen[2] == Direction.R:
        suma += 1
      if origen[2] == Direction.U:
        suma += 2
      if origen[2] == Direction.L:
        suma += 3
    if destino[0] < origen[0]: # esta arriba el destino
      if origen[2] == Direction.R:
        suma += 3
      if origen[2] == Direction.D:
        suma += 2
      if origen[2] == Direction.L:
        suma += 1
    if destino[1] > origen[1]: # esta a la derecha el destino
      if origen[2] == Direction.U:
        suma += 1
      if origen[2] == Direction.D:
        suma += 3
      if origen[2] == Direction.L:
        suma += 2
    if destino[1] < origen[1]: # esta a la izquierda el destino
      if origen[2] == Direction.U:
        suma += 3
      if origen[2] == Direction.D:
        suma += 1
      if origen[2] == Direction.R:
        suma += 2

    if suma < bestSuma:
      bestSuma = suma
      bestDestino = thing.location

  if bestSuma == 10000000:
    return rankUnvisited(origen,notVisited)

  return bestDestino


def travel(origen, destino):
  if origen[2] == Direction.R:
    if origen[1] < destino[1]:
      return ADVANCED
    else:
      return TURN

  if origen[2] == Direction.U:
    if origen[0] <= destino[0]:
      return TURN
    else:
      return ADVANCED

  if origen[2] == Direction.D:
    if origen[0] < destino[0]:
      return ADVANCED
    else:
      return TURN

  if origen[2] == Direction.L:
    if origen[1] <= destino[1]:
      return TURN
    else:
        return ADVANCED

class ModelReflexAgent(Agent):

  visited = set()
  visible = set()

  def __init__(self, program):
    super(ModelReflexAgent, self).__init__(program)
    self.currentDirection = None

  def __str__(self):
    return '(%s, %s, %s)' % (
      self.location[0],
      self.location[1],
      self.currentDirection.direction
    )

  def modifyPerformance(self, amount):
    self.performance += amount

  def checkBounds(self):
    newX = self.location[0]
    newY = self.location[1]
    currentDir = self.currentDirection

    if (currentDir.direction == Direction.U):
      newX = self.location[0] - 1
    elif (currentDir.direction == Direction.R):
      newY = self.location[1] + 1
    elif (currentDir.direction == Direction.D):
      newX = self.location[0] + 1
    elif (currentDir.direction == Direction.L):
      newY = self.location[1] - 1

    if newX < 0 or newY < 0 or newX >= 5 or newY >= 5:
      return None
    else:
      return (newX,newY)

  def turn(self):
    self.modifyPerformance(-1)
    # update direction
    # we can only turn clockwise
    self.currentDirection = self.currentDirection + Direction.R

  def forward(self):
    self.modifyPerformance(-1)
    newLocation = self.checkBounds()

    if newLocation:
      self.location = newLocation
      self.visited.add(newLocation)
      return True
    return False


def createModelReflexAgent():
  agent = None

  # program can access variables declared
  # in the scope of createSimpleReflexAgent
  def program(percepts):
    things, cells = percepts
    agent.visible.update(cells)
    print("Visible:",agent.visible)
    print("Visited:",agent.visited)
    agentCurrentLocation = (agent.location[0], agent.location[1], agent.currentDirection.direction)

    bestOption = rank(agentCurrentLocation, things, agent.visible-agent.visited)
    nextAction = ''
    print('AGENT LOCATION: ' + str(agent.location) + '\n')
    if bestOption:
      print('BEST OPTION: ' + str(bestOption) + '\n')
    else:
      print('BEST OPTION: None' + '\n')

    if not bestOption:
      nextAction = STAY
      agent.alive = False
    elif (agent.location[0] == bestOption[0] and agent.location[1] == bestOption[1]):
      nextAction = STAY
    else:
      nextAction = travel(agentCurrentLocation, bestOption)
    return nextAction

  agent = ModelReflexAgent(program)

  return agent
