from agents import Thing

# Thing class
class Item(Thing):
  def __init__(self, points = 0):
    self.points = points

# Trap class
class Trap(Item):
  def __init__(self):
    super(Trap, self).__init__(-5)

# Gold class
class Gold(Item):
  def __init__(self):
    super(Gold, self).__init__(10)
  
