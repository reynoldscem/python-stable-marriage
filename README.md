# python-stable-marriage
Simple python implementation of Gale-Shapley algorithm.

https://en.wikipedia.org/wiki/Stable_marriage_problem

```python
from Matchmaker import Matchmaker

# pip install stringdist - works on pypy
from stringdist import levenshtein_norm

# Matchmaker(men, women, measure)
# Works like you'd expect on strings.
matched = Matchmaker(
    ['book', 'mountain lion', 'cobra', 'jinja', 'dish'],
    ['jeans', 'fish', 'seamounts', 'kobler', 'nook'],
    levenshtein_norm
).marry()

print(matched)
[('book', 'nook', 0.25),
('mountain lion', 'seamounts', 0.8461538461538461),
('cobra', 'kobler', 0.6666666666666666),
('jinja', 'jeans', 0.8),
('dish', 'fish', 0.25)]

# Matchmaker(men, women, measure)
# Works with other types.
matched = Matchmaker(
    [1, 2, 3],
    [-1, 2, -3],
    lambda x, y: abs(abs(x) - abs(y))
).marry()

print(matched)
[(1, -1, 0), (2, 2, 0), (3, -3, 0)]

# Matchmaker(men, women, measure, measure_attribute)
# Works with objects, and can unpack attibutes of those objects.
# Useful for e.g. using a metric from a library on your own object.
from collections import namedtuple
Person = namedtuple('Person', ['name', 'age'])
Matchmaker(
    [Person('Bob', 32), Person('Dave', 61)],
    [Person('Alice', 37), Person('Dot', 70)],
    lambda x, y: abs(abs(x) - abs(y)),
    measure_attribute='age'
).marry()

print(matched)
[(Person(name='Bob', age=32), Person(name='Alice', age=37), 5),
 (Person(name='Dave', age=61), Person(name='Dot', age=70), 9)]

# Matchmaker(men, women, measure, measure_attribute, person_kwargs)
# person_kwargs refers to Matchmaker.Person, not this namedtuple Person.
# Currently higher_is_better is the only option, but more may be supported in
# future to configure the behaviour of the people being married.
Matchmaker(
    [Person('Bob', 32), Person('Dave', 61)],
    [Person('Alice', 37), Person('Dot', 70)],
    lambda x, y: abs(x - y),
    measure_attribute='age',
    person_kwargs={'higher_is_better'=True}
).marry()

print(matched)
[(Person(name='Bob', age=32), Person(name='Dot', age=70), 38),
 (Person(name='Dave', age=61), Person(name='Alice', age=37), 24)]
```

Warnings:
* `len(women) >= len(men)`. Otherwise you'll get a `ValueError`.
* if `len(women) > len(men)` there will be unmarried women left, you check for these afterwards.
* `measure` function should be commutative. I.e. `measure(a, b) == measure(b, a)`
* Because a lot of time is spent in a tight loop it runs *much* faster with
    `pypy`.
