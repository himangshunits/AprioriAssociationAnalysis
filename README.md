# AprioriAssociationAnalysis
###Python Code for Apriori Algorithm, for CSC 522 NC State University


Solutions to Assignment 4(Problem 3, Bonus Question)

ALDA CSC 522

Fall 2015

NC State University

Implentation of the Apriori algorithm to find the maximal frequent itemsets, then generate rules for apriori 
algorithm with minimum support min sup = 4% and min conf = 10%. Output your frequent itemsets to frequentitemsets.txt, 
and rules to rules.txt, in the same folder where it is run from.

Team : 
1. Himangshu Ranjan Borah(hborah)
2. Sukriti Sharma(ssharm18)
3. Sushma Ravichandran(sravich)

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

The Original Question for the Code Above:

Given transaction.mat, which is a 1000*50 matrix, where each row represents a trans-
action while each column means an item, if item i exist in the transact j, then Tij = 1,
else Tij = 0. Implement the Apriori algorithm to nd the maximal frequent itemsets,
then generate rules for apriori algorithm with minimum support min sup = 40% Plot
the results including item sets and rules. Name your le p03.extension (R or matlab or
python). The First line of your code should be a variable named path where you store
the path to the dataset.
