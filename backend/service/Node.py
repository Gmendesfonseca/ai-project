class Node(object):
    def __init__(self, parent=None, state=None, depth=None,
                 previous=None,  next=None):
        self.parent    = parent
        self.state     = state
        self.depth     = depth  
        self.previous  = previous
        self.next      = next

