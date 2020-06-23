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

    def preference(self, i, j):
        key = (i, j)
        if key not in self._prefs:
            measure = self._measure(self.men[i], self.women[j])
            self._prefs[key] = measure
        else:
            measure = self._prefs[key]

        return measure

    def no_crush_or_prefer(self, crush_score, i, j):
        return crush_score is None or self.preference(i, j) > crush_score

    @property
    def unmarried_men(self):
        for man in self.men:
            if man.unmarried:
                yield man

    @property
    def enum_unmarried_men(self):
        for index, man in enumerate(self.men):
            if man.unmarried:
                yield index, man

    def __propose(self):
        for i, man in self.enum_unmarried_men:
            crush = None
            crush_score = None
            for j, woman in enumerate(self.women):
                if woman in man.exes:
                    continue
                if self.no_crush_or_prefer(crush_score, i, j):
                    crush_score = self.preference(i, j)
                    crush = j
            man.proposed_to = crush

    def __select(self):
        refusation_count = sum([
            1 for man in self.unmarried_men
        ])
        for j, woman in enumerate(self.women):
            crush = None
            crush_score = None
            for i, man in enumerate(self.men):
                if man.proposed_to != j:
                    continue
                if self.no_crush_or_prefer(crush_score, i, j):
                    if crush is not None:
                        self.men[crush].proposed_to = None
                        self.men[crush].exes.add(woman)
                        refusation_count += 1
                    crush_score = self.preference(i, j)
                    crush = i
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

        def _solution_tuple(i, man):
            name = man.name
            proposed_to = man.proposed_to
            bride = self.women[proposed_to].name
            preference = self.preference(i, proposed_to)

            return (name, bride, preference)

        return [_solution_tuple(index, man) for index, man in enumerate(self.men)]
