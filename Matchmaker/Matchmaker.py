class Matchmaker:
    def __propose(self, men, women, measure, prefs):
        for i, man in enumerate(men):
            if man['proposed_to']:
                continue
            crush = None
            crush_score = None
            for j, woman in enumerate(women):
                if j in man['exes']:
                    continue
                prefs[i, j] = prefs.get((i, j), measure(i, j))
                if crush_score is None or prefs[i, j] > crush_score:
                    crush_score = prefs[i, j]
                    crush = j
            man['proposed_to'] = crush

    def __select(self, men, women, measure, prefs):
        refusation_count = sum([
            1 for man in men if man['proposed_to'] is None
        ])
        for j, woman in enumerate(women):
            crush = None
            crush_score = None
            for i, man in enumerate(men):
                if man['proposed_to'] != j:
                    continue
                prefs[i, j] = prefs.get((i, j), measure(i, j))
                if crush_score is None or prefs[i, j] > crush_score:
                    if crush is not None:
                        men[crush]['proposed_to'] = None
                        men[crush]['exes'].append(j)
                        refusation_count += 1
                    crush_score = prefs[i, j]
                    crush = i
                else:
                    man['proposed_to'] = None
                    man['exes'].append(j)
                    refusation_count += 1
        return refusation_count

    @staticmethod
    def make_man_container(man):
        return {
            'soul': man,
            'proposed_to': None,
            'exes': []
        }

    def marry(self, men, women, measure):
        '''
        Run Gale-Shapley algorithm on men and women lists

        men, women : list
        measure : f(man, woman) -> float

        Returns : list of tuples [(man, woman, couple_score), (...) ...]
        '''
        men = [self.make_man_container(man) for man in men]
        self.prefs = {}

        def _measure(i, j):
            return measure(men[i]['soul'], women[j])

        while True:
            unmarried_men = [
                man for man in men
                if man['proposed_to'] is None
            ]
            if not unmarried_men:
                break
            self.__propose(men, women, _measure, self.prefs)
            refusation_count = self.__select(men, women, _measure, self.prefs)
            if not refusation_count:
                break

        def _solution_tuple(i, man):
            name = man['soul']
            proposed_to = man['proposed_to']
            bride = women[proposed_to]
            preference = self.prefs[i, proposed_to]

            return (name, bride, preference)

        return [_solution_tuple(index, man) for index, man in enumerate(men)]
