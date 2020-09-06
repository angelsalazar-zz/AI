def buildCell(cell, agent, mark = '-'):
    if mark == '?':
        return ('(%s %s %s)' % (mark, mark, mark))

    if mark == 'V':
        agentCount = mark
        goldCount = str(cell['G']) if cell['G'] > 0 else '-'
        trapCount = str(cell['T']) if cell['T'] > 0 else '-'
        return ('(%s %s %s)' % (agentCount, goldCount, trapCount))

    agentCount = agent.currentDirection.direction[0:1] if cell['A'] > 0 else '-'
    goldCount = str(cell['G']) if cell['G'] > 0 else '-'
    trapCount = str(cell['T']) if cell['T'] > 0 else '-'

    return ('(%s %s %s)' % (agentCount, goldCount, trapCount))
    

def buildHeaders(start=0, end=5):
    indexes = []
    headerTmpl = '(A G T)'
    headers = []
    
    for _ in range(start, end):
        indexes.append('   %s   ' % start)
        headers.append(headerTmpl)
        start += 1
    
    return (' '.join(indexes)), (' '.join(headers))


def toIndex(location):
    pass

class StateRenderer:
    def __init__(self, env = None):
        self.env = env

    def render(self, startingPoint = (0, 0), endPoint = (4, 4), agent = None, visibilityChecker = None):
        offset = '  '
        indexes, headers = buildHeaders(startingPoint[1], endPoint[1] + 1)
        matrix = [offset + indexes, offset + headers]
        
        for row in range(startingPoint[0], endPoint[0] + 1):
            cells = []
            for col in range(startingPoint[1], endPoint[1] + 1):
                mark = visibilityChecker((row, col)) if visibilityChecker else '-'
                cells.append(
                    buildCell(
                        cell = self.env.state[col + 5 * row],
                        agent = agent,
                        mark = mark
                    )
                )
            matrix.append(str(row) + ' ' + (' '.join(cells)))
        print('\n'.join(matrix))
        
    def printEnvironment(self, agent):
        self.render(agent = agent)

    def printAgentPercept(self, agent, percepts):
        print('PERCEPT')
        # print enviroment and exiting early
        # if env is fully observable
        if self.env.isFullyObservable():
            self.printEnvironment(agent=agent)
            return
        
        print(percepts)
        firstPercept = percepts[0]
        lastPercept = percepts[len(percepts) - 1]
        # special scenarios
        # top left corner
        if agent.location == (0,0):
            firstPercept = agent.location

       # bottom right conter
        if agent.location == (4, 4):
            lastPercept = agent.location

        self.render(startingPoint = firstPercept, endPoint = lastPercept, agent = agent)
        

    def printAgentState(self, agent):
        def checkVisibility(coords):
            if agent.visited.intersection({coords}):
                return 'V'
            
            if not agent.visible.intersection({coords}):
                return '?'

            return '-'

        print('AGENT\'S INTERNAL STATE')
        self.render(agent = agent, visibilityChecker = checkVisibility)
        



