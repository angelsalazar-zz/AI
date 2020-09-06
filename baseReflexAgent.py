from agents import Agent
from agents import Direction
from items import Trap
from allowActions import TURN
from allowActions import ADVANCED
from allowActions import STAY


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


class BaseReflexAgent(Agent):
    def __init__(self, program):
        super(BaseReflexAgent, self).__init__(program)
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
        self.currentDirection = self.currentDirection + Direction.R

    def forward(self):
        raise NotImplementedError