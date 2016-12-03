from ..utils import bfs
from ..typecast import typecast_decor, CastError, Typecast

class Tree:
    __metaclass__ = Typecast

    def __init__(self, data, children=()):
        self.data = data
        self.children = children


class SExpression:
    __metaclass__ = Typecast

    def __init__(self, sexp):
        self.sexp = sexp



    def from__Tree(cls, tree):
        def _from_tree(t):
            return [t.data] + map(_from_tree, t.children)

        return cls(_from_tree(tree))

    def to__Tree(self, cls):
        def _to_tree(s):
            return cls(s[0], map(_to_tree, s[1:]))
        return _to_tree(self.sexp)


class BinTree:
    __metaclass__ = Typecast

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def to__Tree(self, cls):
        if self.right:
            return cls(self.data, [self.left >> cls, self.right >> cls])
        elif self.left:
            return cls(self.data, [self.left >> cls])
        else:
            return cls(self.data)

    def from__Tree(cls, tree):
        return cls(tree.data, *[c>>cls for c in tree.children])

