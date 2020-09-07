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

# Availale Environment types
FULLY_OBSERVABLE = 'FULLY'
PARTIALLY_OBSERVABLE = 'PARTIALLY'

# randomDirection
# randomly provides a direction
# @return {String} 
def randomDirection():
  return [Direction.R, Direction.D, Direction.L, Direction.U][random.randint(0, 3)]


# Grid class
# it is used to create fully and partially observable environments
class Grid(Environment):

  # initialize instance variables
  def __init__(self, envType = FULLY_OBSERVABLE):
    super(Grid, self).__init__()
    self.state = []                                         # stores the enviroment state
    self.STEP_COUNT = 0                                     # reference to the steps performed by the agent
    self.stateRender = StateRenderer(self)                  # init state render instance
    for _ in range(25):                                     # fill state range
      self.state.append({"A":0,"G":0,"T":0})                
    self.envType = envType                                  # stores the environment type
    self.MAX_WIDTH = self.MAX_HEIGHT = 5                    # stores the max rows and cols
    print('<STARTING>')

  # List of classes that can go into environment
  def thing_classes(self):
    return [ModelReflexAgent, SimpleReflexAgent, Trap, Gold]


  # percept
  # percept computes what the agent can percept depending on the environment type
  # @param {Agent} agent
  # @return {List}, {List} things, percepts 
  #                        things: list of gold and trap items
  #                        percepts: list of visible cells
  def percept(self, agent):
    things = self.things.copy()                             # creating a copy of things
    percepts = list(agent.visible)                          # list of cells that the agent can percept

    if self.envType == FULLY_OBSERVABLE:                    # if environment is fully observable
        for i in range(5):                                  # provide all cells as visible
          for j in range(5):
            percepts.append((i, j))

    if self.envType == PARTIALLY_OBSERVABLE:                # if enviroment is partially observable
      movements = [                                         # movements define all possible cells
        (-1, -1), (-1, 0),  (-1, 1),                        # the agent can view
        ( 0, -1)         ,  ( 0, 1),
        ( 1, -1), ( 1, 0),  ( 1, 1)
      ]

      for m in movements:                                       # for each possible visible cell
        newX = agent.location[0] + m[0]                         
        newY = agent.location[1] + m[1]                         # fill percepts list as visible cell
        if newX < 5 and newX >= 0 and newY < 5 and newY >= 0:   # only if they are in the bounding by the enviroment
          percepts.append((newX,newY))
      percepts.append((agent.location[0],agent.location[1]))    # adds the agent location to the percepts

      things_to_remove = []                                     # init things_to_remove

      for thing in things:                                      # for each thing in the enviroment
        if (thing.location not in percepts):                    # check if thing is visible by the agent
          things_to_remove.append(thing)                        # if not add it to the things_to_remove

      for thing in things_to_remove:                            # remove the things that are not visible by the agent
        things.remove(thing)

    # printing agent current state
    print(agent)
    # printing enviroment state
    self.stateRender.printEnvironment(agent = agent)
    # printing agent performance
    print('Agent performance: ' + (str(agent.performance)))
    print('\n')
    # printing agent percept
    self.stateRender.printAgentPercept(agent = agent, percepts=percepts)
    print('\n')

    return things, percepts

  # add_thing
  # add a thing to the environment (Support things Agent, Gold, and Trap)
  # @param {Agent|Trap|Gold} thing      (required)
  # @param {Tuple} location (row, col)  (optional)
  # @return {Void}
  def add_thing(self, thing, location = None):
    # set random location if not provided
    thing.location = location if location is not None else self.default_location(thing)

    # if thing is instance of Agent
    if (isinstance(thing, Agent)):
      self.state[thing.location[0]*5 + thing.location[1]]["A"] += 1             # update enviroment state based on location
      thing.performance = 100                                                   # set agent performance
      thing.currentDirection = Direction(randomDirection())                     # set agent direction
      if (isinstance(thing, ModelReflexAgent)):                                 # if agent is a ModelReflexAgent
        thing.visited.add(thing.location)                                       # add current location as visited
      self.agents.append(thing)                                                 # register agent
    else:
      if (isinstance(thing,Gold)):                                              # if instance of gold
        self.state[thing.location[0]*5 + thing.location[1]]["G"] += 1           # update enviroment state based on location
      else:
        self.state[thing.location[0]*5 + thing.location[1]]["T"] += 1           # if instance of trap  
      self.things.append(thing)                                                 # update enviroment state based on location

  # execute_action
  # executes an allowed agent action
  # @param {Agent} agent (required)
  # @param {String} action (TURN|ADVANCED|STAY)
  def execute_action(self, agent, action):
    self.STEP_COUNT = self.STEP_COUNT + 1                                       # update agent step counter
    # agent is Model-based reflex 
    # print agent's internal state
    if isinstance(agent, ModelReflexAgent):           
      self.stateRender.printAgentState(agent)
      print('\n')
    # print current step
    print('<STEP %s>' % (self.STEP_COUNT))
    # print selected action
    print('SELECT ACTION: %s' % (action))

    if action == TURN:                                                          # if action is TURN
      agent.turn()                                                              # call agent turn method
      self.consumeThingsAtAgentLocation(agent)                                  # consume things at agent location
    elif action == ADVANCED:                                                    # if action is ADVANCED
      previousLocation = agent.location                                         # move agent
      if agent.forward():                                                       # if agent moved
        self.state[previousLocation[0] * 5 + previousLocation[1]]['A'] = 0      # update enviroment state based on new agent location
        self.state[agent.location[0] * 5 + agent.location[1]]['A'] = 1

      self.consumeThingsAtAgentLocation(agent)                                  # consume things at agent location
    elif action == STAY:                                                        # if action is STAY
      self.consumeThingsAtAgentLocation(agent)                                  # consume things at agent location                                  

  # generate a random location for the given thing
  # @return {Tuple} (row, col)
  def default_location(self, thing):
    # generate random x, y
    x = random.randint(0, self.MAX_WIDTH - 1)
    y = random.randint(0, self.MAX_HEIGHT - 1)
    return (x, y)

  # consumeThingsAtAgentLocation
  # consume things at agent location (modifies agent's performance based on the thing at the given location)
  # @param {Agent} agent
  # @return {Void}
  def consumeThingsAtAgentLocation(self, agent):
    ores = self.list_things_at(agent.location, Gold)                          # retrieve gold items
    traps = self.list_things_at(agent.location, Trap)                         # retrieve trap items

    # if gold items
    # update enviroment state based on gold item location
    # delete gold item from things
    # update agent performance
    if len(ores) > 0:
      ore = ores[0]
      self.state[ore.location[0] * 5 + ore.location[1]]['G'] = self.state[ore.location[0] * 5 + ore.location[1]]['G'] - 1
      self.delete_thing(ore)
      agent.modifyPerformance(10)

    # if traps items
    # update enviroment state based on trap item location
    # delete trap item from things
    # update agent performance
    if len(traps) > 0:
      trap = traps[0]
      self.state[trap.location[0] * 5 + trap.location[1]]['T'] = self.state[trap.location[0] * 5 + trap.location[1]]['T'] - 1
      self.delete_thing(traps[0])
      agent.modifyPerformance(-5)

  # isFullyObservable
  # returns true if the enviroment type is FULLY_OBSERVABLE
  # @return {Boolean}
  def isFullyObservable(self):
    return self.envType == FULLY_OBSERVABLE
