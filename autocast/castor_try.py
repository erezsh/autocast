# TODO
# * Degrees / Radians
# * Vector / list / Point
# * Rect / Line / (Point, Point)
# * PNG / BMP
# * JSON / dict / bson / ...

# Module oriented design?
# Casting colors is a good demo for the tutorial
# Show type-safety using HTML (bold("a < b"))

# Example 1: API flexibility & Time
# Example 2: Type-safety & HTML

from .autocast import CastError, autocast, autoclass, cast
from .lib import time
from .lib.time import Seconds, Minutes, Hours, Days, Weeks
from .lib.web import HTML, JSON, RGB

class UFO:
    pass
    


@autoclass
class Fortnights:

    def __init__(self, fortnights):
        self.fortnights = fortnights

    def to__Weeks(self):
        return Weeks(self.fortnights * 2)


def test():
    print( cast( Minutes(60), Seconds ))
    print( cast(Seconds(90), Minutes) )
    print( cast(Days(2), Hours) )
    print( Minutes(30) - Minutes(5) * 2 )
    print( Minutes(30) > Hours(1), Minutes(30) <= Hours(1), Minutes(60) in {Hours(1)} )

    print( cast(Fortnights(2), Days), Fortnights(2) > Hours(200) )

    try:
        cast(Hours(2), UFO)
        assert False
    except CastError:
        pass

    print( cast("small < big", HTML) )
    print( cast({'a': 'haha', 'c': '<hello>'}, HTML ))
    print( cast(JSON('{"a":2}'), dict ) )

    try:
        cast( JSON('[2]'), dict )
        assert False
    except CastError:
        pass
    

    print( cast(RGB(10, 20, 30), HTML ) )


def sleep(time):
    time = time << Seconds
    pass


# sleep(Minutes(1))

# @hack
# class A:
#     pass

@autoclass
class Dog:

    def to__str(self):
        return "dog"

class Pug(Dog):
    def to__str(self):
        return "pug"

class GoodDog(Dog):
    pass

@autoclass
class MechDog:
    def from__Dog(dog):
        assert isinstance(dog, Dog)
        return Dog()

def test_inherit():
    assert cast(GoodDog(), str) == "dog"
    assert cast(Pug(), str) == "pug"
    try:
        print(cast(Pug(), MechDog) )
    except CastError:
        pass    # TODO!

@autocast
def test_autocast(a: int, b: Minutes):
    print(b)

@autocast
def print_html(html : HTML):
    print(html)

if __name__ == '__main__':
    # test_inherit()    # TODO
    test()
    test_autocast(4, Hours(2))

