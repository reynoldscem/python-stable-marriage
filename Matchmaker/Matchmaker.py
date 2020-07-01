from collections import defaultdict


class Person:
    def __init__(self, obj, higher_is_better=False):
        self.name = repr(obj)
        self.data = obj

        self.higher_is_better = higher_is_better

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

    def crush_improvement(self, new_score):
        if not self.has_crush:
            return True

        if self.higher_is_better:
            return new_score > self.crush_score
        else:
            return new_score < self.crush_score

    def update_crush(self, new_score, person):
        if self.crush_improvement(new_score):
            self.jilt(self.crush)

            self.crush_score = new_score
            self.crush = person
        else:
            self.jilt(person)


class Man(Person):
    def __init__(self, obj):
        super().__init__(obj)
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
        if man:
            man.jilted_by(self)

    def suitable(self, man):
        return man.proposed_to == self


class FunctionDefaultDict(defaultdict):
    def __missing__(self, key):
        return_ = self[key[::-1]] = self[key] = self.default_factory(key)
        return return_


class Matchmaker:
    def __init__(
            self,
            men, women,
            measure, measure_attribute=None,
            person_kwargs={}):

        self.men = self.make_people_from_objects(Man, men, person_kwargs)
        self.women = self.make_people_from_objects(Woman, women, person_kwargs)

        self.measure = measure
        self.measure_attribute = measure_attribute

        self.preference = FunctionDefaultDict(self._measure)

        self.ensure_more_women()

    @staticmethod
    def make_people_from_objects(cls, objects, person_kwargs):
        return [cls(obj, **person_kwargs) for obj in objects]

    def ensure_more_women(self):
        message = "Must have more (or the same) women than men."
        if len(self.women) < len(self.men):
            raise ValueError(message)

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
        if self.measure_attribute:
            return self.measure(
                getattr(man.data, self.measure_attribute),
                getattr(woman.data, self.measure_attribute)
            )
        else:
            return self.measure(man.data, woman.data)

    def solution(self, man):
        bride = man.proposed_to
        preference = self.preference[man, bride]

        return (man.data, bride.data, preference)

    def marry(self):
        while self.some_men_unmarried:
            self.propose()
            self.select()

        return [self.solution(man) for man in self.men]
