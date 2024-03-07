from tqdm import tqdm
from random import shuffle
from os import listdir, getcwd

from app.core.Trie import Trie
from app.core.Pronunciation_state_machine import StateMachine


INITIALIZED = False

print(getcwd())


def initialize():
    """
    Initializes a number of variables and loads the necessary resources (Names with pronunciations and Expressions with pronunciations).
    """
    INITIALIZED = True

    global trie, transducer, lastjokes

    transducer = StateMachine()
    lastjokes = {}


    discard = ['.', ' ', '|', '(', ')', '͡', '‿', 'ˈ', 'ː', '̯']

    # loading names
    names = {}
    revnames = {}
    f = open('../../app/resources/names_IPA')
    for l in tqdm(f, leave=False):
        l = l.strip().split('\t')
        for c in discard:
            l[1] = l[1].replace(c, '')
            
        try:
            names[l[1]].add(l[0])
        except:
            names[l[1]] = set()
            names[l[1]].add(l[0])


    for k, vs in names.items():
        for n in vs:
            try:
                revnames[n].add(k)
            except:
                revnames[n] = set()
                revnames[n].add(k)
            


    # loading words
    words = {}
    #f = open('../french_IPA')
    f = open('../../app/resources/french_lem_only')
    for l in tqdm(f, leave=False):
        if l[0] == '-' or '/' in l:
            continue
        l = l.strip().split('\t')
        for c in discard:
            l[2] = l[2].replace(c, '')
    
        if l[2] in names:
            continue
    
        try:
            words[l[2]].add((l[1], l[0], l[3]))
        except:
            words[l[2]] = set()
            words[l[2]].add((l[1], l[0], l[3]))


    trie = Trie(words) # build the IPA trie for words

    """
    for k, vs in words.items():

        if 'approbatrice' in vs:
            
            nodes = trie.follow(k)
            print(nodes)
    """


if INITIALIZED == False:
    initialize()

    



def find(name, api=''):
    """
    Looks for the pronunciation of name and generate puns based on it.

    :param name: a string representing a first-name that will be the basis for generating puns.
    :param api: an IPA* characters string, used when the original **name** was not in the dictionary. ``default=""``

    :returns: ``(b, pron, {jokes})``: 

            * **b** is a boolean stating weither *name* was found in the dictionary; 
            * **pron** is **api** if it is not ``""``, the pronunciation of **name** if **b = True**, ``""`` otherwise; 
            * **{jokes}** is a dictionary of **name**/**pron** based puns if such could be generated.

    """

    if api == '':
        name = name[0].upper() + name[1:]
        #print(revnames)
        if name not in revnames:
            return False, name, ['<p style="font-size:28px"> We don\'t know this name. Betty luck next time. Or try in IPA.</p>']

        names = list(sorted(revnames[name]))
        pron = names[-1]

    else:
        if name == '':
            name = transducer.transduce(api+'#')[0]
            name = name[0].upper() + name[1:]
        pron = api

    l = len(pron)
    boolean, nodes = trie.follow(pron)

    if boolean == False:
        return True, pron, {}
        
    pref = nodes[-1].get_pref()

    #s = []
    out = {}
    if pref.startswith(pron):
        terms = nodes[-1].get_terminal()
        terms = [t for t in terms if t[0] != pron+'#']
        shuffle(terms)
        for i, (ipa, flu) in enumerate(terms[:5]):
            #print(lem)
            family = ipa[l:]
            ortho = transducer.transduce(family)

            #print(family, ortho)            
            form, lem, url = flu[0]
            #print(form, lem, url)
            answer = form[0].upper() + form[1:] + ' (<a href="https://en.wiktionary.org/wiki/'+url+'" target="_blank">' + lem + '</a>)'
            
            #shuffle(ortho)
            ortho.sort(key=lambda x: len(x))
            ortho = ortho[0]
            if ortho.startswith('tt'):
                ortho = ortho[1:]
            ortho = ortho[0].upper() + ortho[1:]

            out[ortho] = name, answer, str(i), ipa[l:-1]
            
            #s.append('<p style="font-size:28px">' + name + '   ' + ' '.join([p[0].upper() + p[1:] for p in transducer.transduce(family)]) + '  :  ' + lem[0][0].upper() + lem[0][1:] + '</p>')

    lastjokes['jokes'] = out
    lastjokes['name'] = name
    lastjokes['pron'] = pron
    return True, pron, out





def atrandom():
    """
    Generates jokes at random from a list of known good candidates.

    :returns: ``{jokes}``:
    
            * **{jokes}** is a dictionary of **name**/**pron** based puns.

    """

    pots = ["Abby", "Abou", "Aya", "Albane", "Ali", "Alex", "Alexis", "Alexandre", "Alain", "Amadou", "Amin", "Amine", "Amand",
            "Amanda", "Anne", "Anna", "Anatole", "Annie", "Atton", "Agathe", "Achille", "Barbe", "Blanche", "Bernard", "Brice",
            "Dominique", "Delphine", "Haydée", "Édith", "Élie", "Élise", "Emma", "Aimée", "Éva", "Fifi", "Phil", "Philippe", "Fleur",
            "Flore", "Franck", "Frank", "France", "Issa", "Yves", "Catherine", "Carla", "Claude", "Claire", "Coline", "Colin", "Corneille",
            "Lise", "Lisa", "Lou", "Loup", "Luc", "Lucie", "Laure", "Laura", "Maxime", "Marie", "Marine", "Marina", "Maria", "Marc",
            "Marthe", "Martine", "Mika", "Maud", "Maurice", "Moussa", "Morgane", "Néo", "Aude", "Auguste", "Pierre", "Planchet", "Paule",
            "Paul", "Polycarpe", "Ponce", "Sarah", "Sara", "Célia", "Céleste", "Sylvie", "Simonne", "Simone", "Sandra", "Sophie", "Cerise",
            "Serge", "Thaïs", "Théo", "Eugénie", "Ambre", "Ange", "Océane", "Océanne", "Guy", "Rémy", "Remi", "Remy", "Rémi", "Régis",
            "Réjean", "Roze", "Rose", "Roy", "Ruth", "Roch", "Romane", "Renart", "Renée", "René", "Reine", "Charles", "Jade", "Jacob",
            "Jeanne", "Gilles", "Just", "Jean"]

    shuffle(pots)

    out = {}
    for i in range(5):
        name = pots[i]
        pron = list(revnames[name])[0]

        l = len(pron)
        boolean, nodes = trie.follow(pron)
        
        pref = nodes[-1].get_pref()

        if pref.startswith(pron):
            terms = nodes[-1].get_terminal()
            terms = [t for t in terms if t[0] != pron+'#']
            shuffle(terms)

            (ipa, flu) = terms[0]
            #print(lem)
            family = ipa[l:]
            ortho = transducer.transduce(family)

            #print(family, ortho)
            form, lem, url = flu[0]
            answer = form[0].upper() + form[1:] + ' (<a href="https://en.wiktionary.org/wiki/'+url+'" target="_blank">' + lem + '</a>)'

            #shuffle(ortho)
            ortho.sort(key=lambda x: len(x))
            ortho = ortho[0]
            print(ortho)
                
            if ortho.startswith('tt'):
                ortho = ortho[1:]
            ortho = ortho[0].upper() + ortho[1:]

            out[ortho] = name, answer, str(i), ipa[l:-1]

    return out




def save(name, nameapi, jokeid, rate, comp, sensible, remarks):
    """
    Saves the evaluation of a pun by a user in a file.

    :param name: the ortographic name.
    :param nameapi: the IPA pronunciation of the joke.
    :param jokeid: an id for the joke.
    :param rate: the grade given by the user.
    :param comp: weither the user has understood the joke.
    :param sensible: weither the user rated the pun as borderline.
    :param remarks: any feedback given by the user.

    :returns: ``None``
    """
    print(name, nameapi, jokeid, rate, comp, sensible, remarks, sep=',\t')
    print(lastjokes)

    joke = [(k, v) for (k, v) in lastjokes['jokes'].items() if v[2] == str(jokeid)][0]
    
    with open('/home/mdehouck/aligator/incoming/rating', 'a') as f:
        print(name, nameapi, joke, rate, comp, sensible, remarks, sep='\t', file=f)






"""
for k, vs in sorted(names.items()):
    
    nodes = trie.follow(k)
    pref = nodes[-1].get_pref()

    if pref.startswith(k):

        for ipa, lem in nodes[-1].get_terminal():
            #print(lem)
            name = ipa.replace(k, '')
            #print(k, vs, ipa, name, transducer.transduce(name), sep='\t')

            print()
"""
