from agents import Thing

class Item(Thing):
  def __init__(self, points = 0):
    self.points = points

class Trap(Item):
  def __init__(self):
    super(Trap, self).__init__(-5)

class Gold(Item):
  def __init__(self):
    super(Gold, self).__init__(10)
  
