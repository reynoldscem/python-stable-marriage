class Person:
    def __init__(self, name):
        self.name = name

        self.crush = None
        self.crush_score = None

    def update_crush(self, new_score, person):
        if not self.has_crush or new_score > self.crush_score:

            if self.has_crush:
                self.jilt(self.crush)

            self.crush_score = new_score
            self.crush = person
        else:
            self.jilt(person)

    @property
    def has_crush(self):
        return self.crush is not None

    def jilt(self, other):
        raise NotImplementedError()

    def break_up(self, other):
        raise NotImplementedError()

    def resolve_crush(self):
        self.crush_score = None
        self.crush = None


class Man(Person):
    def __init__(self, name):
        super().__init__(name)
        self.proposed_to = None
        self.exes = set()

    @property
    def unmarried(self):
        return self.proposed_to is None

    def update_crush(self, new_score, person):
        if not self.has_crush or new_score > self.crush_score:
            self.crush_score = new_score
            self.crush = person

    def break_up(self, person):
        self.proposed_to = None
        self.exes.add(person)

    def suitable(self, person):
        return person not in self.exes

    def resolve_crush(self):
            self.proposed_to = self.crush
            self.crush_score = None
            self.crush = None


class Woman(Person):
    def jilt(self, man):
        man.break_up(self)

    def suitable(self, man):
        return man.proposed_to == self


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

    @property
    def unmarried_men(self):
        for man in self.men:
            if man.unmarried:
                yield man

    def __stage(self, first_people, second_people):
        for first_person in first_people:
            for second_person in second_people:
                if first_person.suitable(second_person):
                    preference = self.preference(first_person, second_person)
                    first_person.update_crush(preference, second_person)
            first_person.resolve_crush()

    def __propose(self):
        self.__stage(self.unmarried_men, self.women)

    def __select(self):
        self.__stage(self.women, self.men)

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
