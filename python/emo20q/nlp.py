#!/usr/bin/python

import re

def isReady(str):
    """
    check to see if the player is ready:
    Try to match affirmative answers to the question, are you ready? 
    """
    str = str.lower()
    match = re.search(r'\byes\b|\bready\b|\bsure\b|\bgo\b|\bok\b|\bokay\b|\byep\b|\byea\b|\byeah\b', str)
    nomatch = re.search(r'\bno\b|\bnot\b', str)
    return match and not nomatch

def classifyYN(str):
    """"Classify answers to a yes/no question into 1/yes, -1/no, or 0/other"""
    str = str.lower()
    if re.search(r'\n',str) : #only look at first line
        newstr = str.split("\n")[0]
        return classifyYN(newstr)
    
    yes = 0
    no = 0
    if re.search(r'\byes\b',str)  : yes += 1 
    if re.search(r'\byeah\b',str)  : yes += 1
    if re.search(r'\byea\b',str)  : yes += 1
    if re.search(r'\byup\b',str)  : yes += 1
    if re.search(r'\byep\b',str)  : yes += 1
    if re.search(r'\baye\b',str)  : yes += 1
    if re.search(r'\bsure\b',str)  : yes += 1
    if re.search(r'\bok\b',str)  : yes += 1
    if re.search(r'\bokay\b',str)  : yes += 1
    if re.search(r'\byou got it\b',str)  : yes += 1
    if re.search(r'\bno\b',str)  : no += 1
    if re.search(r'\bnope\b',str)  : no += 1
    if re.search(r'\bnegative\b',str)  : no += 1 #?
    # if yes and no:
    #     print str
    #     print yes
    #     print no
    if yes > 0 and no == 0:
        ans = 1
    elif no > 0 and yes == 0:
        ans = -1
    else: 
        ans=0
    return ans
    
def isAffirmative(str):
    """"Classify answers to a yes/no question into 1/yes, -1/no, or 0/other"""
    if classifyYN(str) == 1:
        return True
    return False
    

def splitCommaList(string):
    out = []
    #for x in string.split(","):
    for x in re.split(r'(?:, *(?:and)?|\band\b)', string):
        x = x.strip()
        out.append(x)
    return out

import os
import csv
import random


class GenerateDeclarative(dict):
    """
    This class will take a question gloss (semantic representation for a
    question) and generate a declarative sentence from a lookup table (this
    class inherits from dict
    
    instantiate
    >>> gd = GenerateDeclarative()

    generate/lookup
    >>> gd.generate('e.valence==negative') 
    'it is considered a negative thing to feel'

    generate using a random realization (random is seeded)
    >>> gd.generateRandom('e.valence==negative') 
    'it is a negative emotion'
    """

    def __init__(self):
        super(GenerateDeclarative,self).__init__()
        # read in the exported mysql table (compling_emo20qData db, questions table)
        datafile = os.path.dirname(__file__) + "/data/questionsTableFromCompling_emo20qData.txt"
        datareader = csv.reader(open(datafile), delimiter="\t")
        header = datareader.next()
        col = {}
        for i,c in enumerate(header):
            col[c]=i
            
        for row in datareader:
            if re.search(r'NULL', row[col["atmplt"]]): 
                continue
            if re.search(r'^\s*$', row[col["atmplt"]]): 
                continue
            #print row
            #print row[col["gloss"]], row[col["atmplt"]]
            self[row[col["gloss"]]] = row[col["atmplt"]]


        patch = os.path.dirname(__file__) + "/data/declarativeGeneratorPatch.txt"
        datareader = csv.reader(open(patch), delimiter="\t")
        header = datareader.next()
        col = {}
        for i,c in enumerate(header):
            col[c]=i

        for row in datareader:
            if re.search(r'NULL', row[col["atmplt"]]): 
                continue
            if re.search(r'^\s*$', row[col["atmplt"]]): 
                continue
            #print row
            #print row[col["gloss"]], row[col["atmplt"]]
            self[row[col["gloss"]]] = row[col["atmplt"]]

        random.seed(1)

    def __setitem__(self,key,value):
        """ this implements a dict of lists """ 
        if key in self:
            self[key].append(value)
        else:
            #if key is "e.valence==negative":
            #    print "Got it"
            super(GenerateDeclarative,self).__setitem__(key,[value])

    def generate(self,gloss):
        """generates/looks up from a semantic representation to a templated
        surface realization"""
        if gloss in self:
            return self.replace(self[gloss][0])
        else:
            #print gloss
            raise KeyError(gloss)
    def generateRandom(self,gloss):
        """generates a random realization"""
        if gloss in self:
            return self.replace(random.choice(self[gloss]))
        else:
            #print gloss
            raise KeyError(gloss)

    def replace(self,template):
        """ replaces templates in the semantic representation with default
        value """
        return re.sub(r'{(.+?):(.+?)}', r'\2', template)
    def __call__(self,gloss,ans="yes"):
        out = self.generateRandom(gloss)
        if(ans == "yes"):
            return out
        if(ans == "no"):
            return self.negate(out)
        else:
            return self.hedge(out)
    
    def negate(self,sentence):
        if re.search(r'^only',sentence):
            return re.sub(r'^only ', "not only ", sentence)
        if re.search(r' can ',sentence):
            return re.sub(r' can ', " can't ", sentence)
        if re.search(r' would ',sentence):
            return re.sub(r' would ', " wouldn't ", sentence)
        if re.search(r' is ',sentence):
            return re.sub(r' is ', r' is not ', sentence)
        if re.search(r'it [a-z]+s ',sentence):
            return re.sub(r'it ([a-z]+)s ', r"it doesn't \1 ", sentence)
        if re.search(r'(people|you) (show|feel) ',sentence):
            return re.sub(r'(people|you) (show|feel) ', r"\1 don't \2 ", sentence)
        if re.search(r' has ',sentence):
            return re.sub(r' has ', r" does not have ", sentence)
        return "not " + sentence
    def hedge(self,sentence):
        return "maybe " + sentence
        

if __name__ == "__main__":
    import doctest
    
    doctest.testmod()
    #gd = GenerateDeclarative()
    #print gd
    print "ok"
