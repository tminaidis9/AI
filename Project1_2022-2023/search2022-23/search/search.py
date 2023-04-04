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
from operator import truediv
from turtle import distance
from util import Stack
from util import Queue
from util import PriorityQueue 
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from game import Actions, Directions
import util
import math
import time

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

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
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

def depthFirstSearch(problem: SearchProblem):
#   Search the deepest nodes in the search tree first.
#   Your search algorithm needs to return a list of actions that reaches the
#   goal. Make sure to implement a graph search algorithm.
#   To get started, you might want to try some of these simple commands to
#   understand the search problem that is being passed in: 
#   "*** YOUR CODE HERE ***"

    # return acts
    mystate = (problem.getStartState(),[])
    state = mystate[0]
    path = mystate[1]
    stack = [mystate]
    expanded = []

    while(len(stack) > 0):
        
        state,path = stack.pop()
        if problem.isGoalState(state):
            return path
        
        if state not in expanded:
            expanded.append(state)
            for newstate,move,cost in problem.getSuccessors(state):  
                stack.append((newstate,path + [move]))
                
    return path


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    mystate = (problem.getStartState(),[])
    queue = Queue() # queue with nodes that i am searching every time
    expanded = [] # all the expanded nodes
    queue.push(mystate)


    while(not queue.isEmpty()):
        mystate = queue.pop()
        state = mystate[0]
        path = mystate[1]

        if problem.isGoalState(state):
            return path
                
        if state not in expanded:
            expanded.append(state)  
            for newstate,move,cost in problem.getSuccessors(state):
                queue.push((newstate,path + [move]))
    

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    pq = PriorityQueue()
    mystate = (problem.getStartState(),[])
    expanded = []
    pq.push((mystate,0),0)

    while(not pq.isEmpty()):
        state_priority = pq.pop()
        mystate = state_priority[0]
        priority = state_priority[1]
        state = mystate[0]
        path = mystate[1]

        if problem.isGoalState(state):
            return path
        
        if state not in expanded:
            expanded.append(state)
            for newstate,move,cost in problem.getSuccessors(state):
                mynewstate = (newstate, path + [move])
                newpriority = priority + cost
                pq.push((mynewstate,newpriority),newpriority)

    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    if heuristic == nullHeuristic :
        return uniformCostSearch(problem)
    
    pq = PriorityQueue()
    mystate = (problem.getStartState(),[],0)
    expanded = []
    pq.push(mystate,heuristic(mystate[0],problem))

    while not pq.isEmpty():
        mystate = pq.pop()
        state = mystate[0]
        path = mystate[1]
        cost = mystate[2]

        if problem.isGoalState(state):
            return path

        if state not in expanded:
            expanded.append(state)
            for newstate,move,newcost in problem.getSuccessors(state):
                totalcost = cost + newcost
                pq.push((newstate,path+[move],totalcost),totalcost + heuristic(newstate,problem))



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
