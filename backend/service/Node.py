class Node(object):
    def __init__(self, father=None, state=None, v1=None,
                 previous=None,  next=None):
        self.father    = father
        self.state     = state
        self.v1        = v1
        self.previous  = previous
        self.next      = next

