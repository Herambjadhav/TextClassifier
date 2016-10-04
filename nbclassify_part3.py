import os
import sys

specialSymbols = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"

stopWords = {"a", "an", "and", "are", "as", "at", "be", "but", "by",
"for", "if", "in", "into", "is", "it",
"no", "not", "of", "on", "or", "such",
"that", "the", "their", "then", "there", "these",
"they", "this", "to", "was", "will", "with"}

def classify(fileHandler, vocabulary, spam, ham):
    lines = fileHandler.readlines()
    wordList = []
    for line in lines:
        for word in line.split():
            wordList.append(word)

    spamMsgProb = 1.0
    hamMsgProb = 1.0
    spamMsgLog = 0.0
    hamMsgLog = 0.0
    for word in wordList:
        if word in vocabulary:
            if len(word) == 1 and word in specialSymbols:
                continue
            if len(word) == 1 and word in stopWords:
                continue
            counts = vocabulary[word]
            spamMsgProb = spamMsgProb * counts['SP']
            spamMsgLog += counts['SL']
            hamMsgProb = hamMsgProb * counts['HP']
            hamMsgLog += counts['HL']

    spamProb = (spam['log'] + spamMsgLog)
    hamProb = (ham['log'] + hamMsgLog)

    if spamProb > hamProb:
        return 1
    else:
        return 2

print ('Argument count : ', len(sys.argv))
#exit if file name is not provided as command line argument
if len(sys.argv) != 2:
    print ('Please send file name as command line argument')
    exit(0)

rootdir = sys.argv[1]
print ('Root Dir : ', rootdir)

# read model.txt
fileHandler = open('nbmodel.txt', 'r', encoding="latin1")
lines = fileHandler.readlines()
fileHandler.close()

spam = {}
spam['prob'] = float(lines[0].split()[0])
spam['log'] = float(lines[0].split()[1])

ham = {}
ham['prob'] = float(lines[1].split()[0])
ham['log'] = float(lines[1].split()[1])

#print (spam, ham)

vocabulary = {}

#build vocab dictionary
for line in lines[3:]:
    word = line.split()
    counts = {}
    counts['SP'] = float(word[1])
    counts['SL'] = float(word[2])
    counts['HP'] = float(word[3])
    counts['HL'] = float(word[4])
    vocabulary[word[0]] = counts

#print(len(vocabulary))

spamCount = 0
notSpamCount = 0
hamCount = 0
notHamCount = 0
fileCount = 0
totalSpam = 0
totalHam = 0
# read files and classify
outputFile = open('nboutput.txt', 'w')
for root, subDir, files in os.walk(rootdir):
    for file in files:
        if 'txt' in file:
            fileCount += 1

            if 'spam' in root:
                totalSpam += 1
            elif 'ham' in root:
                totalHam +=1

            fileHandler = open(os.path.join(root, file), "r", encoding="latin1")
            type = classify(fileHandler, vocabulary, spam, ham)
            if type == 1:
                if 'spam' in root:
                    spamCount += 1
                else:
                    notSpamCount += 1
                outputFile.write("spam " + os.path.join(root, file)+"\n")
            elif type == 2:
                if 'ham' in root:
                    hamCount += 1
                else:
                    notHamCount += 1
                outputFile.write("ham " + os.path.join(root, file)+"\n")

outputFile.close()

#print (fileCount, spamCount, hamCount, notSpamCount, notHamCount)

sPrecision = (spamCount/(spamCount+notSpamCount))
hPrecision = (hamCount/(hamCount+notHamCount))
sRecall = (spamCount/totalSpam)
hRecall = (hamCount/totalHam)
sF1 = (2*sPrecision*sRecall)/(sPrecision+sRecall)
hF1 = (2*hPrecision*hRecall)/(hPrecision+hRecall)


print ("Spam Precision : ", sPrecision," Ham Precision : ", hPrecision)
print ("Spam Recall : ", sRecall," Ham Recall : ", hRecall)
print ("Spam F1 : ", sF1," Ham F1 : ", hF1)