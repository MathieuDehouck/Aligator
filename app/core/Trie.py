"""
..
  a bit of Trie code
  Mathieu Dehouck / Marine Delaborde
  07/2022

Classes for making prefix trees (Tries) and aligning them.
We use those for efficiently searching IPA prefixes inside whole lexica.
"""


class Trie():
    """
    A prefix tree or trie.
    """

    def __init__(self, forms):
        """
        Creates a prefix tree (trie) from a dictionnary of forms.

        :param forms: is a ``{string:[strings]}`` dictionnary.

        :returns: ``Trie`` :

        * **Trie** is a fresh new trie filled with the given forms.
        """
        self.root = Node(None, '') # an empty string node to rule them all / or a start symbol ?
        for pron, form in forms.items():
            #node = self.root.follow(f)
            node = self.root.add(pron+'#')
            if node.forms == None:
                node.forms = set(form)
            else:
                node.forms.update(form)


    def follow(self, string):
        """
        Follows a string into the prefix tree.

        :param string: the prefix string to follow.

        :returns: ``(bool, [node])``:

        * **bool** is telling if the string has been followed to its end, 
        * **[node]** is a list containing all the nodes along the path followed.
        """
        bl, node = self.root.follow(string)
        return bl, node.ancestors()


    def align(self, other, this_suffix='', other_suffix=''):
        """
        Aligns a pair of prefix trees together.

        :param other: the other trie to align with.
        :param this_suffix: the prefix to consume from this trie before starting the new alignment proper.
        :param other_suffix: the prefix to consume from the other trie before starting the new alignment proper.

        :returns: ``(bool, [node])``

        * **bool** is telling if the string has been followed to its end, 
        * **[node]** is a list containing all the nodes along the path followed.
        
        """
        if this_suffix == '' and other_suffix == '': # both self and other are tries
            return self.root.align(other.root)
        elif this_suffix == '' and other_suffix != '': # then we know other is a node
            if other_suffix[0] == '-':
                s = other_suffix[1]
                i = 1
            else:
                s = other_suffix[0]
                i = 0
            if s in self.root.children:
                return self.root.children[s].run_align(other, other_suffix[i:])
            else:
                return []
        else:
            print(123)
            



class Node():
    """
    nodes make up a tree structure so they have a head and children.
    string is the node actual character content and forms is used to store ortographic forms cause we work with IPA
    """

    def __init__(self, head, string):
        """
        :param head: the parent of this node.
        :param string: the content of this node.

        :returns: ``node``:

        * **node** is a freshly created.
        """
        self.head = head
        self.children = {}

        self.string = string
        self.forms = None


    def find_suiting_child(self, string):
        """
        Picks the child of this node based on the first letter of the string.

        :param string: the remaining string of characters to follow in the trie.

        :returns: ``node``:

        * **node** is the **Node** whose first character matches ``string[0]``, ``None`` if there is no such node.
        """
        if string[0] in self.children:
            # if we share the first character we should follow, that's trie things
            return self.children[string[0]]
        return None


    def follow(self, string):
        """
        Recursively follows a string along the trie.

        :param string: the string of characters to follow in the trie root at the node.

        :returns: ``(bool, node)``:

        * **bool** is a **boolean** indicating weither the desired string has been fully found in the trie,
        * **node** is the last **Node** in the tree whose prefix matches ``string`` (could match only partially the prefix).
        """
        if self.string != '' and self.string[-1] == '#':
            sstring = self.string[:-1]
            end = True
        else:
            sstring = self.string
            end = False
        
        if string.startswith(sstring):
            suff = string[len(sstring):]

            if suff == '' or end == True:
                return True, self

            ch = self.find_suiting_child(suff)
            if not ch is None:
                return ch.follow(suff)
            return False, self

        else:
            return False, self
            


    def add(self, string):
        """
        Add a string to the trie.

        :param string: the string to add to the trie.

        :returns: ``node``:

        * **node** is the leaf node whose prefix matches with ``string``, creating one if necessary.
        """
        if string.startswith(self.string):
            suff = string[len(self.string):]

            if suff == '':
                return self

            ch = self.find_suiting_child(suff)
            if not ch is None:
                return ch.add(suff)
            else:
                nnode = Node(self, suff)
                self.children[suff[0]] = nnode
                return nnode

        else:
            # we have to split the current node somewhere in the middle, let's find out where
            i = 0
            while i < min(len(string), len(self.string)) and string[i] == self.string[i]:
                i += 1
            #print(i, string, self.string)

            self.string = self.string[i:] # we'll keep this node at the second half

            pref = string[:i]
            suff = string[i:]
            
            nnode = Node(self.head, pref)
            self.head.children[pref[0]] = nnode
            self.head = nnode
            
            nnode.children[suff[0]] = Node(nnode, suff)
            nnode.children[self.string[0]] = self

            return nnode.children[suff[0]]
            

    def __str__(self):
        if self.string == '':
            return '$'
        s = self.string
        return s

    
    def __repr__(self):
        if self.string == '':
            return '$'
        s = self.string
        return s


    def ancestors(self):
        """
        Returns the list of ancestors of the current node.

        :returns: ``[ancestors]``:

            * **[ancestors]** is the list of ancestors of this node.
        """
        if self.head == None:
            return [self]
        else:
            return self.head.ancestors() + [self]
        

    def get_pref(self, sep=''):
        """
        Builds the prefix corresponding to a given node, sep can be provided to separate the contribution of the various ancestors.

        :param sep: a string used to delimit the sub-string of each ancestor node. ``default=''`` 

        :returns: ``pref`` :
        
            * **prefix** is the prefix leading up to this node (this node's string included).
        """
        if self.head != None:
            pref = self.head.get_pref(sep) + sep + self.string
        else:
            pref = self.string
        return pref


    def align(self, other, depth = 0):
        """
        Match two nodes' strings and align their children with each others if relevant.

        :param other: the other **Node** to align with.
        :param depth: ``default=0`` (used for debugging purpose)

        :returns: ``[aligned]``: 

            * **[aligned]** is the list of descedant nodes from this node and another that share a their prefixes.
        """
        aligned_pairs = []

        left_node = self
        right_node = other

        if self.string == '' and other.string == '': # the only common prefix to everything is '' so we add a begin of string symbol
            left = '$'
            right = '$'
        else: # else we have running sequences
            left = self.string
            right = other.string

        #print('-'*depth, left, right, sep='\t')

        if left[0] != right[0]: # if both starts are different and one is # then we have a fully consumed word aligned with remaining possibilities
            if left[0] == '#':
                aligned_pairs = [(self, other, '#', '-'+right)]
            elif right[0] == '#':
                aligned_pairs = [(self, other, '-'+left, '#')]
            else:
                print('OUPS!!!')

        
        while left[0] == right[0]:

            if left == '#' and right == '#': # both have reached their ends
                return [(left_node, right_node, '#', '#')]

            # remove equal characters
            left = left[1:]
            right = right[1:]

            #print(left, right)

            if left == '' and right == '': # both strings have been consumed but they are not end of words
                
                if '#' in left_node.children: # the current left end point is a complete word
                    lch = left_node.children['#']
                    for rch in right_node.children.values(): # we add every children of right
                        aligned_pairs.extend(lch.align(rch, depth+1))

                if '#' in right_node.children: # same but for the right side
                    rch = right_node.children['#']
                    for s, lch in left_node.children.items():
                        if s == '#': # we have already added the end of left just above
                            continue
                        aligned_pairs.extend(lch.align(rch, depth+1))
                     
                for s, lch in left_node.children.items(): # for all remaining children who share the first letter, try to align them
                    if s == '#':
                        continue

                    if s in right_node.children:
                        aligned_pairs.extend(lch.align(right_node.children[s], depth+1))

                return aligned_pairs


            elif left == '#' and right != '#': # if we have reached an end of word and there remain unconsumed characters in the other string
                if right == '':
                    return [(left_node, rch, '#', rch.string) for rch in right_node.children.values()]
                else:
                    return [(left_node, right_node, '#', '-'+right)]

            elif right == '#' and left != '#':
                if left == '':
                    return [(lch, right_node, lch.string, '#') for lch in left_node.children.values()]
                else:
                    return [(left_node, right_node, '-'+left, '#')]


            elif left == '': # if we have consumed all of left but there remains some characters in right, there is only one left child interesting
                s = right[0]
                if s in left_node.children:
                    left_node = left_node.children[s]
                    left = left_node.string
                    #print('lr', left, right)
                elif '#' in left_node.children:
                    return [(left_node.children['#'], right_node, '#', '-'+right)]
                else:
                    return []
                
            elif right == '': # same as above but roles inversed
                s = left[0]
                if s in right_node.children:
                    right_node = right_node.children[s]
                    right = right_node.string
                    #print('rl', left, right)
                elif '#' in right_node.children:
                    return [(left_node, right_node.children['#'], '-'+left, '#')]
                else:
                    return []

        return aligned_pairs



    def run_align(self, other, other_suffix):
        """
        Matches two nodes' strings and align their children with each others if relevant
        assuming we have already partially consumed the other nodes string

        :param other: the other **Node** to align with.
        :param other_suffix: a string representing the suffix remaining to consume in the other node. Useful when one wants to align several tries after each other.

        :returns: ``[aligned]``: 

            * **[aligned]** is the list of descedant nodes from this node and another that share a their prefixes.
        
        """
        aligned_pairs = []

        left_node = self
        right_node = other

        left = self.string
        right = other_suffix

        print(left_node, right_node, left, right, sep='\t')
        #print('-'*depth, left, right, sep='\t')

        if left[0] != right[0]: # if both starts are different and one is # then we have a fully consumed word aligned with remaining possibilities
            if left[0] == '#':
                aligned_pairs = [(self, other, '#', '-'+right)]
            elif right[0] == '#':
                aligned_pairs = [(self, other, '-'+left, '#')]
            else:
                print('OUPS!!!')

        
        while left[0] == right[0]:

            if left == '#' and right == '#': # both have reached their ends
                return [(left_node, right_node, '#', '#')]

            # remove equal characters
            left = left[1:]
            right = right[1:]

            #print(left, right)
            
            if left == '' and right == '': # both strings have been consumed but they are not end of words
                
                if '#' in left_node.children: # the current left end point is a complete word
                    lch = left_node.children['#']
                    for rch in right_node.children.values(): # we add every children of right
                        aligned_pairs.extend(lch.align(rch, 0))

                if '#' in right_node.children: # same but for the right side
                    rch = right_node.children['#']
                    for s, lch in left_node.children.items():
                        if s == '#': # we have already added the end of left just above
                            continue
                        aligned_pairs.extend(lch.align(rch, 0))
                     
                for s, lch in left_node.children.items(): # for all remaining children who share the first letter, try to align them
                    if s == '#':
                        continue

                    if s in right_node.children:
                        aligned_pairs.extend(lch.align(right_node.children[s], 0))

                return aligned_pairs


            elif left == '#' and right != '#': # if we have reached an end of word and there remain unconsumed characters in the other string
                if right == '':
                    return [(left_node, rch, '#', rch.string) for rch in right_node.children.values()]
                else:
                    return [(left_node, right_node, '#', '-'+right)]

            elif right == '#' and left != '#':
                if left == '':
                    return [(lch, right_node, lch.string, '#') for lch in left_node.children.values()]
                else:
                    return [(left_node, right_node, '-'+left, '#')]


            elif left == '': # if we have consumed all of left but there remains some characters in right, there is only one left child interesting
                s = right[0]
                if s in left_node.children:
                    left_node = left_node.children[s]
                    left = left_node.string
                    #print('lr', left, right)
                elif '#' in left_node.children:
                    return [(left_node.children['#'], right_node, '#', '-'+right)]
                else:
                    return []
                
            elif right == '': # same as above but roles inversed
                s = left[0]
                if s in right_node.children:
                    right_node = right_node.children[s]
                    right = right_node.string
                    #print('rl', left, right)
                elif '#' in right_node.children:
                    return [(left_node, right_node.children['#'], '-'+left, '#')]
                else:
                    return []

        return aligned_pairs


    
    def print_tree(self, pref=''):
        """
        Follows the tree from a given node and prints all the prefixes of its descendants.

        :param pref: a string to prefix to each descendant of this node. ``default=''``
        
        :returns: ``string``: 

            * **string** a string made up of all the suffixes rooted at self as a tree, each on its own line.

        """        
        if pref == '':
            pref = self.get_pref()
            s = pref + '\n'
        else:
            pref += '.' + self.string
            s = pref + '\n'

        for k, ch in sorted(self.children.items()):
            s += ch.print_tree(pref)

        return s


    def print_terminal(self, pref=''):
        """
        Follows the tree from a given node and prints all the forms corresponding to leaf nodes.

        :param pref: a string to prefix to each descendant of this node. ``default=''``
        
        :returns: ``string``: 

            * **string** a string made up of all terminal suffixes rooted at self, each on its own line.
        """
        if pref == '':
            pref = self.get_pref()
        else:
            pref = pref + self.string

        if self.string[-1] == '#':
            s = pref + '\t' + str(sorted(self.forms)) + '\n'
        else:
            s = ''.join([ch.print_terminal(pref) for k, ch in sorted(self.children.items())])

        return s


    def get_terminal(self, pref=''):
        """
        Follows the tree from a given node and returns all the forms corresponding to leaf nodes.

        :param pref: a string to prefix to each descendant of this node. ``default=''``
        
        :returns: ``[terminals]``: 

            * **[terminals]** is a list of (prefix, leaf node) each representing a leaf/terminal descending from ``self``.
        """
        if pref == '':
            pref = self.get_pref()
        else:
            pref = pref + self.string # there could be some overlap here, beware !!!

        if self.string[-1] == '#':
            s = [(pref, sorted(self.forms))]
        else:
            s = []
            for k, ch in sorted(self.children.items()):
                s.extend(ch.get_terminal(pref))

        return s

    
    
    
