import os
import sys

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

# read files and classify
outputFile = open('nboutput.txt', 'w')
for root, subDir, files in os.walk(rootdir):
    for file in files:
        if 'txt' in file:
            fileHandler = open(os.path.join(root, file), "r", encoding="latin1")
            type = classify(fileHandler, vocabulary, spam, ham)
            if type == 1:
                outputFile.write("spam " + os.path.join(root, file)+"\n")
            elif type == 2:
                outputFile.write("ham " + os.path.join(root, file)+"\n")

outputFile.close()
