Build a min-max heap from scratch (https://en.wikipedia.org/wiki/Min-max_heap#Operations).
A min-max heap is a data structure that combines the utilities of both a min heap and a max heap. 
The property that defines a min-max heap is that: each node at an even level in the tree is less than all of its descendants, while each node at an odd level in the tree is greater than all of its descendants. 
I incorporated the following methods within the minMaxHeap class:
removeMin, removeMax, insert, trickleDown (both max and min), trickle up (both max and min), findMin, findMax, and isMinMaxHeap. 
Additionally, there are very extensive PyTests included at the end. 
