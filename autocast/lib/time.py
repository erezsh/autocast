from __future__ import absolute_import
import time

from ..autocast import CastError, autoclass, autocast, cast

class Unit:

    def __init__(self, value):
        setattr(self, self._attr, value)

    def __repr__(self):
        return "%s(%g)" % (self.__class__.__name__, getattr(self, self._attr))

    def __mul__(self, scalar):
        assert isinstance(scalar, (int, float))
        return type(self)(getattr(self, self._attr) * scalar)

    def __div__(self, scalar):
        assert isinstance(scalar, (int, float))
        return type(self)(getattr(self, self._attr) / scalar)

    def __add__(self, other):
        other = cast(other, type(self))
        return type(self)(getattr(self, self._attr) + getattr(other, self._attr))

    def __sub__(self, other):
        other = cast(other, type(self))
        return type(self)(getattr(self, self._attr) - getattr(other, self._attr))

    def __eq__(self, other):
        other = cast(other, type(self))
        return getattr(self, self._attr) == getattr(other, self._attr)

    def __lt__(self, other):
        other = cast(other, type(self))
        return getattr(self, self._attr) < getattr(other, self._attr)

    def __ne__(self, other):
        return not (self == other)
    def __gt__(self, other):
        return other < self
    def __ge__(self, other):
        return not (self < other)
    def __le__(self, other):
        return not (other < self)

class TimeUnit(Unit):
    def __hash__(self):
        return hash(cast(self, Seconds).seconds)


@autoclass
class Seconds(TimeUnit):
    _attr = 'seconds'


@autoclass
class Millisecs(TimeUnit):
    _attr = 'millisecs'

    def to__Seconds(self):
        return Seconds(self.millisecs / 1000.0)

    def from__Seconds(seconds):
        return Millisecs(seconds.seconds * 1000.0)


@autoclass
class Minutes(TimeUnit):
    _attr = 'minutes'

    def to__Seconds(self):
        return Seconds(self.minutes * 60.0)

    def from__Seconds(seconds):
        return Minutes(seconds.seconds / 60.0)

@autoclass
class Hours(TimeUnit):
    _attr = 'hours'

    def to__Seconds(self):
        return Seconds(self.hours * (60.0 * 60.0))

    def from__Seconds(seconds):
        return Hours(seconds.seconds / (60.0 * 60.0))

@autoclass
class Days(TimeUnit):
    _attr = 'days'

    def to__Seconds(self):
        return Seconds(self.days * (60.0 * 24.0 * 60.0))

    def from__Seconds(seconds):
        return Days(seconds.seconds / (24.0 * 60.0 * 60.0))


@autoclass
class Weeks(TimeUnit):
    _attr = 'weeks'

    def to__Days(self):
        return Days(self.weeks * 7)

    def from__Days(days):
        return Weeks(days.days / 7.0)


@autocast
def sleep(secs: Seconds):
    time.sleep(secs.seconds)

