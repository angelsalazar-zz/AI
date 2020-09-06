from agents import Agent
from agents import Direction
from items import Trap
from allowActions import TURN
from allowActions import ADVANCED
from allowActions import STAY
from baseReflexAgent import BaseReflexAgent
from baseReflexAgent import travel


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




class ModelReflexAgent(BaseReflexAgent):
  visited = set()
  visible = set()

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
