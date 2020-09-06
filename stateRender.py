# Strategy class
# this is used to create complex
# printings
class Strategy: 
    def print(self):
        raise NotImplementedError

# MissingStrategy class 
class MissingStrategy(Exception):
    def __init__(self, message = 'Strategy is required'):
        self.message = message

# StateRender class
# performs a printing based on the given strategy
class StateRender:
    def __init__(self, strategy = None):
        if not strategy:
            raise MissingStrategy()
        
        if not isinstance(strategy, Strategy):
            raise MissingStrategy('Given strategy must extend from Strategy')

        self.printingStrategy = strategy

    def print(self):
        self.printingStrategy.print()
