from agents import Agent
from agents import Direction

class SimplyReflexAgent(Agent):

  def modifyPerformance(self, amount):
    self.performance += amount
  
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

    pass