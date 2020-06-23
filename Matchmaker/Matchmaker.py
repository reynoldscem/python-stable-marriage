class Matchmaker:
    def __init__(self, men, women, measure):
        self.men = [self._make_man_container(man) for man in men]
        self.women = women
        self.measure = measure

        assert len(women) >= len(men), (
            "Must have more (or the same) women than men."
        )

    def __propose(self, prefs):
        for i, man in enumerate(self.men):
            if man['proposed_to']:
                continue
            crush = None
            crush_score = None
            for j, woman in enumerate(self.women):
                if j in man['exes']:
                    continue
                prefs[i, j] = prefs.get((i, j), self._measure(i, j))
                if crush_score is None or prefs[i, j] > crush_score:
                    crush_score = prefs[i, j]
                    crush = j
            man['proposed_to'] = crush

    def __select(self, prefs):
        refusation_count = sum([
            1 for man in self.men if man['proposed_to'] is None
        ])
        for j, woman in enumerate(self.women):
            crush = None
            crush_score = None
            for i, man in enumerate(self.men):
                if man['proposed_to'] != j:
                    continue
                prefs[i, j] = prefs.get((i, j), self._measure(i, j))
                if crush_score is None or prefs[i, j] > crush_score:
                    if crush is not None:
                        self.men[crush]['proposed_to'] = None
                        self.men[crush]['exes'].append(j)
                        refusation_count += 1
                    crush_score = prefs[i, j]
                    crush = i
                else:
                    man['proposed_to'] = None
                    man['exes'].append(j)
                    refusation_count += 1
        return refusation_count

    @staticmethod
    def _make_man_container(man):
        return {
            'soul': man,
            'proposed_to': None,
            'exes': []
        }

    def _measure(self, i, j):
        return self.measure(self.men[i]['soul'], self.women[j])

    def marry(self):
        '''
        Run Gale-Shapley algorithm on men and women lists

        men, women : list
        measure : f(man, woman) -> float

        Returns : list of tuples [(man, woman, couple_score), (...) ...]
        '''
        self.prefs = {}

        while True:
            unmarried_men = [
                man for man in self.men
                if man['proposed_to'] is None
            ]
            if not unmarried_men:
                break
            self.__propose(self.prefs)
            refusation_count = self.__select(self.prefs)
            if not refusation_count:
                break

        def _solution_tuple(i, man):
            name = man['soul']
            proposed_to = man['proposed_to']
            bride = self.women[proposed_to]
            preference = self.prefs[i, proposed_to]

            return (name, bride, preference)

        return [_solution_tuple(index, man) for index, man in enumerate(self.men)]
