# TODO: from/to should follow inheritance even when defined outside of the class

from collections import defaultdict, deque
import inspect

_g_classmap = defaultdict(dict)

class CastError(Exception):
    def __str__(self):
        return self.args[0] % self.args[1:]


def _bfs(initial, expand):
    open_q = deque(list(initial))
    visited = set(open_q)
    while open_q:
        node = open_q.popleft()
        yield node
        for next_node in expand(node):
            if next_node not in visited:
                visited.add(next_node)
                open_q.append(next_node)



def _add_cast_function(from_type, to_type, f):
    if to_type in _g_classmap[from_type]:
        raise ValueError("Duplicate function", from_type, to_type)
    _g_classmap[from_type][to_type] = f


def _get_cast_elements(cls_module, cls, attr):
    direction, other_cls_name = attr.split('__', 1)
    assert direction in ('from', 'to')
    try:
        other_cls = getattr(cls_module, other_cls_name)
    except AttributeError:
        other_cls = __builtins__[other_cls_name]

    orig, target = (cls, other_cls) if direction == 'to' else (other_cls, cls)

    return orig, target, getattr(cls, attr)

def _find_cast_path(from_type, to_type):
    breadcrumbs = {}
    def expand(n):
        for k in _g_classmap[n]:
            if k not in breadcrumbs:
                breadcrumbs[k] = n
            yield k
    for x in _bfs([from_type], expand):
        if x == to_type:
            break
    else:
        raise CastError("Couldn't find a cast path between %s and %s", from_type, to_type)

    x = to_type
    path = []
    while x != from_type:
        path.append(x)
        x = breadcrumbs[x]
    path.reverse()
    return path

def _cast(instance, to_type):
    from_type = instance.__class__
    try:
        return _g_classmap[from_type][to_type](instance)
    except KeyError:
        path = _find_cast_path(from_type, to_type)

        prev = from_type
        inst = instance
        for n in path:
            inst = _g_classmap[prev][n](inst)
            prev = n
        return inst


def _match_annotations_decor(f):
    # TODO optimize (cast_args, cast_kwargs)
    names = list(f.__code__.co_varnames)
    annotations = f.__annotations__
    indices = [(names.index(n), a) for n,a in annotations.items()]
    def _inner(*args, **kwargs):
        args = list(args)
        for i, ann in indices:
            if i >= len(args):
                break
            args[i] = cast(args[i], ann)

        for name, val in kwargs.items():
            if name in annotations:
                kwargs[name] = cast(val, annotations[name])

        res = f(*args, **kwargs)
        if 'return' in annotations:
            res = cast(res, annotations['return'])
        return res

    return _inner

# ===========
#   API
# ===========
def autocast(f, lossy=False):
    return _match_annotations_decor(f)

def autoclass(cls):
    "Autocast class decorator to collect to__ and from__ methods."
    cls_module = inspect.getmodule(cls)
    for attr in dir(cls):
        if attr.startswith(('from__', 'to__')):
            orig, target, f = _get_cast_elements(cls_module, cls, attr)

            _add_cast_function(orig, target, f)
            # TODO remove original functions?

    return cls

def add_cast(from_type, to_type, f, is_lossy=False):
    """Add a cast function between two types

    The cast function should accept an instance of type 'from_type',
    and return an instance of type 'to_type'.
        1) instance of type 'from_type'
        2) type object of 'to_type'
    And return a new instance of type 'to_type'

    Example:
        >>>  add_cast(int, str, str)
        >>>  cast(5, str)
        "5"
    """
    assert not is_lossy, "TODO" # TODO
    assert from_type is not to_type
    return _add_cast_function(from_type, to_type, f)

def cast(inst, to):
    "Cast an instance to the target type"
    if isinstance(inst, to):
        return inst
    else:
        new_inst = _cast(inst, to)
        if not isinstance(new_inst, to):
            raise CastError("Returned instance is not of type %s (it's %s)", to, type(new_inst))
        return new_inst

# Basic casts
add_cast(str, int, int)
add_cast(bytes, int, int)
# add_cast(int, float, float, lossy=True)
add_cast(int, str, str)
add_cast(str, bytes, lambda s: s.encode('latin'))
add_cast(bytes, str, lambda b: b.decode('latin'))
add_cast(str, list, list)
add_cast(tuple, list, list)
add_cast(set, list, list)
add_cast(list, tuple, tuple)
add_cast(str, iter, iter)
add_cast(list, iter, iter)
add_cast(tuple, iter, iter)
add_cast(set, iter, iter)
add_cast(frozenset, iter, iter)
add_cast(frozenset, set, set)
add_cast(set, frozenset, frozenset)

add_cast(dict, list, lambda d: list(d.items()))
add_cast(dict, iter, lambda d: d.iteritems())

# Extra basic types
@autoclass
class Hex:
    @autocast
    def __init__(self, hexstr: str):
        assert hexstr.isalnum()
        self.hexstr = hexstr

    def to__bytes(self):
        return bytes.fromhex(self.hexstr)
    def from__bytes(b):
        return Hex(b.hex())

    def __len__(self):
        return len(self.hexstr) / 2


