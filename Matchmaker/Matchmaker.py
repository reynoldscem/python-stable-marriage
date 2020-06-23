class Person:
    def __init__(self, name):
        self.name = name

        self.crush = None
        self.crush_score = None

    def update_crush(self, new_score, person):
        raise NotImplementedError()


class Man(Person):
    def __init__(self, name):
        super().__init__(name)
        self.proposed_to = None
        self.exes = set()

    @property
    def unmarried(self):
        return self.proposed_to is None

    def update_crush(self, new_score, person):
        if self.crush_score is None or new_score > self.crush_score:
            self.crush_score = new_score
            self.crush = person


class Woman(Person):
    def update_crush(self, new_score, person):
        if self.crush_score is None or new_score > self.crush_score:
            if self.crush is not None:
                self.crush.proposed_to = None
                self.crush.exes.add(self)
            self.crush_score = new_score
            self.crush = person
        else:
            person.proposed_to = None
            person.exes.add(self)


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
            for woman in self.women:
                if woman in man.exes:
                    continue
                man.update_crush(self.preference(man, woman), woman)
            man.proposed_to = man.crush
            man.crush_score = None
            man.crush = None

    def __select(self):
        for woman in self.women:
            for man in self.men:
                if man.proposed_to != woman:
                    continue
                woman.update_crush(self.preference(man, woman), man)

            woman.crush_score = None
            woman.crush = None

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
            if list(self.unmarried_men):
                self.__propose()
                self.__select()
                continue
            break

        def _solution_tuple(man):
            bride = man.proposed_to
            preference = self.preference(man, bride)

            return (man.name, bride.name, preference)

        return [_solution_tuple(man) for man in self.men]
