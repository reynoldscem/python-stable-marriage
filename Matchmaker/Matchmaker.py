class Man:
    def __init__(self, name):
        self.name = name
        self.proposed_to = None
        self.exes = set()

    @property
    def unmarried(self):
        return self.proposed_to is None


class Woman:
    def __init__(self, name):
        self.name = name


class Matchmaker:
    def __init__(self, men, women, measure):
        self.men = [Man(name) for name in men]
        self.women = [Woman(name) for name in women]
        self.measure = measure
        self._prefs = {}

        assert len(women) >= len(men), (
            "Must have more (or the same) women than men."
        )

    def preference(self, man, woman):
        key = (hash(man), hash(woman))
        if key not in self._prefs:
            measure = self._measure(man, woman)
            self._prefs[key] = measure
        else:
            measure = self._prefs[key]

        return measure

    def no_crush_or_prefer(self, crush_score, man, woman):
        return crush_score is None or self.preference(man, woman) > crush_score

    @property
    def unmarried_men(self):
        for man in self.men:
            if man.unmarried:
                yield man

    def __propose(self):
        for man in self.unmarried_men:
            crush = None
            crush_score = None
            for woman in self.women:
                if woman in man.exes:
                    continue
                if self.no_crush_or_prefer(crush_score, man, woman):
                    crush_score = self.preference(man, woman)
                    crush = woman
            man.proposed_to = crush

    def __select(self):
        refusation_count = sum([
            1 for man in self.unmarried_men
        ])
        for woman in self.women:
            crush = None
            crush_score = None
            for man in self.men:
                if man.proposed_to != woman:
                    continue
                if self.no_crush_or_prefer(crush_score, man, woman):
                    if crush is not None:
                        crush.proposed_to = None
                        crush.exes.add(woman)
                        refusation_count += 1
                    crush_score = self.preference(man, woman)
                    crush = man
                else:
                    man.proposed_to = None
                    man.exes.add(woman)
                    refusation_count += 1
        return refusation_count

    def _measure(self, man, woman):
        return self.measure(man.name, woman.name)

    def marry(self):
        '''
        Run Gale-Shapley algorithm on men and women lists

        men, women : list
        measure : f(man, woman) -> float

        Returns : list of tuples [(man, woman, couple_score), (...) ...]
        '''
        while True:
            if not list(self.unmarried_men):
                break
            self.__propose()
            refusation_count = self.__select()
            if not refusation_count:
                break

        def _solution_tuple(man):
            bride = man.proposed_to
            preference = self.preference(man, bride)

            return (man.name, bride.name, preference)

        return [_solution_tuple(man) for man in self.men]
