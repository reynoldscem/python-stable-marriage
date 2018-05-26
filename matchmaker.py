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
                prefs[i,j] = prefs.get((i, j), measure(i, j))
                if prefs[i,j] > crush_score:
                    crush_score = prefs[i,j]
                    crush = j
            man['proposed_to'] = crush
            
    def __select(self, men, women, measure, prefs):
        refusation_count = 0
        for j, woman in enumerate(women):
            crush = None
            crush_score = None
            for i, man in enumerate(men):
                
                if man['proposed_to'] != j:
                    continue
                
                prefs[i,j] = prefs.get((i, j), measure(i, j))
                if prefs[i,j] > crush_score:
                    if crush is not None:
                        men[crush]['proposed_to'] = None
                        men[crush]['exes'].append(j)
                    crush_score = prefs[i,j]
                    crush = i
                else:
                    man['proposed_to'] = None
                    man['exes'].append(j)
                    refusation_count += 1
        return refusation_count
    
    def marry(self, men, women, measure):
        '''
        Run Gale-Shapley algorithm on men and women lists
        
        men, women : list
        measure : f(man, woman) -> float
        
        Returns : list of tuples [(man, woman, couple_score), (...) ...]
        '''
        men = [{'soul': man,
                'proposed_to':None,
                'exes':[]} for man in men]
        self.prefs = {}
        
        def _measure(i, j):
            return measure(men[i]['soul'], women[j])
        
        while True:
            unmarried_men = [man for man in men
                             if man['proposed_to'] is None]
            if not unmarried_men:
                break
            self.__propose(men, women, _measure, self.prefs)
            refusation_count = self.__select(men, women, _measure, self.prefs)
            if not refusation_count:
                break
        return [(man['soul'],
                 women[man['proposed_to']],
                 self.prefs[i, man['proposed_to']])
                for i, man in enumerate(men)]