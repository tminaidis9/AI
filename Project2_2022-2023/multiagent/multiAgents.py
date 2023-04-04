# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util, math

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best action
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        oldFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        x,y = newPos
        evaluation_num = float(0)
        #check how many ghosts are close to new position
        for state in newGhostStates:
            x1,y1 = state.getPosition()
            distance = abs(x-x1) + abs(y-y1)

            if newPos in oldFood.asList():
                evaluation_num += 1
            
            if newScaredTimes[0] > 0 :
                evaluation_num += distance
            
            if distance < 3:
                evaluation_num -= 3
        
        closestfood = []
        for x2,y2 in oldFood.asList():
            fooddist = abs(x-x2) + abs(y-y2)
            closestfood.append(fooddist)
        evaluation_num -=  0.1 * min(closestfood)

        return evaluation_num
        
def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)
        successorsGameState = [gameState.generateSuccessor(0,act) for act in legalMoves]
        maxnum = -math.inf
        statenum = 0
        for num in range(len(successorsGameState)):
            result = self.value(successorsGameState[num],0,1)
            if result > maxnum:
                maxnum = result
                statenum = num
        return legalMoves[statenum]
        
    def value(self,gameState: GameState,dpth,Index):
        if (dpth  == self.depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if Index == 0 : #for max
            return self.max_value(gameState,dpth,Index)
        else: #for min
            return self.min_value(gameState,dpth,Index)

    def max_value(self,gameState: GameState,dpth,index):
        legalMoves = gameState.getLegalActions(index)
        successorsGameState = [gameState.generateSuccessor(index,act) for act in legalMoves]
        x = -200000000
        for GState in successorsGameState:
            x = max(x,self.value(GState,dpth,1))
        return x
    
    def min_value(self,gameState: GameState,dpth,Index):
        legalMoves = gameState.getLegalActions(Index)
        successors = [gameState.generateSuccessor(Index,act) for act in legalMoves]
        x = 200000000
        for succ in successors:
            if (Index == gameState.getNumAgents() - 1) :
                x = min(x,self.value(succ,dpth + 1,0))
            else:
                x = min(x,self.value(succ,dpth,Index + 1))
        return x

        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState:GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = -math.inf
        b = math.inf
        legalMoves = gameState.getLegalActions(0)
        successorsGameState = [gameState.generateSuccessor(0,act) for act in legalMoves]
        maxresult = -math.inf
        for num in range(len(successorsGameState)):
            result = self.value(successorsGameState[num],a,b,0,1) 
            if result > maxresult:
                maxresult = result
                statenum = num
                a = maxresult
        return legalMoves[statenum]

    def value(self,gameState:GameState,a,b,dpth,Index):
        if (dpth == self.depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if Index == 0 : #for max
            return self.max_value(gameState,a,b,dpth,Index)
        else: #for min
            return self.min_value(gameState,a,b,dpth,Index)

    def max_value(self,state:GameState,a,b,dpth,Index):
        v = -math.inf
        legalMoves = state.getLegalActions(Index)
        for act in legalMoves:
            succ = state.generateSuccessor(Index,act) 
            v = max(v,self.value(succ,a,b,dpth,1))
            if v > b:
                return v
            a = max(a,v)
        return v

    def min_value(self,state:GameState,a,b,dpth,Index):
        v = math.inf
        legalMoves = state.getLegalActions(Index)
        for act in legalMoves:
            succ = state.generateSuccessor(Index,act)
            if (Index + 1 == state.getNumAgents()) :
                v = min(v,self.value(succ,a,b,dpth + 1,0))
            else:
                v = min(v,self.value(succ,a,b,dpth,Index + 1))
            if v < a:
                return v
            b = min(b,v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)
        successorsGameState = [gameState.generateSuccessor(0,act) for act in legalMoves]
        results = [self.value(GState,0,1) for GState in successorsGameState]
        maxresult = max(results)
        for num in range(len(results)):
            if results[num] == maxresult:
                return legalMoves[num]

    def value(self,gameState:GameState,dpth,Index):
        if (dpth == self.depth) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if Index == 0 : #for max
            return self.max_value(gameState,dpth,Index)
        else: #for min
            return self.chance_value(gameState,dpth,Index)

    def max_value(self,state:GameState,dpth,Index):
        v = -math.inf
        legalMoves = state.getLegalActions(Index)
        for act in legalMoves:
            succ = state.generateSuccessor(Index,act) 
            v = max(v,self.value(succ,dpth,1))
        return v
    
    def chance_value(self,state:GameState,dpth,Index):
        legalMoves = state.getLegalActions(Index)
        num_of_moves = len(legalMoves)
        total = 0
        for act in legalMoves:
            succ = state.generateSuccessor(Index,act) 
            if Index + 1 == state.getNumAgents():
                total += self.value(succ,dpth + 1,0) 
            else:
                total += self.value(succ,dpth,Index + 1)
        return total / num_of_moves


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
