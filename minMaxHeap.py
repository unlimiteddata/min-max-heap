# Amira Isenberg
# The Big Homework, Spring 2022

# I hereby certify that this program is solely the result of my own 
# work and is in compliance with the Academic Integrity policy of the 
# course syllabus and the academic integrity policy of the CS 
# department.

import random
import pytest
import math

## helper functions:
# calculate the left child index of i:
def leftChild(i):
    return 2 * i + 1

# calculate the right child index of i:
def rightChild(i):
    return 2 * i + 2

# calculate the parent index of i:
def parent(i):
    return (i-1) // 2

# calculate the grandparent index of i:
def grandparent(i):
    return (i-3) // 4

# calculate the leftmost grandchild index of i:
def LLgrandchild(i):
    return 4 * i + 3

# calculate the rightmost grandchild index of i:
def RRgrandchild(i):
    return 4 * i + 6

# calculate the level/depth of i:
def level(i):
    return math.floor(math.log2(i+1))

class Node(object):
    def __init__(self,k,d):
        self.key  = k
        self.data = d
        
    def __str__(self):
        return "(" + str(self.key) + "," + repr(self.data) + ")"  
    
class minMaxHeap(object):
    def __init__(self,size):
        self.__arr = [None] * size
        self.__nElems = 0
        
    def __len__(self):
        return self.__nElems
    
    # Remove the minimum key and then return the removed key/data 
    # pair:    
    def removeMin(self):
        # empty heap, so nothing is removed:
        if self.__nElems == 0: return None, None
        
        # the minimum node will always be the root node:
        root = self.__arr[0]
        self.__nElems -= 1 
        
        # place the last node in the heap into the root location and
        # call trickleDown on the root index to restore the min-max 
        # heap property:
        self.__arr[0] = self.__arr[self.__nElems]
        self.__arr[self.__nElems] = None # garbage collection
        self.__trickleDown(0)
        
        # return the key/data pair of the removed node:
        return root.key, root.data
    
    # Remove the maximum key and then return the removed key/data 
    # pair:     
    def removeMax(self):
        size = self.__nElems 
        
        # empty heap, so nothing is removed:
        if size == 0: return None, None
        
        # if the heap has only one node, it must be the max:
        if size == 1:
            big = self.__arr[0]
            self.__nElems -= 1
            
            self.__arr[0] = None # garbage collection
            
            return big.key, big.data
        
        # otherwise, the max is one of the children of the root.
        
        # the only possible indexes for the children of the root are 1 
        # for the left child (which definitely exists) and 2 for the 
        # right child (which may not exist):
        left  = 1
        right = 2
        
        # since the heap must have at least 2 nodes, the second node
        # in the array must be the left child:
        m = left
        
        # if the right child exists and is greater than the left child,
        # store that as the greater child:
        if right < size and \
           self.__arr[right].key > self.__arr[left].key:
            m = right   
            
        # m is now the index of the largest child of the root (and the 
        # maximum key in the heap).
        big = self.__arr[m]
        self.__nElems -= 1 
        
        # place the last node in the heap into the location of m and
        # call trickleDown on the index of the replaced maximum to 
        # restore the min-max heap property:
        self.__arr[m] = self.__arr[self.__nElems]
        self.__arr[self.__nElems] = None  # garbage collection
        self.__trickleDown(m)
        
        # return the key/data pair of the removed node:
        return big.key, big.data
    
    def insert(self,k,d):
        # doesn't insert anything and fails if the heap is full:
        if self.__nElems == len(self.__arr): return False
        
        # otherwise, place the new node at the end of the heap and 
        # call trickle up on the index of the newly added key:
        self.__arr[self.__nElems] = Node(k,d)
        self.__trickleUp(self.__nElems)
        self.__nElems += 1
        
        # returns True because it succeeds if the heap isn't full:
        return True
    
    def __trickleDown(self,i=0):
        if level(i) % 2 == 0: # even (min) level
            self.__trickleDownMin(i)
        else:  # odd (max) level
            self.__trickleDownMax(i)
        
    def __trickleDownMax(self,i=0):
        size = self.__nElems
        
        # left and right are the calculated indexes of the left and 
        # right children of i, respectively:
        left  = leftChild(i)
        right = rightChild(i)
        
        # if i has at least one child:
        if left < size:
            # first, find which child is bigger.
            
            # the greatest node so far is the left child (since the 
            # right child may not exist):            
            m = left
            
            # if the right child exists and is greater than the left 
            # child, store that as the greater child:
            if right < size and \
               self.__arr[right].key > self.__arr[left].key:
                m = right
                
            # m is now the index of the largest child of i.
            
            # next, check if any of the grandchildren of i are bigger.
            
            # variable to use for testing if m is a grandchild:
            gc = False
            
            # if there is at least one grandchild:
            if LLgrandchild(i) < size:
            
                # end point for the loop (either go to the index of 
                # the rightmost grandchild or just to the end of the 
                # heap array, whichever comes first): 
                end = min(RRgrandchild(i)+1,size)
                
                # check the grandchildren of i to see if any of them are
                # greater than the previously selected largest child. 
                # if so, store that as the greatest child/grandchild: 
                for x in range(LLgrandchild(i),end):
                    if self.__arr[x].key > self.__arr[m].key:
                        gc = True
                        m  = x 
                
            # m is now the index of the largest child/grandchild of i.
            
            # if m is a grandchild of i:
            if gc:
                # if the grandchild's key is greater than i's key, 
                # that violates the min-max heap property, so swap them:
                if self.__arr[m].key > self.__arr[i].key:
                    self.__arr[m],self.__arr[i] = \
                        self.__arr[i], self.__arr[m]
                    
                    # if the grandchild's parent's key is greater 
                    # than the grandchild's key, that violates the 
                    # min-max heap property, so swap them:
                    if self.__arr[parent(m)].key > self.__arr[m].key:
                        self.__arr[m],self.__arr[parent(m)] = \
                            self.__arr[parent(m)],self.__arr[m]
                     
                    # call trickleDownMax on the index of the 
                    # grandchild:   
                    self.__trickleDownMax(m)
                    
            # if m is not a grandchild of i (but rather a child), check
            # if m's key is greater than i's key. if so, that violates
            # the min-max heap property, so swap them:
            elif self.__arr[m].key > self.__arr[i].key:
                self.__arr[m], self.__arr[i] = \
                    self.__arr[i], self.__arr[m]
    
    def __trickleDownMin(self,i=0):
        size = self.__nElems
        
        # left and right are the calculated indexes of the left and 
        # right children of i, respectively:        
        left  = leftChild(i)
        right = rightChild(i)
        
        # if i has at least one child:
        if left < size:
            # first, find which child is smaller. 
            
            # the smallest node so far is the left child (since the 
            # right child may not exist):            
            m = left
            
            # if the right child exists and is smaller than the left 
            # child, store that as the smaller child:
            if right < size and \
               self.__arr[right].key < self.__arr[left].key:
                m = right
                
            # m is now the index of the smallest child of i.
            
            # next, check if any of the grandchildren of i are smaller.
            
            # variable to use for testing if m is a grandchild:
            gc = False
                   
            # if there is at least one grandchild:
            if LLgrandchild(i) < size:
            
                # end point for the loop (either go to the index of 
                # the rightmost grandchild or just to the end of the 
                # heap array, whichever comes first): 
                end = min(RRgrandchild(i)+1,size)
                
                # check the grandchildren of i to see if any of them are
                # smaller than the previously selected largest child. 
                # if so, store that as the smallest child/grandchild:  
                for x in range(LLgrandchild(i),end):
                    if self.__arr[x].key < self.__arr[m].key:
                        gc = True
                        m  = x 
                
            # m is now the index of the smallest child/grandchild of i.
            
            # if m is a grandchild of i:
            if gc:
                # if the grandchild's key is less than i's key, that 
                # violates the min-max heap property, so swap 
                # them:                
                if self.__arr[m].key < self.__arr[i].key:
                    self.__arr[m],self.__arr[i] = \
                        self.__arr[i],self.__arr[m]
                    
                    # if the grandchild's parent's key is less than 
                    # the grandchild's key, that violates the min-max 
                    # heap property, so swap them:                    
                    if self.__arr[parent(m)].key < self.__arr[m].key:
                        self.__arr[parent(m)], self.__arr[m] = \
                            self.__arr[m], self.__arr[parent(m)]
                    
                    # call trickleDownMin on the index of the 
                    # grandchild:     
                    self.__trickleDownMin(m)
                    
            # if m is not a grandchild of i (but rather a child), check
            # if m's key is less than i's key. if so, that violates
            # the min-max heap property, so swap them:
            elif self.__arr[m].key < self.__arr[i].key:
                self.__arr[m],self.__arr[i] = \
                    self.__arr[i],self.__arr[m]
    
    def __trickleUp(self,i=0):
        if i != 0:      # if i is not the root:
            if level(i) % 2 == 0: # even (min) level
                # if i's key is greater than its parent's key, that 
                # violates the min-max heap property, so swap them:
                if self.__arr[i].key > self.__arr[parent(i)].key:
                    self.__arr[parent(i)],self.__arr[i] = \
                        self.__arr[i],self.__arr[parent(i)]
                    
                    # call trickleUpMax on the index of i's parent:
                    self.__trickleUpMax(parent(i))
                 
                # otherwise, call trickleUpMin on the index of i:   
                else:
                    self.__trickleUpMin(i)
                    
            else:   # odd (max) level 
                # if i's key is less than its parent's key, that 
                # violates the min-max heap property, so swap them:
                if self.__arr[i].key < self.__arr[parent(i)].key:
                    self.__arr[parent(i)],self.__arr[i] = \
                        self.__arr[i],self.__arr[parent(i)]
                    
                    # call trickleUpMin on the index of i's parent:
                    self.__trickleUpMin(parent(i))
                
                # otherwise, call trickleUpMax on the index of i:   
                else:
                    self.__trickleUpMax(i) 
                    
    def __trickleUpMin(self,i):
        # if i has a grandparent (which would mean that the list goes 
        # at least to index 3) and i's key is less than its
        # grandparent's key, that violates the min-max heap property, 
        # so swap i and the grandparent:
        if i > 2 and \
           self.__arr[i].key < self.__arr[grandparent(i)].key: 
            self.__arr[grandparent(i)],self.__arr[i] = \
                self.__arr[i],self.__arr[grandparent(i)]            
            
            # call trickleUpMin on the index of i's grandparent:
            self.__trickleUpMin(grandparent(i))
            
    def __trickleUpMax(self,i):        
        # if i has a grandparent (which would mean that the list goes 
        # at least to index 3) and i's key is greater than its
        # grandparent's key, that violates the min-max heap property, 
        # so swap i and the grandparent:
        if i > 2 and \
           self.__arr[i].key > self.__arr[grandparent(i)].key: 
            self.__arr[grandparent(i)],self.__arr[i] = \
                self.__arr[i],self.__arr[grandparent(i)]
            
            # call trickleUpMax on the index of i's grandparent:
            self.__trickleUpMax(grandparent(i))
    
    # find the minimum node and return its key/data pair:        
    def findMin(self):
        # empty heap, so nothing is removed:
        if self.__nElems == 0: return None, None
        
        # return the key/data pair of the minimum (root) node:
        return self.__arr[0].key, self.__arr[0].data  
    
    # find the maximum node and return its key/data pair:
    def findMax(self): 
        size = self.__nElems
        
        # empty heap, so nothing is removed:
        if size == 0: return None, None
        
        # if the heap has only one node, it must be the max:
        if size == 1: 
            return self.__arr[0].key, self.__arr[0].data
        
        # otherwise, the max is one of the children of the root.
        
        # the only possible indexes for the children of the root are 1 
        # for the left child (which definitely exists, since there 
        # are at least 2 items in the heap if the code reaches this 
        # point) and 2 for the right child (which may not exist):
        left  = 1
        right = 2
        
        # the greatest node so far is the left child (since the right
        # child may not exist):
        m = left
        
        # if the right child exists and is greater than the left child,
        # store that as the greater child:
        if right < size and \
           self.__arr[right].key > self.__arr[left].key:
            m = right   
            
        # m is now the index of the largest child of the root (the 
        # maximum node in the heap).

        # return the key/data pair of the maximum node:
        return self.__arr[m].key, self.__arr[m].data 
    
    # tests if the heap satisfies the requirements of a min-max heap-
    # each node at an even level is less than its descendants, while
    # each node at an odd level is greater than its descendants:
    def isMinMaxHeap(self):
        size = self.__nElems
        i = 0
        
        # if the heap has zero or one nodes, it automatically satisfies
        # the min-max heap property, so return True:
        if size == 0 or size == 1: return True
        
        # while the current node has at least one child:
        while i < size // 2:
            # left and right are the calculated indexes of the left and 
            # right children of i, respectively:             
            left  = leftChild(i)
            right = rightChild(i)
            
            # if i is on a min (even) level, it must be less than its 
            # descendants:
            if level(i) % 2 == 0:  
                # if the left child is less than i, it does not satisfy
                # the min-max heap property, so return False:
                if self.__arr[left].key < self.__arr[i].key:
                    return False
                
                # if the right child exists and is less than i, the heap
                # doesn't satisfy the min-max heap property, so return
                # False: 
                elif right < size and \
                   self.__arr[right].key < self.__arr[i].key:
                    return False 
            
            # if i is on a max (odd) level, it must be greater than its 
            # descendants:    
            else:
                # if the left child is greater than i, the heap doesn't
                # satisfy the min-max heap property, so return False:
                if self.__arr[left].key > self.__arr[i].key:
                    return False
                
                # if the right child exists and is greater than i,
                # the heap doesn't satisfy the min-max heap property, 
                # so return False: 
                elif right < size and \
                   self.__arr[right].key > self.__arr[i].key:
                    return False
            
            # keep going through the heap: 
            i += 1 
                
        # if the code makes it here, it did not return False and thus 
        # it satisfies the min-max heap property, so return True:
        return True   

## PYTESTS: ##
 
## isHeap tests with known keys:  
    
# small min-max heap:
def test_isHeapSmall():
    size = 3
    h = minMaxHeap(size)
    h.insert(5,"3")
    h.insert(6,"f")
    h.insert(3,"s")
    
    assert h.isMinMaxHeap()

# medium min-max heap:   
def test_isHeapMedium():
    size = 50
    h = minMaxHeap(size)
    
    for i in range(size):
        key = i
        data = chr(i)
        h.insert(key,data)
    
    assert h.isMinMaxHeap()

# big min-max heap:    
def test_isHeapBig():
    size = 10000
    h = minMaxHeap(size)
    
    for i in range(size):
        key = i
        data = chr(i)
        h.insert(key,data)
    
    assert h.isMinMaxHeap()
    
    
## isHeap tests with randomly generated keys:
    
# small min-max heap (randomly generated size and keys):    
def test_isHeapSmallRandom():
    size = random.randint(2,10)
    h = minMaxHeap(size)
    
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
    
    assert h.isMinMaxHeap()

# medium min-max heap (randomly generated size and keys):      
def test_isHeapMediumRandom():
    size = random.randint(50,200)
    h = minMaxHeap(size)
    
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
    
    assert h.isMinMaxHeap()    

# big min-max heap (randomly generated size and keys):       
def test_isHeapBigRandom():
    size = random.randint(1000,100000)
    h = minMaxHeap(size)
    
    for i in range(size):
        key = random.randint(0,10000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
    
    assert h.isMinMaxHeap()   
    
# empty min-max heap:  
def test_isheapEmpty():
    h = minMaxHeap(0)
    assert h.isMinMaxHeap()
 
# min-max heap with one node:   
def test_isHeapOneNode():
    h = minMaxHeap(1)
    h.insert(18,'a')
    assert h.isMinMaxHeap()
 
 
## removeMin tests:
    
# small min-max heap (randomly generated size and keys):    
def test_removeMinSmall():
    size = random.randint(2,10)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in ascending order (min is at position 0):    
    test.sort()
    removeMin = h.removeMin()
    
    # assert that removeMin removed the minimum value:
    assert removeMin[0] == test[0]

# big min-max heap (randomly generated size and keys):        
def test_removeMinBig():
    size = random.randint(1000,100000)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:    
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in ascending order (min is at position 0):    
    test.sort()
    removeMin = h.removeMin()
    
    # assert that removeMin removed the minimum value:    
    assert removeMin[0] == test[0]

# empty min-max heap:    
def test_removeMinEmpty():
    h = minMaxHeap(0)
    
    assert h.removeMin() == (None,None)

# min-max heap with one node:
def test_removeMinOneNode():
    h = minMaxHeap(1)

    h.insert(613,"abc")
    
    removeMin = h.removeMin()
    
    assert removeMin[0] == 613
    
    
## removeMax tests:
    
# small min-max heap (randomly generated size and keys):    
def test_removeMaxSmall():
    size = random.randint(2,10)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in descending order (max is at position 0):    
    test.sort()
    test.reverse()
    
    removeMax = h.removeMax()
    
    # assert that removeMin removed the maximum value:
    assert removeMax[0] == test[0]    

# big min-max heap (randomly generated size and keys):    
def test_removeMaxBig():
    size = random.randint(1000,100000)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:    
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in descending order (max is at position 0):    
    test.sort()
    test.reverse()
    
    removeMax = h.removeMax()
    
    # assert that removeMin removed the maximum value:    
    assert removeMax[0] == test[0]    

# empty min-max heap:    
def test_removeMaxEmpty():
    h = minMaxHeap(0)
    
    assert h.removeMax() == (None,None)    

# min-max heap with one node:
def test_removeMaxOneNode():
    h = minMaxHeap(1)
    
    h.insert(7,"sdifj")
    
    removeMax = h.removeMax()
    
    assert removeMax[0] == 7  
   

## findMin tests:
    
# small min-max heap:
def test_findMinSmall():
    size = random.randint(2,10)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in ascending order (min is at position 0):    
    test.sort()
    
    findMin = h.findMin()    
    removeMin = h.removeMin()  
    
    # assert that findMin returned the same key as removeMin and that
    # it found the correct minimum value:
    assert findMin[0] == removeMin[0]
    assert findMin[0] == test[0]

# big min-max heap:
def test_findMinBig():
    size = random.randint(1000,100000)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in ascending order (min is at position 0):    
    test.sort()
    
    findMin = h.findMin()    
    removeMin = h.removeMin()  
    
    # assert that findMin returned the same key as removeMin and that
    # it found the correct minimum value:
    assert findMin[0] == removeMin[0]
    assert findMin[0] == test[0]
    
# empty min-max heap:  
def test_findMinEmpty():
    h = minMaxHeap(0)
    
    assert h.findMin() == (None,None)

# min-max heap with one node:
def test_findMinOneNode():
    h = minMaxHeap(1)
    h.insert(18,"asdfghjkl")
    
    assert h.findMin() == (18,"asdfghjkl")


## findMax tests:
    
# small min-max heap:
def test_findMaxSmall():
    size = random.randint(2,10)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in descending order (max is at position 0):    
    test.sort()
    test.reverse()
    
    findMax = h.findMax()    
    removeMax = h.removeMax()  
    
    # assert that findMax returned the same key as removeMax and that
    # it found the correct maximum value:
    assert findMax[0] == removeMax[0]
    assert findMax[0] == test[0]    

# big min-max heap:
def test_findMaxBig():
    size = random.randint(1000,100000)
    h = minMaxHeap(size)
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:
    for i in range(size):
        key = random.randint(0,1000)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data)
        test.append(key)
    
    # make the list be in descending order (max is at position 0):    
    test.sort()
    test.reverse()
    
    findMax = h.findMax()    
    removeMax = h.removeMax()  
    
    # assert that findMax returned the same key as removeMax and that
    # it found the correct maximum value:
    assert findMax[0] == removeMax[0]
    assert findMax[0] == test[0]
    
# empty min-max heap:  
def test_findMaxEmpty():
    h = minMaxHeap(0)
    
    assert h.findMax() == (None,None)

# min-max heap with one node:
def test_findMaxOneNode():
    h = minMaxHeap(1)
    h.insert(20,"c")
    
    assert h.findMax() == (20,"c")


## insert tests (using removeMin and removeMax):
    
# testing if the min-max heap actually inserts the keys (removeMin):
def test_sameKeysRemoveMin():
    size = 10
    h = minMaxHeap(size)
    found = True
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:    
    for i in range(size):  
        key = random.randint(0,100)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data) 
        test.append((key,data))       
    
    # make the list be in ascending order (min is at position 0):
    test.sort()
    
    # check if the keys inserted actually went into the heap by 
    # removing the min of the heap and comparing it to the min
    # of the list with the heap values: 
    for i in range(size):
        temp = h.removeMin()
        if temp[0] != test[i][0]:
            found = False
        
    assert found    

# testing if the min-max heap actually inserts the keys (removeMax):
def test_sameKeysRemoveMax():
    size = 10
    h = minMaxHeap(size)
    found = True
    
    test = []
    
    # insert the same key/data pair into the heap and the test list:    
    for i in range(size):  
        key = random.randint(0,100)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data) 
        test.append((key,data))       
    
    # make the list be in descending order (max is at position 0):
    test.sort()
    test.reverse()
    
    # check if the keys inserted actually went into the heap by 
    # removing the max of the heap and comparing it to the max
    # of the list with the heap values: 
    for i in range(size):        
        temp = h.removeMax()
        if temp[0] != test[i][0]:
            found = False
        
    assert found    

##remove tests:

# testing if removeMin actually removes the nodes by successively 
# calling it until the heap should be empty:
def test_removeMinEmptiesHeap():
    size = 1000
    h = minMaxHeap(size)
    
    for i in range(size):  
        key = random.randint(0,100)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data) 
        
    for i in range(size):
        h.removeMin()
    
    # assert that the heap is empty:
    assert len(h) == 0

# testing if removeMax actually removes the nodes by successively 
# calling it until the heap should be empty:
def test_RemoveMaxEmptiesHeap():
    size = 1000
    h = minMaxHeap(size)
    
    for i in range(size):  
        key = random.randint(0,100)
        data = chr(ord('A') + 1 + i)
        h.insert(key,data) 
        
    for i in range(size):
        h.removeMax()
    
    # assert that the heap is empty:
    assert len(h) == 0

pytest.main(["-v", "-s", "minMaxHeap.py"])       
