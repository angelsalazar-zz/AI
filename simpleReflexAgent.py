from agents import Agent
from agents import Direction

class SimpleReflexAgent(Agent):

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
