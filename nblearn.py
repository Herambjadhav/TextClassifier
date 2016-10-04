import os
import sys
import math

def updateVocabulary(emailType, fileHandler):
    lines = fileHandler.readlines()
    wordList = []
    for line in lines:
        for word in line.split():
            wordList.append(word)
    if emailType == 1:
        for word in wordList:
            if word in vocabulary:
                counts = vocabulary[word]
                if 'spam' in counts:
                    counts['spam'] = counts['spam'] + 1
                else:
                    counts['spam'] = 1
            else:
                counts = {}
                counts['spam'] = 1
                vocabulary[word] = counts
    else:
        for word in wordList:
            if word in vocabulary:
                counts = vocabulary[word]
                if 'ham' in counts:
                    counts['ham'] = counts['ham'] + 1
                else:
                    counts['ham'] = 1
            else:
                counts = {}
                counts['ham'] = 1
                vocabulary[word] = counts
    fileHandler.close()
    return len(wordList)

print ('Argument count : ', len(sys.argv))
#exit if file name is not provided as command line argument
if len(sys.argv) != 2:
    print ('Please send file name as command line argument')
    exit(0)

rootdir = sys.argv[1]
print ('Root Dir : ', rootdir)

vocabulary = {}
spamCount = 0
hamCount = 0
spamWords = 0
hamWords = 0

for root, subDir, files in os.walk(rootdir):
    for file in files:
        fileHandler = open(os.path.join(root, file), "r", encoding="latin1")
        # spam emails
        if 'spam' in root:
            spamCount += 1
            spamWords += updateVocabulary(1, fileHandler);
        # ham emails
        if 'ham' in root:
            hamCount += 1
            hamWords += updateVocabulary(2, fileHandler);

print (spamCount, hamCount, spamWords, hamWords)
print (len(vocabulary))

# Calculate Probabilities of each word
fileHandler = open('nbmodel.txt', 'w', encoding="latin1")
print("%g %g" %(spamCount/(spamCount+hamCount), math.log(spamCount/(spamCount+hamCount))), file = fileHandler)
print("%g %g" %(hamCount/(spamCount+hamCount), math.log(hamCount/(spamCount+hamCount))), file = fileHandler)
print("%s" %(len(vocabulary)), file = fileHandler)

for word in vocabulary:
    counts = vocabulary[word]
    if 'spam' in counts:
        frequency = counts['spam']
        counts['SP'] = (frequency + 1) / (spamWords + len(vocabulary))
    else:
        counts['SP'] = 1 / (spamWords + len(vocabulary))
    if 'ham' in counts:
        frequency = counts['ham']
        counts['HP'] = (frequency + 1) / (hamWords + len(vocabulary))
    else:
        counts['HP'] = 1 / (hamWords + len(vocabulary))

    #write to file
    print("%s %g %g %g %g" % (word, counts['SP'], math.log(counts['SP']), counts['HP'], math.log(counts['HP'])),file = fileHandler)

fileHandler.close()






