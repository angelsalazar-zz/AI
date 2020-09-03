from agents import Environment
from agents import Agent
from agents import Direction
from items import Gold
from items import Trap
from agentsImpl import SimpleReflexAgent


import random

TURN = 'Turn'
ADVANCED = 'Advance'
STAY = 'Stay'

class Grid(Environment):
    printGrid = []

    def __init__(self, envType = 'FULLY'):
        super(Grid, self).__init__()
        for i in range(25):
          self.printGrid.append({"A":0,"G":0,"T":0})
        self.envType = envType
        self.MAX_WIDTH = self.MAX_HEIGHT = 5

    def thing_classes(self):
        return [SimpleReflexAgent, Trap, Gold]  # List of classes that can go into environment

    def __str__(self):
        r = ""
        for i in self.printGrid:
            r += str(i)+"\n"
        return r


    def percept(self, agent):
        things = self.things;

        if self.envType == 'FULLY':
            pass
        
        # Only retrieves things visible
        if self.envType == 'PARTIALLY':
            movements = [(1,0),(1,1),(0,1),(-1,-1),(-1,0),(0,-1),(-1,1),(1,-1)]
            percepts = []
            for m in movements:
                newX = agent.location[0] + m[0]
                newY = agent.location[1] + m[1]
            if newX < 5 and newX >= 0 and newY < 5 and newY >= 0:
                percepts.append((newX,newY))

            for thing in things:
                if ((thing.location[0],thing.location[1]) not in percepts):
                    things.remove(thing)

        print(things)
        return things

    def add_thing(self, thing, location = None):
        # set random location if not provided
        thing.location = location if location is not None else self.default_location(thing)

        print(thing.location)
        # if thing is instance of Agent
        if (isinstance(thing, Agent)):
            self.printGrid[thing.location[0]*5 + thing.location[1]]["A"] += 1
            # initialize thing's perform
            thing.performance = 100
            # register agent
            self.agents.append(thing)
        else:
            if (isinstance(thing,Gold)):
                self.printGrid[thing.location[0]*5 + thing.location[1]]["G"] += 1
            else:
                self.printGrid[thing.location[0]*5 + thing.location[1]]["T"] += 1
            # register thing 2
            self.things.append(thing)

    def execute_action(self, agent, action):
        if action == TURN:
            agent.turn()
        elif action == ADVANCED:
            agent.forward()
            self.consumeThingsAtAgentLocation(agent)
        elif action == STAY:
            self.consumeThingsAtAgentLocation(agent)

    # generatas a random location for the given thing
    def default_location(self, thing):
        # generate random x, y, and default direction
        x = random.randint(0, self.MAX_WIDTH - 1);
        y = random.randint(0, self.MAX_HEIGHT - 1);
        d = Direction(Direction.R)

        # if initialAgentLocation is given and given thing is instance of agent
        if (self.initialAgentLocation and isinstance(thing, Agent)):
            # initialize agent at specific location
            x = self.initialAgentLocation.x
            y = self.initialAgentLocation.y
            d = self.initialAgentLocation.d

        # return thing direction
        return (x, y, d)

    def consumeThingsAtAgentLocation(self, agent):
        traps = self.list_things_at(agent.location, Trap)
        if len(traps) > 0:
            self.delete_thing(traps[0])
            agent.modifyPerformance(-5)

        ores = self.list_things_at(agent.location, Gold)
        if len(ores) > 0:
            self.delete_thing(ores[0])
            agent.modifyPerformance(10)
