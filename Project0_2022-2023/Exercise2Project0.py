import imp
from multiprocessing import heap
import optparse
import os
import queue
import re
import sys
import random
import json
import math

import heapq

class PriorityQueue: # Class PriorityQueue
    
    def __init__(self) -> None: # Initialization
        self.count = 0 #counter
        self.heap = [] # heap with tuples
        heapq.heapify(self.heap) # init heap

    def push(self,item,priority):
        PriorityQueue.update(self,item,priority) #using the update func to push items

    def pop(self):
        self.count -= 1 
        task = heapq.heappop(self.heap) # pop the smaller element from heap
        return task[1] #return the name of the task we just pop

    def isEmpty(self): 
        if (self.count == 0):
            return True
        else:
            return False

    def update(self,item,priority):
        list = heapq.nlargest(self.count,self.heap) #list of elements what heap has
        exist = 0 #if element already exist in heap with bad priority
        for items in list: # check the elements in heap
            if (items[1] == item): #if this item exist 
                exist = 1
                if(items[0] > priority): #and the new element has better priority.If our new element hasn't better priority, we do nothing
                    new_heap = []
                    heapq.heapify(new_heap) #make a new heap without the old element
                    for pqitems in self.heap:
                        new_item = self.heap.pop()  
                        if (new_item[1] == item): #find the old one and threw it
                            continue
                        heapq.heappush(new_heap,new_item) #copy all the other elements
                    pair = (priority,item) # last, add the new element
                    heapq.heappush(new_heap,pair)
                    self.heap = new_heap #and that's our new heap

        
        if (exist != 1): # if the element doesn't exist, just add it in the list
            self.count += 1
            pair = (priority,item)
            heapq.heappush(self.heap,pair)
        

def PQSort(list):
    pq = PriorityQueue()
    for items in list:
        pq.push(items,items)
    return(pq)

# text for checking the use of PriorityQueue
if __name__ == "__main__":
    pqueue = PriorityQueue()
    pqueue.push("task1",1)
    print(pqueue.isEmpty())
    pqueue.push("task1",2)
    pqueue.push("task0",0)
    t = pqueue.pop()
    print(t)
    t = pqueue.pop()
    print(t)
    pqueue.push("task3", 3)
    pqueue.push("task3", 4)
    pqueue.push("task2", 0)
    t = pqueue.pop()
    print(t)
    list = [2,5,8,3,2]
    pq = PQSort(list)
    print(pq.pop())
    print(pq.pop())
    print(pq.pop())
    print(pq.pop())
    print(pq.isEmpty())





