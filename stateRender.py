# buildCell
# gets a string of the given cell
# @param {Map} cell ({A:Integer, G:Integer, T:Integer})
# @param {Agent} agent
# @param {String} mark (default -)
# @return {String}
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
    
# buildHeaders
# build the state headers
# @param {Integer} start column to start (default 0)
# @param {Integer} end column to end (not inclusive, default 5)
# @return {Tuple} (indexes:String, headers:String)
def buildHeaders(start=0, end=5):
    indexes = []
    headerTmpl = '(A G T)'
    headers = []
    
    for _ in range(start, end):
        indexes.append('   %s   ' % start)
        headers.append(headerTmpl)
        start += 1
    
    return (' '.join(indexes)), (' '.join(headers))


# StateRenderer class
# used to display the enviroment state, agent's internal state, and agent's percept
class StateRenderer:
    # initialize state renderer variables
    # @param {Grid} env (required)
    def __init__(self, env = None):
        self.env = env

    # render
    # displays the enviroment state, agent's internal state, and agent's percept 
    # @param {Tuple} startingPoint
    # @param {Tuple} endPoint
    # @param {Agent} agent
    # @param {Function} visibilityChecker
    # @retunr {Void}
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

    # printEnvironment
    # displays the enviroment state
    # @param {Agent} agent
    # @retunr {Void} 
    def printEnvironment(self, agent, visibilityChecker = None):
        self.render(agent = agent, visibilityChecker = visibilityChecker)

    # printAgentPercept
    # displays the agent's percept
    # @param {Agent} agent
    # @param {List<Tuple>} percepts
    # @retunr {Void} 
    def printAgentPercept(self, agent, percepts):
        print('PERCEPT')
        # print enviroment and exiting early
        # if env is fully observable
        if self.env.isFullyObservable():
            self.printEnvironment(agent=agent)
            return
    
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
        
    # printAgentState
    # displays the agent's internal state (Supported only for Model based reflex agents)
    # @param {Agent} agent
    # @retunr {Void} 
    def printAgentState(self, agent):
        def checkVisibility(coords):
            if agent.visited.intersection({coords}):
                return 'V'
            
            if not agent.visible.intersection({coords}):
                return '?'

            return '-'

        print('AGENT\'S INTERNAL STATE')
        self.render(agent = agent, visibilityChecker = checkVisibility)
        



