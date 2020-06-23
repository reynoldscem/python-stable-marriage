from collections import defaultdict


class Person:
    def __init__(self, name):
        self.name = name

        self.crush = None
        self.crush_score = None

    @property
    def has_crush(self):
        return self.crush is not None

    def jilt(self, other):
        pass

    def jilted_by(self, other):
        pass

    def resolve_crush(self):
        self.crush_score = None
        self.crush = None

    def update_crush(self, new_score, person):
        if not self.has_crush or new_score > self.crush_score:

            if self.has_crush:
                self.jilt(self.crush)

            self.crush_score = new_score
            self.crush = person
        else:
            self.jilt(person)


class Man(Person):
    def __init__(self, name):
        super().__init__(name)
        self.proposed_to = None
        self.exes = set()

    @property
    def unmarried(self):
        return self.proposed_to is None

    def jilted_by(self, person):
        self.proposed_to = None
        self.exes.add(person)

    def suitable(self, person):
        return person not in self.exes

    def resolve_crush(self):
        self.proposed_to = self.crush
        super().resolve_crush()


class Woman(Person):
    def jilt(self, man):
        man.jilted_by(self)

    def suitable(self, man):
        return man.proposed_to == self


class FunctionDefaultDict(defaultdict):
    def __missing__(self, key):
        return_ = self[key[::-1]] = self[key] = self.default_factory(key)
        return return_


class Matchmaker:
    def __init__(self, men, women, measure):
        self.men = [Man(name) for name in men]
        self.women = [Woman(name) for name in women]
        self.measure = measure
        self.preference = FunctionDefaultDict(self._measure)

        self.assert_more_women()

    def assert_more_women(self):
        message = "Must have more (or the same) women than men."
        assert len(self.women) >= len(self.men), message

    @property
    def unmarried_men(self):
        for man in self.men:
            if man.unmarried:
                yield man

    @property
    def some_men_unmarried(self):
        return any(man.unmarried for man in self.men)

    def stage(self, first_people, second_people):
        for first_person in first_people:
            for second_person in second_people:
                if first_person.suitable(second_person):
                    preference = self.preference[first_person, second_person]
                    first_person.update_crush(preference, second_person)
            first_person.resolve_crush()

    def propose(self):
        self.stage(self.unmarried_men, self.women)

    def select(self):
        self.stage(self.women, self.men)

    def _measure(self, args):
        man, woman = args
        return self.measure(man.name, woman.name)

    def solution(self, man):
        bride = man.proposed_to
        preference = self.preference[man, bride]

        return (man.name, bride.name, preference)

    def marry(self):
        while self.some_men_unmarried:
            self.propose()
            self.select()

        return [self.solution(man) for man in self.men]
