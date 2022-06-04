# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from pacman import GameState
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    frontier = util.Queue() #isws prepei stack
    father_state = problem.getStartState()
    problem.expand(problem.getStartState())
    frontier.push(father_state)
    dictionary = {}
    path = []
    fath_dictionary = {}

    while (frontier.isEmpty() == False): #

        # state = node # //////////// οταν το φτιαξεις δεν θα χρειαζεσαι το φροντιερ,  
                                    # θα έχεις ήδη το στέιτ από πριν
        state = frontier.pop()
        actions = problem.getActions(state)
        # print(state, 133)
        
        if( state not in dictionary.keys()):
            dictionary.update({state:actions})

        goal_reached = problem.isGoalState(state)
        
        if (len(actions) < 1):
            #
            frontier.push(fath_dictionary[state])              ########################if (problem.getNextState(state,fkid)) in dictionary.keys():
            path.pop(-1)
            continue                                 ###############################continue
            
        if goal_reached:
            return path
            
        for act in actions:
            # print(147)
            nextkid = problem.getNextState(state,act)
            # print(nextkid)
            fath_dictionary.update({nextkid:state})

            if nextkid not in dictionary.keys():
                # print(152)
                path.append(act)
                if problem.isGoalState(nextkid):
                    return path
                frontier.push(nextkid)
                problem.expand(nextkid) # isws thelei elegxo gia ta expand //////////////////////////////
                break                  ######kai ena continue ginetai amesa
            else:
                # print(160)
                continue

        # print(dictionary , "dict updated")
    return path



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    father_state = problem.getStartState()
    problem.expand(problem.getStartState())
    frontier.push(father_state)
    dictionary = {}
    fath_dictionary = {father_state:father_state}
    path = []

    while (frontier.isEmpty() == False): # Μέχρι να μην υπάρχουν άλλα παιδιά να εξερευνήσει
        
        state = frontier.pop()

        actions = problem.getActions(state)
        dictionary.update({state:actions}) # Αποθήκευσε τις actions κάθε state σε ένα dictionary για ευκολότερη πρόσβαση
        
        if (len(actions) < 1): # Δεν υπάρχουν άλλες κινήσεις να κάνει
            continue           
            
        for act in actions:             
            kid = problem.getNextState(state,act)

            if ( kid in dictionary.keys()):
                continue
            
            fath_dictionary.update({kid:state})
            
            if problem.isGoalState(kid):
                while kid != state : # Δημιουργώ αντίθετα το path και το κάνω μετά reverse
                    father_actions = dictionary[state]     
                    for act in father_actions:
                        if problem.getNextState(state,act) == kid :
                            path.append(act)
                            break
                    kid = state
                    state = fath_dictionary[kid]
                path.reverse()
                print(path)
                return path
                
            if kid not in dictionary.keys():
                dictionary.update({kid:actions})
                frontier.push(kid)

            problem.expand(kid)
        
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    frontier = util.PriorityQueue()                #i use priority queue
    father_state = problem.getStartState()
    # print("acts", problem.getActions(father_state))
    frontier.push(father_state,0)
    dictionary = {}
    total_path_dictionary = {}
    fath_dictionary = {father_state:father_state}
    path = []
    expanded = []
    # num = 0 #trick to working for problem 3
    # finish = 0

    while (frontier.isEmpty() == False): # Μέχρι να μην υπάρχουν άλλα παιδιά να εξερευνήσει
        
        state = frontier.pop()

        actions = problem.getActions(state) # actions that state can do
        dictionary.update({state:actions}) # Αποθήκευσε τις actions κάθε state σε ένα dictionary για ευκολότερη πρόσβαση
        
        if problem.isGoalState(state):
            kid = state
            state = fath_dictionary[kid]
            while kid != state: # Δημιουργώ αντίθετα το path και το κάνω μετά reverse
                father_actions = dictionary[state]
                for act in father_actions:
                    if problem.getNextState(state,act) == kid :
                        path.append(act)
                        break
                kid = state
                state = fath_dictionary[kid]
            path.reverse()
            return path

        if state not in expanded: #expand only the unexpanded states
            problem.expand(state)
            expanded.append(state)

        if (len(actions) < 1): # Δεν υπάρχουν άλλες κινήσεις να κάνει
            continue

        for act in actions:             #for every action
            kid = problem.getNextState(state,act)
            if ( kid in dictionary.keys()): #check if kid is on dict
                father = fath_dictionary[kid]
                father_act = dictionary[father]
                if (father != kid and problem.getActionCost(state,act,kid)):
                    for acts in father_act: #check if we find a better way to go in this state
                        if problem.getNextState(father,acts) == kid:
                            if (state in total_path_dictionary.keys()) and (father in total_path_dictionary.keys()):
                                sum1 = (problem.getActionCost(state,act,kid) + total_path_dictionary[state])
                                sum2 = (problem.getActionCost(father,acts,kid) + total_path_dictionary[father])
                            else:
                                sum1 = problem.getActionCost(state,act,kid)
                                sum2 = problem.getActionCost(father,acts,kid)
                            if sum1 < sum2:
                                fath_dictionary.update({kid:state})
                                frontier.push(kid,sum1)
                        
                continue
            
            fath_dictionary.update({kid:state})
                
            if kid not in dictionary.keys(): #do the type of A*
                dictionary.update({kid:actions})
                if (heuristic != nullHeuristic):
                        num = heuristic(kid,problem)
                else:
                    num = 0
                distance = (problem.getActionCost(state,act,kid)+num) #distance + heur_num
                if state in total_path_dictionary.keys():
                    distance += total_path_dictionary[state]
                frontier.push(kid,distance)
                total_path_dictionary.update({kid:distance-num}) # (distance-num): the clear distance

    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
