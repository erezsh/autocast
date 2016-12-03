import collections
import functools

# Mixins
class IdentMixin(object):
    '''Provide basic class functionality based on the 'ident'
    attribute of a class

    >>> class Person(IdentMixin):
    ...     def __init__(self, name, surname):
    ...         self.name = name
    ...         self.surname = surname
    ...         self.ident = name, surname

    >>> Person('eric', 'blair')
    Person(('eric', 'blair'))

    >>> Person('erez', 'shinan') == Person('erez', 'shinan')
    True

    >>> Person('erez', 'shinan') == Person('erez', 'lalala')
    False

    >>> d = {Person('erez', 'sh'): 4}
    >>> d[Person('erez', 'sh')]
    4

    '''
    def __hash__(self):
        return hash(self.ident)
    def __eq__(self, other):
        try:
            return self.ident == other.ident
        except AttributeError:
            return False
    def __ne__(self, other):
        return not self == other
    def __repr__(self):
        if isinstance(self.ident, tuple):
            return '%s%r' % (type(self).__name__, self.ident)
        else:
            return '%s(%r)' % (type(self).__name__, self.ident)


# Decorators
def memoize(obj):
    '''Remember the result of a function, per argument, to avoid repeated calculation

    >>> @memoize
    ... def long_computation():
    ...     print "Oh my this is so long"
    ...     return 42

    >>> long_computation()
    Oh my this is so long
    42

    >>> long_computation()
    42
    '''
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = args, frozenset(kwargs.items())
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]

def bfs(initial, expand):
    open_q = collections.deque(list(initial))
    visited = set(open_q)
    while open_q:
        node = open_q.popleft()
        yield node
        for next_node in expand(node):
            if next_node not in visited:
                visited.add(next_node)
                open_q.append(next_node)


def dfs(initial, expand):
    queue = list(initial)
    visited = set(queue)
    while queue:
        node = queue.pop()
        yield node
        for next_node in expand(node):
            if next_node not in visited:
                visited.add(next_node)
                queue.append(next_node)

def classify_bool(seq, pred):
    true_elems = []
    false_elems = []

    for elem in seq:
        if pred(elem):
            true_elems.append(elem)
        else:
            false_elems.append(elem)

    return true_elems, false_elems

def classify(seq, key=None):
    d = {}
    for item in seq:
        k = key(item) if (key is not None) else item
        if k in d:
            d[k].append(item)
        else:
            d[k] = [item]
    return d

try:
    from contextlib import suppress     # New in Python 3.4
except ImportError:
    from contextlib import contextmanager
    @contextmanager
    def suppress(exc, else_call=None):
        '''Catch and dismiss the provided exception

        >>> x = 'hello'
        >>> with suppress(IndexError):
        ...     x = x[10]
        >>> x
        'hello'
        '''
        try:
            yield
        except exc:
            pass
        else:
            if else_call:
                else_call()

