def buildCell(cell, agent):
    agentCount = agent.currentDirection.direction[0:1] if cell['A'] > 0 else '-'
    goldCount = str(cell['G']) if cell['G'] != 0 else '-'
    trapCount = str(cell['T']) if cell['T'] != 0 else '-'
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


class StateRenderer:
    def __init__(self, env = None):
        self.env = env

    def render(self, start = 0, end = 5, agent = None):
        offset = '  '
        indexes, headers = buildHeaders(start, end)
        matrix = [offset + indexes, offset + headers]
        print(self.env)
        for i in range(start, end):
            cells = []
            for j in range(end - start):
                cells.append(buildCell(self.env.state[j + 5 * i], agent))
            matrix.append(str(i) + ' ' + (' '.join(cells)))
        print('\n'.join(matrix))
        
    def printEnvironment(self, agent):
        self.render(agent=agent)

    def printAgentPercept(self, agent, things, percepts):
        print('PERCEPT')
        # print enviroment and exiting early
        # if env is fully observable
        if self.env.isFullyObservable():
            self.printEnvironment(agent=agent)
            return
        # (row, column)
        # agent.location
        print(percepts)

    def printAgentState(self, agent):
        print('AGENT\'S INTERNAL STATE')
        # pass
