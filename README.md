# Autocast: Cast-Oriented programming

Autocast is an experimental python library for defining casts (transformations) between different types.

A cast is a simply a function that converts between types. Autocast provides a convenient way to define casts, and to apply them in your code.

Features:

* Convenient declaration syntax using class decorators (with `@autoclass`)

* Autocasting arguments according to the function annotations (with `@autocast`)

* Cast chaining, chosen by the shortest-path

* Type-checking in run-time

## Install

```bash
    $ git clone https://github.com/erezsh/autocast
    $ cd autocast
    $ python3 setup.py install
```

## Case Study

As a case study, let's use Autocast on a toy JSON class:

```python
import json
from autocast import autoclass

@autoclass
class JSON:
    def __init__(self, json):
        self.json = json

    def from__str(s):
        return JSON(json.loads(s))

    def to__dict(self):
        return self.json

    # ... more casts, and other methods

```

The `@autoclass` decorator automatically finds the `to__*` and `from__*` methods, and adds them as casts.

Let's see how we can use it to cast between types:

```python
>>> from autocast import cast
>>> cast('{"a": [1,2  ]}', JSON, dict)  # Convert to dict via JSON
{'a': [1, 2]}
```

Because this is the best route between `str` and `dict`, we can just do:
```python
>>> cast('{"a": [1,2  ]}', dict)
{'a': [1, 2]}
```

Of course, Autocast protects you from making type errors:

```python
>>> cast('["a", "b"]', dict)
autocast.CastError: Returned instance is not of type <class 'dict'> (it's <class 'list'>)
```

But this is all a little boring. Let's demonstrate something useful, and define an itemgetter function:

```python
@autocast
def dict_getitem(d: dict, key: str):
    return d[key]
```

And this is how we use it:

```python
>>> json_getitem({"foo": "bar"}, 'foo')     # Works as normal
'bar'
>>> json_getitem('{"foo": "bar"}', 'foo')   # Magic!
'bar'
>>> json_getitem('{"foo": "bar"}', [1]) # [1] is not a valid key type
autocast.autocast.CastPathError: Couldn't find a cast path between <class 'list'> and <class 'str'>
```

Pretty cool, right?

## Caveats

The main caveats of this library is that:

1. It's young, which means it's still lacking a lot of features.

2. It's experimental, which means its concepts still need some work.

3. It's easy to abuse it and write bad code. Use it with caution!

## Support

Autocast works on all versions of Python 3. (autocast relies on annotations)

If there's enough demand, I will make it work for Python 2 too.

## Contribute

I'm open to any contribution.

The main thing you can do is use it and report about your experience with it!

