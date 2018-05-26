# python-stable-marriage
Simple python implementation of Gale-Shapley algorithm.

https://en.wikipedia.org/wiki/Stable_marriage_problem

```python
from matchmaker import Matchmaker

# pip install python-levenshtein
from Levenshtein import ratio

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
* len(women) >= len(men) . Otherwise you'll get TypeError
* if len(women) > len(men) there will be unmarried women left
* _measure_ function should be commutative. _measure_(a, b) == _measure_(b, a)
