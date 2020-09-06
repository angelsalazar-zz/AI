from agents import Environment
from agents import Agent
from agents import Direction
from items import Gold
from items import Trap
from simpleReflexAgent import SimpleReflexAgent
from modelReflexAgent import ModelReflexAgent
from allowActions import TURN
from allowActions import ADVANCED
from allowActions import STAY
from stateRender import StateRenderer

import random

FULLY_OBSERVABLE = 'FULLY'
PARTIALLY_OBSERVABLE = 'PARTIALLY'

def randomDirection():
  return [Direction.R, Direction.D, Direction.L, Direction.U][random.randint(0, 3)]

class Grid(Environment):
  def __init__(self, envType = FULLY_OBSERVABLE):
    super(Grid, self).__init__()
    self.state = []
    self.STEP_COUNT = 0
    self.stateRender = StateRenderer(self)
    for _ in range(25):
      self.state.append({"A":0,"G":0,"T":0})
    self.envType = envType
    self.MAX_WIDTH = self.MAX_HEIGHT = 5
    print('<STARTING>')

  def thing_classes(self):
    return [ModelReflexAgent, SimpleReflexAgent, Trap, Gold]  # List of classes that can go into environment

  def percept(self, agent):
    things = self.things.copy()
    percepts = []

    if self.envType == FULLY_OBSERVABLE:
        for i in range(5):
          for j in range(5):
            percepts.append((i, j))

    if self.envType == PARTIALLY_OBSERVABLE:
      movements = [(1,0),(1,1),(0,1),(-1,-1),(-1,0),(0,-1),(-1,1),(1,-1)]
      for m in movements:
        newX = agent.location[0] + m[0]
        newY = agent.location[1] + m[1]
        if newX < 5 and newX >= 0 and newY < 5 and newY >= 0:
          percepts.append((newX,newY))

        for thing in things:
          if ((thing.location[0],thing.location[1]) not in percepts):
            things.remove(thing)

    print(agent)       
    self.stateRender.printEnvironment(agent=agent)
    print('Agent performance: ' + (str(agent.performance)))
    self.stateRender.printAgentPercept(agent = agent, things=things, percepts=percepts)
    return things, percepts

  def add_thing(self, thing, location = None):
    # set random location if not provided
    thing.location = location if location is not None else self.default_location(thing)

    # if thing is instance of Agent
    if (isinstance(thing, Agent)):
      self.state[thing.location[0]*5 + thing.location[1]]["A"] += 1
      thing.performance = 100
      thing.currentDirection = Direction(randomDirection())
      self.agents.append(thing)
    else:
      if (isinstance(thing,Gold)):
        self.state[thing.location[0]*5 + thing.location[1]]["G"] += 1
      else:
        self.state[thing.location[0]*5 + thing.location[1]]["T"] += 1
      self.things.append(thing)

  def execute_action(self, agent, action):
    self.STEP_COUNT = self.STEP_COUNT + 1
    if isinstance(agent, ModelReflexAgent):
      self.stateRender.printAgentState(agent)
    print('<Step> %s' % (self.STEP_COUNT))
    print('SELECT ACTION: %s' % (action))
    
    if action == TURN:
      agent.turn()
      self.consumeThingsAtAgentLocation(agent)
    elif action == ADVANCED:
      previousLocation = agent.location
      if agent.forward():
        self.state[previousLocation[0] * 5 + previousLocation[1]]['A'] = 0
        self.state[agent.location[0] * 5 + agent.location[1]]['A'] = 1

      self.consumeThingsAtAgentLocation(agent)
    elif action == STAY:
      self.consumeThingsAtAgentLocation(agent)

  # generate a random location for the given thing
  def default_location(self, thing):
    # generate random x, y
    x = random.randint(0, self.MAX_WIDTH - 1)
    y = random.randint(0, self.MAX_HEIGHT - 1)
    return (x, y)

  def consumeThingsAtAgentLocation(self, agent):
    ores = self.list_things_at(agent.location, Gold)
    traps = self.list_things_at(agent.location, Trap)

    if len(ores) > 0:
      ore = ores[0]
      self.state[ore.location[0] * 5 + ore.location[1]]['G'] = self.state[ore.location[0] * 5 + ore.location[1]]['G'] - 1
      self.delete_thing(ore)
      agent.modifyPerformance(10)

    if len(traps) > 0:
      trap = traps[0]
      self.state[trap.location[0] * 5 + trap.location[1]]['T'] = self.state[trap.location[0] * 5 + trap.location[1]]['T'] - 1
      self.delete_thing(traps[0])
      agent.modifyPerformance(-5)

  def isFullyObservable(self):
    return self.envType == FULLY_OBSERVABLE
