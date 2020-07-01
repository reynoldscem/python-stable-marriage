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
    # Men can proposition up to one woman at once, and suitable women are those
    # who have not yet rejected (here jilted) him.
    def __init__(self, obj, **kwargs):
        super().__init__(obj, **kwargs)
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
    # A suitable partner is one who has proposed to the woman, forward a
    # message to a man if he has been jilted.
    def jilt(self, man):
        if man:
            man.jilted_by(self)

    def suitable(self, man):
        return man.proposed_to == self


class FunctionDefaultDict(defaultdict):
    # This is for memoising the scores. We use self[key[::-1]] = self[key] in
    # order to memoise it in both directions, given scores should be reflexive.
    # The overridden __missing__ method is to compute the measure on the key
    # (which is a pair of people, and memoise it. Can give significant speedup
    # if measure is expensive.
    def __missing__(self, key):
        return_ = self[key[::-1]] = self[key] = self.default_factory(key)
        return return_


class Measure():
    def __init__(self, measure, measure_attribute=None):
        if isinstance(measure, type(self)):
            # If we're passed a measure just 'become' it.
            self.measure = measure.measure
            self.attribute = measure.attribute
            self.cache = measure.cache

            return

        self.measure = measure
        self.attribute = self.make_attribute_func(measure_attribute)
        self.cache = FunctionDefaultDict(self)

    @staticmethod
    def make_attribute_func(measure_attribute):
        if measure_attribute:
            def _measure_attribute(person):
                return getattr(person.data, measure_attribute)
        else:
            def _measure_attribute(person):
                return person.data

        return _measure_attribute

    def __call__(self, argument):
        man, woman = argument

        return self.measure(self.attribute(man), self.attribute(woman))


class Matchmaker:
    def __init__(
            self, men, women, measure,
            measure_attribute=None, person_kwargs={}):
        self.men = self.make_people_from_objects(Man, men, person_kwargs)
        self.women = self.make_people_from_objects(Woman, women, person_kwargs)

        # If `measure` is not a measure object, make one. Pass the measuring
        # function and an optional attribute to call on the objects before
        # measuring. E.g. if we have a function measuring strings and File
        # objects with a string `name` attribute then `attribute` could be
        # `name` and we would measure like `measure(man.name, woman.name)`.
        # Measure object has a cache for making memoised calls.
        #
        # Bit of a weird approach, but allows for choosing:
        #  - Simple interface where user just passes a function
        #  - Slight configuration where they also pass an attribute
        #  - Full dependency injection where they pass an arbitrary Measure
        if not isinstance(measure, Measure):
            measure = Measure(measure, measure_attribute)

        # Get memoised preference. Treat it like a function, but access with
        # self.prefence[man, woman] or self.preference[woman, man].
        self.preference = measure.cache

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
        # Both phases of the algorithm are structurally similar. One group goes
        # through its suitors and attempts to find a(n improved) potentiall
        # spouse. The exact mechanics of how they find and deal with suitors
        # depends on the type of Person object. Hopefully variants of the
        # stable marriage problem should be obtainable by sublcassing person
        # and calling stages with different groups of people / in different
        # orders.
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

    def solution(self, man):
        bride = man.proposed_to
        score = self.preference[man, bride]

        return (man.data, bride.data, score)

    def marry(self):
        while self.some_men_unmarried:
            self.propose()
            self.select()

        return [self.solution(man) for man in self.men]
