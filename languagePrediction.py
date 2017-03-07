# file: wBabisAss6.py
# author: Billy Babis
# date: 3/15/14
#

## This code was an assingment for my Randomness and Computation course
## Essentially, we are looking to determine the language of a given string
## This is done by creating dictionary (or language model) of given n-gram sequences
  ## and their probabilities.
  ## the "n-gram" refers to the number of letters used for our predictive modelling.
    ##So, if n=4 and we perform a 4-gram analysis, it will iterate thorugh our sentence 4 letters at a time

## This language detection algorithm does not test the frequency of certain words, but instead
##   tests the frequency of sub-strings of length n followed by a certain character.
## for example, (n=4) the 4 character substring "chum" will usually be followed by "p"

##works slowly, as anticipated by our professor.

#from pylab import *

print "Call the function predictLanguage(n,s) with your n-gram choice and input string s"
print "Only available languages are english, french, italian, german, portuguese, and spanish. Uses English letters."


import math

abc = ' abcdefghijklmnopqrstuvwxyz'


## Called in the above function. If the string sequence "s" is in the dictionary, add
  ## one to the frequency. Otherwise, create a new key with value 1.
def create_language_model(s, n):
    model = {}
    n=n-1       # simply for compatible string iteration
    for i in range(len(s) - n):
        subStr = s[i: i + n]
        nextChar = (s[i + n]).lower()
        if subStr not in model:
            newSubStr_dic = {}
            for c in abc:
                newSubStr_dic[c]=0
            model[subStr] = newSubStr_dic
        model[subStr][nextChar] += 1
    ##turn those frequency integers into fractions
    for i in range(len(s) - n):
        subStr = s[i: i + n]
        denom = sum( model[subStr].values() )
        for c in abc:
            model[subStr][c] = float(model[subStr][c]) / float(denom)
    return model


## Given a language model and a string s on an n-gram analysis, a fairly arbitrary scoring algorithm
    ## finds the probability that the sample is a given language
    ## The language model with lowest score will be our the most probable.
def findScore(model, s, n):
    probSum = 0
    n=n-1
    for j in range(len(s) - n):
        subStr = s[j: j + n]
        nextChar = (s[j+n]).lower()
        if subStr in model:
            prob = model[subStr][nextChar]
        else:
            prob = 1.0/50

        num = float(-math.log(prob)) if prob!=0 else 1.0/50
        probSum += num 
            
    return probSum / float(len(s))
        
            

#This will perform an n-gram analysis of String s, yielding the scores of each 6 language
#The language with the lowest score is the language of sting s
def predictLanguage(n, s):
    s = s.replace('.','').replace(',','')
    scores = {'english':3}
    langz = ['english', 'french', 'italian', 'german', 'portuguese', 'spanish']
    path = 'langz/'
    minLang = "english"
    for lang in langz:
        infile = open(path + lang + '_training.txt', 'r')
        sampleLanguageText = infile.read()
        infile.close()
        languageModel = create_language_model(sampleLanguageText, n)
        score = findScore(languageModel, s, n)
        print lang
        print score
        scores[lang]=score
        if score<scores[minLang]:
            minLang = lang

    if scores[minLang] > 3:
        print "This is an unknown Language. Try a larger n-value or a longer sentence"
        return None
    else:
        ##check to make sure our results are probable
        for lang in scores:
            difference = scores[lang] - scores[minLang] 
            if difference<.15 and difference!=0:
                print difference
                print "Similar language results: no conclusion. Try a larger n-value or a longer sentence"
                return None
        print "The results suggest that this language is: " + minLang
        return minLang  





inputStr="This is my sample english sentence to be tested with my language prediction algorithm. I will use fairly long words like programming, artificial intelligence, and probability to improve acccuracy" 
print " "
print "Results for n=6 and input string: "
print inputStr
print predictLanguage(6, inputStr)



         
### ---------  some extras ----------




import numpy.random as np
    
    ## This will take in a language model and use the probabilites in that model to create
  ## a string of length k with starting point string "seed"
def get_sample(model, k, seed):
    abcLst = []
    for i in range(27):
        abcLst.append(abc[i])
    sentence = seed
    n = len(seed)
    for i in range(k):
        probz = model[sentence[i: i + (n)]]
        nextLetter = np.choice(abcLst, p =probz)
        sentence = sentence + nextLetter
    return sentence

## Will read in the training texts and develop a dictionary of letter-sequence frequencies
def get_language_model(n):  #input: n-gram analysis
    langList = ['english', 'french', 'italian', 'german', 'portuguese', 'spanish']
    path = 'langz/'
    langDict = {}
    for lang in langList:
        infile = open(path + lang + '_training.txt', 'r')
        s = infile.read()
        infile.close()
        model = create_language_model(s, n)
        langDict[lang] = model
    return langDict
