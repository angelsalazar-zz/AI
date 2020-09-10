from agents import Agent
from agents import Direction
from items import Trap
from allowActions import TURN
from allowActions import ADVANCED
from allowActions import STAY
from baseReflexAgent import BaseReflexAgent
from baseReflexAgent import travel


# rankUnvisited
# gets the cells that requires the least amount steps to get reached
# @param {Tuple} origen (row, col, direction)
# @param {List<Tuple>} notVisited
# @return {Tuple}
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

# rank
# gets the gold item that requires the least amount steps to get reached
# @param {Tuple} origen (row, col, direction)
# @param {List<Things>} destinos
# @param {List<Tuple>} notVisited
# @return {Thing}
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

# SimpleReflexAgent
# used to create instances of model based reflex agent
class ModelReflexAgent(BaseReflexAgent):

  # Model based reflex agent 
  # internal state
  visited = set()
  visible = set()
  
  # forward
  # returns true wether the agent was able to move
  # if true, agent location changes and performance decreces by 1
  # if false, agent location remains the same and performance decreces by 1
  # @return {Boolean}
  def forward(self):
    self.modifyPerformance(-1)
    newLocation = self.checkBounds()

    if newLocation:
      self.location = newLocation
      self.visited.add(newLocation)
      if self.visited.intersection(newLocation):
        self.modifyPerformance(-2)
      return True
    return False


# createModelReflexAgent
# factory method that creates instances of model based reflex agent
# @return {SimpleReflexAgent}
def createModelReflexAgent():
  agent = None

  # program
  # model based reflex agent's program
  # @param {List<Things, List<Tuple>} percepts
  # @return {String} action
  def program(percepts):
    things, cells = percepts
    # update agent internal state
    agent.visible.update(cells)
    agentCurrentLocation = (agent.location[0], agent.location[1], agent.currentDirection.direction)

    # computes the best option
    bestOption = rank(agentCurrentLocation, things, agent.visible-agent.visited)
    nextAction = ''

    # if no best option
    # kill agent
    if not bestOption:
      nextAction = STAY
      agent.alive = False
    elif (agent.location[0] == bestOption[0] and agent.location[1] == bestOption[1]):   # if agent location and best option location are equal
      nextAction = STAY                                                                 # set next action to STAY
    else:
      nextAction = travel(agentCurrentLocation, bestOption)                             # else compute next action
    return nextAction

  agent = ModelReflexAgent(program) # init ModelReflexAgent instance

  return agent
