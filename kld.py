#!/usr/bin/python
# Emily Davis
# Ashton Stephens
# Information Theory
# Kullback-Leibler Distance 


import sys
import string
import collections
from collections import namedtuple
import math

epsilon = .0001

# takes in the training filename and returns a dictionary containing
# words as the key and a named tuple of class probabilites of that word
# as the values
def getTrainDist (fname):
    	training_dict = {}
	trainset = open(fname, 'r')
	for line in trainset:
		if (line == "\n"):
			pass
		else:	#extracts data from line and adds it to dictionary
			training_dict = processLine (line, training_dict)

	totposwords = 0	#running totals for class word counts
	totnegwords = 0
	for x in training_dict:
		totposwords = totposwords + training_dict[x].poscount
		totnegwords = totnegwords + training_dict[x].negcount

	probabilities = training_dict.copy()

	#prevent division by 0 when no positive or no negative words were in
	#training doc
	if (totposwords == 0):
		totposwords = 1
	if (totnegwords == 0):
		totnegwords = 1

	#convert counts into probabilities
	for x in probabilities:
		probabilities[x].poscount = float(training_dict[x].poscount) / totposwords
		probabilities[x].negcount = float(training_dict[x].negcount) / totnegwords	

	return probabilities

# takes in a training example to process and updates the dictionary
def processLine (ln, dic):
	#epsilon = .0001

	cls = (ln[-2:])[:-1]
	ln = ln[:-3].lower()
	ln = ''.join(e for e in ln if e not in string.punctuation)
	ln = ln.split(" ")


	for j in range(0, len(ln)): 
	    	currkey = ln[j]
	    	if (currkey in dic):
			if (cls == '0'):
		   		dic[currkey].negcount += 1
			elif (cls == '1'):
		    		dic[currkey].poscount += 1
			else:
		    		print ('this should not happen')
	    	else:
		#create a dictionary entry for new word
			wcounts = collections.namedtuple('wcounts', 'poscount negcount')
		
			if (cls == '0'):
	   			wcounts.poscount = epsilon
	    			wcounts.negcount = 1
	    			dic[currkey] = wcounts
	       		else:
	    			wcounts.poscount = 1
	    			wcounts.negcount = epsilon
	    			dic.update({currkey:wcounts})

	return dic

# takes in test filename and dictionary with training class distributions
# returns a list of tuples containing test examples true and
# predicted classifications
def classifyTestData(fname, trainDist):
	testfile = open(fname, 'r')
	
	classifications = []

	#process each document/example in test data
	for doc in testfile:
		if (doc == '\n'):
			pass
		else:
			classifications = classifydoc(doc, trainDist, classifications)
	return classifications

# takes in a document to classify, the training distributions, and the
# list of classifications so far.  Returns an updated list
# including the classification for the new doc
def classifydoc(doc, trainDist, myClassifications):
	
	#get document probability distribution and 
	#actual document class
	processDoc = getdocDist(doc, trainDist)
	docDist = processDoc[0]
	cls = processDoc[1]	

	#find KL distance between doc and each class
	negDist = KLDistance(docDist, trainDist, 0)
	posDist = KLDistance(docDist, trainDist, 1)

	predvsreality = collections.namedtuple('predvsreality', 'pred real line')
	predvsreality.real = cls
	predvsreality.line = doc

	#doc dist is closer to pos class dist, classify doc as pos
	if (posDist <= negDist):
		predvsreality.pred = '1'
		myClassifications.append(predvsreality)

	else: #otherwise classify doc as neg
		predvsreality.pred = '0'
		myClassifications.append(predvsreality)

	return myClassifications


def KLDistance(dDist, tDist, cls):
	mysum = 0
	for x in tDist:
		
		px = dDist[x]

		if (cls == 0):
			qx = tDist[x].negcount
		elif (cls == 1):
			qx = tDist[x].poscount

		mysum = mysum + (px - qx)*(math.log((px/qx), 2))

	return mysum

# Takes a document to be classified and the training distribution.
# Returns a dictionary with the probabilities of the 
# training vocabulary in the new doc.
def getdocDist(doc, trainDist):

	cls = (doc[-2:])[:-1]
        doc = doc[:-3].lower()
        doc = ''.join(e for e in doc if e not in string.punctuation)
        doc = doc.split(" ")
	

	docdict = {}
	wc = 0

	for j in range(0, len(doc)):
		currkey = doc[j]		

		#ignore words not in dictionary
		if (currkey not in trainDist):
			pass
		else:	
			wc = wc + 1		
			
			#update word count if already in doc dictionary
			if (currkey in docdict):
				docdict[currkey] = docdict[currkey] + 1

			#insert to doc dictionary if not already there
			else:
				docdict.update({currkey:1})

	#convert counts to probabilities
	for x in docdict:
		docdict[x] = float(docdict[x]) / wc 

	#set probabilites of words that did not appear to be
	#some fixed epsilon so that we will not have 
	#division by 0		
	for x in trainDist:
		if (x not in docdict):
			docdict.update({x:epsilon})

	return [docdict, cls]

#takes list of predicted classes and actual classes
#and returns accuracy	
def computeAccuracy(mycls, printwrongs):

	numexs = 0
	numcorrect = 0
	numwrong = 0

	for doc in mycls:

		numexs = numexs + 1

		if (doc.pred == doc.real):
			numcorrect = numcorrect + 1
			
		else:
			numwrong = numwrong + 1
			if (printwrongs == "true"):
				print doc.line

	myacc = float(numcorrect)/numexs

	return myacc


def main (trainfile, testfile, printwrongs):
    	trainDist = getTrainDist(trainfile)
    	classifications = classifyTestData(testfile, trainDist)

	accuracy = computeAccuracy(classifications, printwrongs)


	print ('accuracy: %.4f' % accuracy)

main(sys.argv[1], sys.argv[2], sys.argv[3])










