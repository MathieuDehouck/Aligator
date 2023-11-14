"""
..
  A simple implementation of a finite state transducer for Mx and Mx project
  starts from the right to the left
  Marine Delaborde, Mathieu Dehouck
  01/2023

Contains two classes for modeling French spelling rules as a backward transducer.
"""


cons = ['m', 'b', 'p', 'f', 'v', 'n', 'd', 't', 'z', 's', 'l', 'ɲ', 'ʒ', 'ʃ', 'ŋ', 'ɡ', 'k', 'ʁ', 'j']
vowels = ['i', 'y', 'u', 'e', 'œ', 'ø', 'o', 'ɔ', 'ɛ', 'ə', 'a', 'ɑ']
#'̃'

# s'occuper du t avant voyelle tion
# s'occuper du n avant p et b 

class StateMachine():
    """
    A state machine class with a few twists to handle default case.
    """

    def __init__(self):
        """
        :returns: a state machine representing a subset of French spelling backward.
        """
        
        self.last_state = State('last', self)
        self.states = {'last':self.last_state, 'I':State('I', self, accept=True), 'O':State('O', self, accept=True), 'E':State('E', self, accept=True), 'V':State('V', self, accept=True),'Vs':State('Vs', self), 'notI':State('notI', self),
                       'C':State('C', self, accept=True), 'CC':State('CC', self, accept=True), '2C':State('2C', self, accept=False), 'Cs':State('Cs', self, accept=True), 'N':State('N', self)}

        self.states['I'].default = self.states['V']
        self.states['O'].default = self.states['V']
        self.states['CC'].default = self.states['C']
        self.states['2C'].default = self.states['C']
        self.states['notI'].default = self.states['C']
        
        self.last_state.transitions = {'m':[('me', 'C'), ('mme', '2C')],
                                       'b':[('be', 'C'), ('bbe', '2C')],
                                       'p':[('pe', 'C'), ('ppe', '2C')],
                                       'f':[('fe', 'C'), ('ffe', '2C'), ('f', 'C'), ('phe', 'CC'), ('ph','CC')],
                                       'v':[('ve', 'C')],
                                       'n':[('ne', 'C'), ('nne', '2C')],
                                       'd':[('de', 'C'), ('dde', '2C')],
                                       't':[('te', 'C'), ('tte', '2C'), ('the', 'CC')],
                                       'z':[('ze', 'C'), ('se', 'Vs')], # VssV is fine here since we want to make sure we have a vowel
                                       's':[('se', 'Cs'), ('sse', 'Vs'), ('ce', 'C')],
                                       'l':[('le', 'C'), ('lle', 'notI'), ('l', 'C')],
                                       'ɲ':[('gne', 'CC')],
                                       'ʒ':[('ge', 'C')],
                                       'ʃ':[('che', 'CC'), ('sch', 'CC')],
                                       'ŋ':[('ng', 'CC')],
                                       'ɡ':[('gue', 'C')],
                                       'k':[('que', 'C'), ('c', 'C'), ('ck', 'CC'), ('k', 'C'), ('cque', 'CC'), ('q', 'C')],
                                       'ʁ':[('re', 'C'), ('rre', '2C'), ('rt', 'CC'), ('rd', 'CC'), ('rs', 'CC')],
                                       'i':[('i', 'I')], # front vowels, i, e, and y
                                       'y':[('u', 'O')],
                                       'u':[('ou', 'O')], # rounded vowels, o, a, u
                                       'e':[('é', 'E'), ('ez', 'E')],
                                       'œ':[('œux', 'O')],
                                       'ø':[('eux', 'E')],
                                       'o':[('eau', 'E'), ('ault', 'O'), ('aux', 'O'), ('ot', 'O')],
                                       'ɔ':[('o', 'O')],
                                       'ɛ':[('ai', 'O')],
                                       'ə':[('eu', 'E')],
                                       'a':[('a', 'O')],
                                       'ɑ':[('â', 'O')],
                                       '̃':[('n', 'N')],
                                       'j':[('ille', 'I'), ('ï', 'I')]}


        self.states['V'].transitions = {'m':[('m', 'C'), ('mm', '2C')],
                                        'b':[('b', 'C'), ('bb', '2C')],
                                        'p':[('p', 'C'), ('pp', '2C')],
                                        'f':[('f', 'C'), ('ff', '2C'), ('f', 'C'), ('ph', 'CC')],
                                        'v':[('v', 'C')],
                                        'n':[('n', 'C'), ('nn', '2C')],
                                        'd':[('d', 'C'), ('dd', '2C')],
                                        't':[('tt', '2C'), ('th', 'CC'), ('t', 'C')],
                                        'z':[('z', 'C'), ('s', 'Vs')],
                                        'l':[('l', 'C')],# ('ll', 'notPostI')],
                                        'ɲ':[('gn', 'CC')],
                                        #'ʒ':[('g', 'CC')],
                                        'ʃ':[('ch', 'CC')],# ('sch', 'CC')],
                                        #'ŋ':[('ng', 'CC'#)],
                                        #'ɡ':[('gu', 'CC')],
                                        #'k':[('qu', 'C')],
                                        'ʁ':[('r', 'C'), ('rr', '2C')],
                                        'i':[('i', 'I')],
                                        'y':[('u', 'O')],
                                        'u':[('ou', 'O')],
                                        'e':[('é', 'E')],
                                        'œ':[('œu', 'O')],
                                        'ø':[('eu', 'E')],
                                        'o':[('eau', 'E'), ('au', 'O')],
                                        'ɔ':[('o', 'O')],
                                        'ɛ':[('è', 'E'), ('ai', 'O')],
                                        'ə':[('eh', 'E')],
                                        'a':[('a', 'O')],
                                        'ɑ':[('â', 'O')],
                                        #'̃':[('n', 'N')],
                                        'j':[('y', 'I')],
                                        'w':[('w', 'C'), ('ou', 'O')],
                                        'ɥ':[('u', 'O')]}

        self.states['I'].transitions = {'t':[('tt', 'CC'), ('th', 'CC')],
                                        's':[('s', 'Cs'), ('ss', 'Vs'), ('c', 'C'), ('sc', 'CC')],
                                        #'l':[('l', 'C'), ('ll', 'notPostI'), ('l', 'C')],
                                        #'ɲ':[('gn', 'CC')],
                                        'ʒ':[('g', 'C'), ('j', 'C')],
                                        'ʃ':[('ch', 'CC')],# ('sch', 'CC')],
                                        #'ŋ':[('ng', 'CC'#)],
                                        'ɡ':[('gu', 'C')],
                                        'k':[('qu', 'C'), ('cqu', 'CC')],
                                        'j':[('y', 'I')],
                                        'ɛ':[('e', 'E')],
        }

        self.states['E'].default = self.states['V']
        self.states['E'].transitions = {'s':[('s', 'Cs'), ('ss', 'Vs'), ('c', 'C'), ('sc', 'CC')],
                                        #'l':[('l', 'C'), ('ll', 'notPostI'), ('l', 'C')],
                                        #'ɲ':[('gn', 'CC')],
                                        'ʒ':[('g', 'C'), ('j', 'C')],
                                        'ʃ':[('ch', 'CC')],# ('sch', 'CC')],
                                        #'ŋ':[('ng', 'CC'#)],
                                        'ɡ':[('gu', 'C')],
                                        'k':[('qu', 'C'), ('cqu', 'CC')],
                                        'j':[('y', 'I')] }

        self.states['O'].transitions = {#'t':[('t', 'C'), ('tt', 'CC'), ('th', 'CC')],
            's':[('s', 'Cs'), ('ss', 'Vs'), ('ç', 'C')],
            'ʒ':[('ge', 'C'), ('j', 'C')],
            'ɡ':[('g', 'C')],
            'k':[('c', 'C')],
            'j':[('y', 'I')]
        }

        self.states['C'].transitions = {'̃':[('n', 'N')],
                                        'm':[('m', 'CC')],
                                        'b':[('b', 'CC')],
                                        'p':[('p', 'CC')],
                                        'f':[('f', 'CC'), ('ph', 'CC')],
                                        'v':[('v', 'CC')],
                                        'n':[('n', 'C'), ('nn', '2C')],
                                        'd':[('d', 'CC')],
                                        't':[('t', 'CC'), ('tt', '2C'), ('th', 'CC')],
                                        'z':[('z', 'CC')],
                                        's':[('s', 'CC')],
                                        'l':[('l', 'CC'), ('ll', 'notI')],
                                        #'ɲ':[('gn', 'CC')],
                                        'ʒ':[('j', 'CC'), ('ge', 'C')],
                                        'ʃ':[('ch', 'CC'), ('sch', 'CC')],
                                        'ŋ':[('ng', 'CC')],
                                        'ɡ':[('g', 'CC')],
                                        'k':[('c', 'CC')],
                                        'ʁ':[('r', 'CC'), ('rr', '2C')],
                                        'i':[('i', 'I')],
                                        'y':[('u', 'O')],
                                        'u':[('ou', 'O')],
                                        'e':[('é', 'E')],
                                        'œ':[('œu', 'O')],
                                        'ø':[('eu', 'E')],
                                        'o':[('au', 'O')],
                                        'ɔ':[('o', 'O')],
                                        'ɛ':[('è', 'E'), ('ai', 'O')],
                                        'ə':[('e', 'E')],
                                        'a':[('a', 'O')],
                                        'ɑ':[('â', 'O')],
                                        'w':[('w', 'C'), ('ou', 'O')],
                                        'j':[('ye?', 'I')]
        }

        self.states['CC'].transitions = {'ɛ':[('e', 'E'), ('ei', 'E'), ('ai', 'O')], 'ə':[('eu', 'E')],
                                         'ʁ':[('r', 'CC')]}
                                         
        self.states['2C'].transitions = {'ɛ':[('e', 'E'), ('ei', 'E'), ('ai', 'O')], 'ə':[('', 'catch_all')]}
        self.states['2C'].transitions.update({c:[('', 'catch_all')] for c in cons})

        self.states['notI'].transitions = {}

        self.states['Cs'].default = self.states['C']
        self.states['Cs'].transitions = {v:[('', 'catch_all')] for v in vowels}

        self.states['Vs'].default = self.states['C']
        self.states['Vs'].transitions = {c:[('', 'catch_all')] for c in cons}
        self.states['Vs'].transitions.update({'̃':[('n', 'N')],
                                              'ɛ':[('è', 'E'), ('ai', 'O')],
                                              'ə':[('eu', 'E')],
                                              'a':[('a', 'O')]})

        self.states['N'].transitions = {'ɑ':[('a', 'O')],
                                        'ɔ':[('o', 'O')],
                                        'ɛ':[('i', 'E'), ('ai', 'O')],
                                        'œ':[('u', 'O')]}
        

    def transduce(self, ipa):
        """
        turns a sequence of IPA characters into a sequence of latin alphabet characters

        :param ipa: The IPA string to turn into a French-like family name.

        :returns: ``[forms]``:
        
        * **[forms]** is the list of orthographical forms corresponding to the ipa form.
        """
        print(ipa)

        forms = self.last_state.extend(ipa[::-1][1:])
        return forms




class State():
    """
    the basic state class
    """

    def __init__(self, name, machine, default=None, accept=False):
        """
        :param name: an indentifier for this state (for debugging mostly).
        :param machine: the finite state machine this belongs to.
        :param default: another **State** to fall back if we don't find what we're looking for. ``default=None``
        :param accept: a boolean stating weither a form can end at this state. ``default=False``
        """
        self.name = name
        self.machine = machine
        self.default = default
        self.is_accepting = accept

        self.transitions = {}
        


    def extend(self, ipa, suff=''):
        """
        Extends a suffix with the orthographical transduction of an IPA string.

        :param ipa: the IPA string to transduce.
        :param suff: the suffix to append after **ipa**'s transduction. ``default=""``

        :returns: ``[forms]``:

        * **[forms]** is a list of transductions matching the input IPA with **suff** concatenated at the end.
        """
        if ipa == '':
            if self.is_accepting:
                #print(self.name, ipa, suff, '####')
                return [suff]
            else:
                return []

        forms = []

        char = ipa[0]
        ipa = ipa[1:]

        #print(self.name, ipa, char, suff)
        
        if char in self.transitions:
            trans = self.transitions[char]
            #print(char, self.transitions[char])

        elif not self.default is None:
            trans = self.default.transitions[char]
            #print(char, self.default.transitions[char])

        for letters, next_state in trans:
            if next_state == 'catch_all':
                continue
            forms.extend(self.machine.states[next_state].extend(ipa, letters + suff))
        

        return forms
