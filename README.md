# python-stable-marriage
Simple python implementation of Gale-Shapley algorithm.

https://en.wikipedia.org/wiki/Stable_marriage_problem

```python
from matchmaker import Matchmaker

# pip install python-levenshtein
from Levenshtein import ratio

# pip install stringdist - works on pypy
from stringdist import levenshtein_norm
def levenshtein_distance(first, second):
    return 1 - levenshtein_norm(first, second)

matchmaker = Matchmaker()
# matchmaker.marry(men, women, measure)
matched = matchmaker.marry(['book', 'mountain lion', 'cobra', 'jinja', 'dish'],
                           ['jeans', 'fish', 'seamounts', 'kobler', 'nook'],
                           ratio)

print(matched)
[('book', 'nook', 0.75),
 ('mountain lion', 'seamounts', 0.45454545454545453),
 ('cobra', 'kobler', 0.5454545454545454),
 ('jinja', 'jeans', 0.4),
 ('dish', 'fish', 0.75)]
```

Warnings:
* `len(women) >= len(men)`. Otherwise you'll get an `AssertinError`.
* if `len(women) > len(men)` there will be unmarried women left, you check for these afterwards.
* `measure` function should be commutative. I.e. `measure(a, b) == measure(b, a)`
* Because a lot of time is spent in a tight loop it runs *much* faster with
    `pypy`.
