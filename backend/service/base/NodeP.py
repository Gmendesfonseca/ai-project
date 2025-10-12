from .Node import Node


class NodeP(Node):
    def __init__(self, parent=None, state=None, v1=None,
                 previous=None, next_node=None, v2=None):
        super().__init__(parent, state, v1, previous, next_node)
        self.v2 = v2
