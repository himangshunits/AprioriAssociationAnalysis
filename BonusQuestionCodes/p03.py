path = "transaction.mat"
pathItemsets = "frequentitemsets.txt"
pathRules = "rules.txt"




'''
Solutions to Assignment 4(Problem 3, Bonus Question)
ALDA CSC 522
Fall 2015
NC State University

Implentation of the Apriori algorithm to find the maximal frequent itemsets, then generate rules for apriori 
algorithm with minimum support min sup = 4% and min conf = 10%. Output your frequent itemsets to frequentitemsets.txt, 
and rules to rules.txt, in the same folder where it is run from.

Team : 
Himangshu Ranjan Borah(hborah)
Sukriti Sharma(ssharm18)
Sushma Ravichandran(sravich)

Referrences:
1. Textbook(Tan, Steinbach, Kumar)
2. Agrawal, Rakesh, Heikki Mannila, Ramakrishnan Srikant, Hannu Toivonen, and A. Inkeri Verkamo. 
    "Fast Discovery of Association Rules." Advances in knowledge discovery and data mining 12, no. 1 (1996): 307-328.

NB : Parts of the code below uses ideas learnt from the above referrences.

Ruuning Instructions:

1. Please check the path above for loading the matrix and saving the outputs and set it to personal need.
	if the paths are not changed, then it searches for the transaction.mat in the current folder and also saves the output to current folder
    -> So if you are not already in the directory where you have put the transaction.mat, please navigate to that or change the paths !
2. Please enter in the form of python filename.py <minSup> <minConf> and run.
3. minSup should be the exact number, like if 4% of 1000 items, then minSup = 40
4. minConf should be a fraction, if 10%, then minConf = 0.1
5. Sample run command as per personal system
"/User/Himangshu/p03.py 40 0.1"


Sample path settings:
path = "/Users/Himangshu/Desktop/AprioriDataset/transaction.mat"
pathItemsets = "/Users/Himangshu/Desktop/AprioriDataset/frequentitemsets.txt"
pathRules = "/Users/Himangshu/Desktop/AprioriDataset/rules.txt"


'''




import scipy.io as sio
from itertools import combinations
import numpy
import sys


# Filter the Candidates
def generateFk(supportCounts, minSup):
	result = dict()

	for candidate, count in supportCounts.iteritems():
		if count >= minSup:
			result[candidate] = count

	return result


# Writing the itemsets to file
def dumpFreqItemsetsToFile(path, F):
	myFile = open(path, "wb")

	for i in F.itervalues():
		for j in i.iterkeys():
			for k in j:
				myFile.write(str(k))
				myFile.write(", ")

			myFile.write("\n")
	myFile.close()



# writing the rules to file
def dumpRulesToFile(rules, path):
	# Print to file
	myFile = open(path, "wb")
	for a, b in rules:
		for a1 in a:
			myFile.write(str(a1))
			myFile.write(", ")	
		myFile.write("  --->  ")
		for b1 in b:
			myFile.write(str(b1))
			myFile.write(", ")	
		myFile.write("\n")
	myFile.close()



# Find the subsets contained in a transaction. using Naive method.
# TODO: Can be made more efficient
def subsetFinder(Ck, t):
	result = list()
	for c_i in Ck.iterkeys():
		if all(item in t for item in c_i):
			result.append(c_i)

	return result


# Generate the candidate subsets
# We use the second approach given in texbook for this part, merging the F(k-1)
# Please refer to texbook for details
def aprioriGen(FPrevious, k):

    Ck = dict()

    # Find the already finalised itemsets till now.
    confirmedItemsets = list()
    for key in FPrevious.iterkeys():
    	confirmedItemsets.append(set(key))

    possiblePairs = combinations(FPrevious, 2)

    for a_i, b_i in possiblePairs:
    	# Check if the first n - 1 items match.
        flag = True
        for i in range(0, k - 2):
            if a_i[i] != b_i[i]:
                flag = False;
        if flag:
            # Sor the remaining of the list lexicographically and combine
            rest = tuple(sorted((a_i[k-1], b_i[k-1])))
            posCan = a_i[0:k-1] + rest
            # Check if all the proper subsets are safe, if yes then insert it to dictionary
            # This refers to the prunning mentioned in book
            if isSafe(posCan, confirmedItemsets, k):
                Ck[posCan] = 0
    return Ck

# Utility fucntion used by aprioriGen
def isSafe(posCan, confirmedItemsets, k):
	#find proper subsets
	properSubsets = combinations(posCan, k)
	for prop in properSubsets:
		setProp = set(prop)
		if setProp not in confirmedItemsets:
			return False
	return True




# This is the main function which generates the Frequent itemsets
# Refre to pseudo code given in Texbook
# DataDict is the input database stored in a hashMap
def getFreqItemsets(DataDict, minSup):

    itemCounts = dict()

    # Inititalize the counters
    for tid in DataDict.itervalues():
        for item in tid:
            itemCounts[item] = 0

    for tid in DataDict.itervalues():
        for item in tid:
            itemCounts[item] += 1   

    k = 0
    # Maintain the frequent itemsets
    F = {k: dict()} 
      
    # generate 1 Frequent Itemsets      
    for i in itemCounts.keys():
    	if itemCounts[i] >= minSup:
    		F[0][(i,)] = itemCounts[i]    

    while F[k]:
    	k = k + 1
        Ck = aprioriGen(F[k-1], k)
        
        supportCounts = dict()        
        for i in Ck:
        	supportCounts[i] = 0

        for transaction in DataDict.itervalues():
            Ct = subsetFinder(Ck, transaction)            

            for c in Ct:
                supportCounts[c] += 1

        # Filter the Candidates
        F[k] = generateFk(supportCounts, minSup)
	
    return F





###### Itemset finding over
##### Below is the rule generation code

def ExtractRules(F, minConf):
    
    result = set()   
	
    # Get the itemsets in an enumerted list
    fkList = sorted(F.iteritems())
    # Now iterate through all the possible itemsets for different values of k
    for k, Fk in fkList:
        ruleK = set()
        # pick an item each time
        for itemSet, supCount in Fk.iteritems():
            # Find the one item consequents of the rule
            HOne = dict()
            for item in itemSet:
            	HOne[(item,)] = supCount

            ruleK = GenerateRules(F, itemSet, supCount, k, HOne, 0,
                                         minConf)			

            # Handle the signleton subsets of itemset as they are not handled by the above recurison
            for item in itemSet:              
                elem1 = [item]
                elem = set(elem1)
                itemSetSet = set(itemSet)
                diffSet = itemSetSet - elem
                diffTuple = tuple(sorted(tuple(diffSet)))

                if len(diffTuple):
                    supportOfDiff = float(F[len(diffTuple)-1][diffTuple])
                else:
                    supportOfDiff = float(sum(F[0].values()))
                    

                conf = supCount / supportOfDiff
                if conf >= minConf:
                    ruleK.add((diffTuple,(item,) ))

            # Merge the sets
            result = result | ruleK
            
    return result




def GenerateRules(F, itemSet, supCount, k, hCurrent, m, minConf):
	# Handle base case
    if k <= m + 1:
    	empty = set()
        return empty
    
    rules = set()

    # genrate next possible candidates using the aprioriGen
    hNext = aprioriGen(hCurrent, m + 1)


    for ruleSet in hNext.keys():
    	# Find the set difference
    	setDiff = (set(itemSet)) - (set(ruleSet))
    	diffTuple = tuple(sorted(setDiff))
        tupleLen = len(diffTuple)
        # Locate the difftuple in the largest itemset's dictionary and get the value
        diffSupport = float(F[tupleLen - 1][diffTuple])
        
        conf = supCount / diffSupport
        # check whether to keep or delete the ruleSet
        if conf >= minConf:
        	# We store the rules
            rules.add((diffTuple, ruleSet))
        else:
        	# Remove entry from dictionary
            del hNext[ruleSet]
    m = m + 1        
    currentRules = GenerateRules(F, itemSet, supCount, k, hNext, m,
                              minConf)

    rules = rules | currentRules

    return rules



if __name__ == '__main__':

	# Get the minimum support and confidence from command line
	try:
		minSup = float(sys.argv[1])
		minConf = float(sys.argv[2])
	except:
		print 'Input format invalid ! Please enter in the form of python filename.py <minSup> <minConf>'
		print "Sample usage >>> python p03.py 40 0.10"
		sys.exit(0)

    # Pull the data from the matrix file

	dataMatrix = sio.loadmat(path)
	dataSet = dataMatrix['transaction']

	maxItem = len(dataSet[1, :])
	maxTrans = len(dataSet[:, 1])

	resultDict = dict()

	for t in range(0, maxTrans):
		tempList = []
		for item in range(0, maxItem):
			if dataSet[t][item] == 1:
				tempList.append(item + 1)
		resultDict[t + 1] = tuple(tempList)

	# Get the frequent itemsets and dump to file	

	itemSets = getFreqItemsets(resultDict, minSup)
	#for i in itemSets.itervalues():
		#for j in i.iterkeys():
	#		print i
	#		print "\n"

	dumpFreqItemsetsToFile(pathItemsets, itemSets)

	# Extract the rules and dump to file
	rules = ExtractRules(itemSets, minConf)


	#for a,b in rules:
	#	print a
	#	print "######"
	#	print b
	#	print "\n"

	dumpRulesToFile(rules, pathRules)

	print "Rules Extracted successfully ! Please check your directory for the files frequentitemsets.txt and rules.txt."