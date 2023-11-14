"""
..
  a few methods to make, save and load POS-morph tries
  Marine Delaborde, Mathieu Dehouck
  10/2022

  used in V2
"""
from tqdm import tqdm
from copy import deepcopy
from os import listdir

from Trie import Trie
from morphalou_scripts.Morphalou2UD import morph2UD, pos2UD, irrelevant


def read_file(fname):
    data = []
    fl = open(fname)
    
    for l in fl:
        l = l.strip()
        l = l.replace("'", "").replace('(', '').replace(')', '')
        l = l.split('\t')
        l[1] = l[1].replace(' ', '').replace('ɔ̃', 'ɔ~').replace('ɛ̃', 'ɛ~').replace('ɑ̃', 'ɑ~').replace('œ̃', 'œ~').split(',')
        
        if 'plural' in fname:
            l.append('+C')
            
            l2 = deepcopy(l)
            l2[1][0] += 'z'
            l2[2] = '+V'

            data.append(l2)

        if len(l) == 2:
            l.append('+CV')

        data.append(l)

    return data



def read_file_with_morpho(fname):
    data = {}
    fl = open(fname)
    
    for l in fl:
        l = l.strip()
        l = l.replace('(', '').replace(')', '')
        l = l.split('\t')
        l[1] = l[1].replace("'",'').replace(' ', '').replace('ɔ̃', 'ɔ~').replace('ɛ̃', 'ɛ~').replace('ɑ̃', 'ɑ~').replace('œ̃', 'œ~').split(',')

        try:
            data[2].append(l)
        except:
            data[2] = [l]

    return data



def make_tries():
    tries = {'NOUN':{}, 'DET':{}, 'ADJ':{}, 'PRON':{}, 'CCONJ':{}}
    dname = 'morphalou_scripts/sorted/'

    for fname in listdir(dname):
        if 'DET' in fname:
            morph = fname.split('_')[-1]

            forms = read_file(dname+fname)
            tries['DET'][morph] = Trie({ipa[0]:(form, cv) for form, ipa, cv in forms})


    for num in ['singular', 'plural']:
        for gen in ['feminine', 'masculine']:#, 'invariable']:

            flex = num + '_' + gen
            flexUD = morph2UD[gen] + '|' + morph2UD[num]
            
            fname = 'Nom commun_' + flex
            forms = read_file(dname+fname)
            tries['NOUN'][flexUD] = Trie({ipa[0]:(form, cv) for form, ipa, cv in forms})

            fname = 'Adjectif qualificatif_' + flex
            forms = read_file(dname+fname)
            tries['ADJ'][flexUD] = Trie({ipa[0]:(form, cv) for form, ipa, cv in forms})

    forms = read_file('pos_files/CCONJ')
    tries['CCONJ'] = {'_':Trie({ipa[0]:(form, cv) for form, ipa, cv in forms})}

    forms = read_file(dname+'/ADV')
    tries['ADV'] = {'_':Trie({ipa[0]:(form, cv) for form, ipa, cv in forms})}
            
    #prons = read_file_with_morpho()
            
            
    return tries






def read_list_struct(fname):
    """
    reads a file containing lists representing syntax and morphology
    ['1', 'CCONJ', '_', '3', 'cc']
    ['2', 'ADV', '_', '3', 'advmod']
    ['3', 'VERB', 'VerbForm=Inf', '0', 'root']
    """

    data = [[]]
    with open(fname) as f:
        for l in f:
            l = l.strip().replace("'",'').split(', ')
            if l == ['']:
                data.append([])
                continue

            l[2] = '|'.join((x for x in l[2].split('|') if x not in irrelevant))
            data[-1].append(l[1:3])

    return data[:-1]
