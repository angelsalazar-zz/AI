from agents import Agent
from agents import Direction
from items import Trap
from allowActions import TURN
from allowActions import ADVANCED
from allowActions import STAY
from baseReflexAgent import BaseReflexAgent
from baseReflexAgent import travel

def rank(origen, destinos):
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
      bestDestino = thing

  return bestDestino

class SimpleReflexAgent(BaseReflexAgent):
  def forward(self):
    self.modifyPerformance(-1)
    newLocation = self.checkBounds()
   
    if newLocation:
      self.location = newLocation
      return True
    return False 

def createSimpleReflexAgent():
  agent = None

  # program can access variables declared
  # in the scope of createSimpleReflexAgent 
  def program(percepts):
    things, cells = percepts
    agentCurrentLocation = (agent.location[0], agent.location[1], agent.currentDirection.direction)
  
    bestOption = rank(agentCurrentLocation, things)
    nextAction = ''
    print('AGENT LOCATION: ' + str(agent.location) + '\n')
    if bestOption:
      print('BEST OPTION: ' + str(bestOption.location) + '\n')
    else: 
      print('BEST OPTION: None' + '\n')

    if not bestOption:
      nextAction = STAY
      agent.alive = False
    elif (agent.location[0] == bestOption.location[0] and agent.location[1] == bestOption.location[1]):
      nextAction = STAY
    else:
      nextAction = travel(agentCurrentLocation, bestOption.location)
    return nextAction
  
  agent = SimpleReflexAgent(program)

  return agent
