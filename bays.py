
from numpy import *
def loadDataSet():
	postingList = [['my','dog','has','flea','problems','help','please'],\
			['maybe','not','take','him','to','dog','park','stupid'],\
			['my','dalmation','is','so','cute','I','love','him'],\
			['stop','posting','stupid','worthless','garbage'],\
			['mr','licks','ate','my','steak','how','to','stop','him'],\
			['quit','buying','worthless','dog','food''stupid']
			]
	classVec = [0,1,0,1,0,1]  #1代表侮辱性的文字 0代表正常言论
	return postingList,classVec

def createVocabList(dataSet):
	vocabSet = set({})
	for document in dataSet:
		vocabSet = vocabSet| set(document)
	return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
	returnVec = [0]*len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)]=1
		else:
			print("the word: %s is not in my Vocabulary" % word)
	return returnVec

def bagOfWords2Vec(vocabList,inputSet):
        returnVec = [0]*len(vocabList)
        for word in inputSet:
                if word in vocabList:
                        returnVec[vocabList.index(word)] += 1
                else:
                        print("the word: %s is not in my Vocabulary" % word)
        return returnVec

def trainNB0(trainMatrix,trainCategory):
	numTrainDocs = len(trainMatrix) #文档矩阵
	numWords = len(trainMatrix[0])
	pAbusive = sum(trainCategory)/float(numTrainDocs)
	#print(numTrainDocs)
	#print(numTrainDocs)
	p0Num = ones(numWords)
	p1Num = ones(numWords)
	p0Denom = 2.0
	p1Denom = 2.0
	#print(numWords)
	#print(p0Num,p1Num)
	for i in range(numTrainDocs):
		if trainCategory[i]==1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	#print("=================")
	#print(p1Num)
	#print(p0Num)
	#print(p1Denom)
	#print(p0Denom)
	#print("=================")
	p1Vect = log(p1Num/p1Denom)
	p0Vect = log(p0Num/p0Denom)
	return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
	p1 = sum(vec2Classify * p1Vec) + log(pClass1)
	p0 = sum(vec2Classify * p0Vec) + log(1.0-pClass1)
	if p1 > p0:
		return 1
	else:
		return 0

def testingNB():
	listOPosts,listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
	p0V,p1V,pAb = trainNB0(trainMat,listClasses)
	testEntry = ['love','my','dalmatin']
	thisDoc = array(setOfWords2Vec(myVocabList,testEntry))
	print(testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb))
	
	secondEntry = ['stupid','garbage']
	secondDoc = array(setOfWords2Vec(myVocabList,secondEntry))
	print(secondEntry,'classified as:',classifyNB(secondDoc,p0V,p1V,pAb))

def testDataSet():
	listOPosts,listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	print(myVocabList)
	#words2Vec = setOfWords2Vec(myVocabList,listOPosts[0])
	#print(words2Vec)

	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
	print(trainMat)
	p0V,p1V,pAb = trainNB0(trainMat,listClasses)
	print(p0V)
	print(p1V)
	print(pAb)

def textParse(bigString):
	import re
	listOfTokens = re.split('\W+',bigString)
	#print(listOfTokens)
	return [tok.lower() for tok in listOfTokens if len(tok)>2]

def spamTest():
	docList=[]
	classList=[]
	fullText=[]
	for i in range(1,26):
		#print("================",i)
		wordList=textParse(open('./data/email/spam/%d.txt' % i,'r',encoding='gbk').read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open('./data/email/ham/%d.txt' %i,'r',encoding='gbk').read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = createVocabList(docList)
	trainingSet = list(range(50))
	testSet=[]
	for i in range(10):
		randIndex = int(random.uniform(0,len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat=[]
	trainClasses=[]
	#print(len(docList))
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
	errorCount=0
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList,docList[docIndex])
		if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
			errorCount +=1
	print('the error rate is ',float(errorCount/len(testSet)))

if __name__=='__main__':
	#testingNB()
	spamTest()
