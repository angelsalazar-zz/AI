from agents import Agent
from agents import Direction

from envImpl import TURN
from envImpl import ADVANCED
from envImpl import STAY

# act only based on the current perception
# ignore the rest of percept history
# based on if-then rules
# environment should be fully observable

def simpleReflexAgentProgram(percept):
    status
    if ()
    pass
    # location, status = percept
    # if status == 'Dirty':
    #     return 'Suck'
    # elif location == loc_A:
    #     return 'Right'
    # elif location == loc_B:
    #     return 'Left'

class SimpleReflexAgent(Agent):
    def __init__(self, envType = 'FULLY', initialAgentLocation = None):
      super(SimpleReflexAgent, self).__init__(program=simpleReflexAgentProgram)

    def modifyPerformance(self, amount):
        self.performance += amount

    def checkBounds():
        newX, newY = None
        if (currentDir.direction == Direction.U):
          newX = self.location[0] - 1
        elif (currentDir.direction == Direction.R):
          newY = self.location[1] + 1
        elif (currentDir.direction == Direction.B):
          newX = self.location[0] + 1
        elif (currentDir.direction == Direction.L):
          newY = self.location[1] - 1

        if newX < 0 or newY < 0 or newX >= 5 or newY >= 5:
          return None
        else:
          return (newX,newY,self.location[2])

    def turn(self):
        self.modifyPerformance(-1)
        currentDir = self.location[2];
        # d + Direction.R
        if (currentDir.direction == Direction.U):
          currentDir = currentDir + Direction.R
        elif (currentDir.direction == Direction.R):
          currentDir = currentDir + Direction.B
        elif (currentDir.direction == Direction.B):
          currentDir = currentDir + Direction.L;
        elif (currentDir.direction == Direction.L):
          currentDir = currentDir + Direction.U;

    def forward(self):
        self.modifyPerformance(-1)
        newLocation = self.checkBounds()
        if newLocation:
          self.location = newLocation
