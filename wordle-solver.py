import random
import sys

bestwords = []
words = []
badletters = []
positionsknown = []
contained = []
previousguesses = []
badposletter = []

verbose = False
quiet = False

def getGuess(lastguess,answer):
    # evaluate our last guess
    pos = 0
    for letter in lastguess:
        answerLetter = answer[pos]
        if (answerLetter == letter):
            #this is an exact match letter, note that we now know this letter
            if (pos not in positionsknown):
                positionsknown.append(pos)
        elif (letter in answer):
            # this is an inexact match letter, so just note it is somewhere in the word
            if (letter not in contained):
                contained.append(letter)
                # but it isn't in this position
                key = letter+"-"+str(pos)
                if (key not in badposletter):
                    badposletter.append(key)
        else:
            # this letter isn't right at all, note that it is bad
            if (letter not in badletters):
                badletters.append(letter)
        pos = pos + 1

    if (verbose):
        print("I know these positions: "+str(positionsknown))
        print("I know these letters were bad"+str(badletters))
        print("I know I need these letters: "+str(contained))

    for word in words:
        if word in previousguesses:
            continue
        pos = 0
        matches = True
        for letter in word:
            key = letter+"-"+str(pos)
            if (key in badposletter):
                matches=False
            answerLetter = answer[pos]
            if (pos in positionsknown):
                # if we know this letter, is it the right letter?
                if (answerLetter != letter):
                    matches = False
            elif (letter in badletters):
                matches = False
            pos = pos + 1
        for checkletter in contained:
            if (checkletter not in word):
                # we know we need a letter and we don't have it
                matches = False
        if matches:
            return word 
    # sadly return our old guess because we have no idea        
    print("FAILURE to find something")
    print("I knew these positions: "+str(positionsknown))
    print("I knew these letters were bad"+str(badletters))
    print("I knew these words were wrong"+str(previousguesses))
    quit()

def solve(answer):

    badletters.clear()
    positionsknown.clear()
    contained.clear()
    previousguesses.clear()
    badposletter.clear()
    goes = 0
       
    guess = ""
    lastguess = ""
    while (guess != answer):
        guess = getGuess(lastguess,answer)
        if (not quiet):
            print("Guessing "+guess) 
        lastguess = guess
        previousguesses.append(lastguess)
        goes = goes + 1 

    if (not quiet):
        print("Found the answer in "+str(goes)+ " tries.")
    return goes


with open("bestwords.csv") as file:
    wordtemp = file.readlines()
    counter = 0
    for wordline in wordtemp:
        counter = counter + 1
        (word,temp) = wordline.split(",")
        word = word.rstrip()
        word = word.lower()
        bestwords.append(word)

if (len(sys.argv) == 1):
    search = random.choice(bestwords)
else:
    search = sys.argv[1].strip()

searchlist = []
if (search == "ALL"):
    for word in bestwords:
        searchlist.append(word)
    random.shuffle(searchlist)
    quiet = True
else:
    searchlist.append(search)

output = []

for answer in searchlist:
    if (not quiet):
        print("Searching for "+answer)

    if (not quiet):
        print("Using bestwords")
    words.clear()
    for word in bestwords:
        words.append(word)
    bestwordresult = solve(answer);

    if (not quiet):
        print("Using randomwords")
    count = 1
    sum = 0.0
    if (len(searchlist)>1):
        count = 5
    for i in range(count):
        words.clear()
        for word in bestwords:
            words.insert(0,word)
        random.shuffle(words)
        sum = sum + solve(answer)
    randomwordresult = sum / count 
        

    if (not quiet):
        print("Using most vowels then random")
    count = 1
    sum = 0.0
    if (len(searchlist)>1):
        count = 5
    for i in range(count):
        words.clear()
        for word in bestwords:
            words.insert(0,word)
        random.shuffle(words)
        words.insert(0,'audio')
        sum = sum + solve(answer)
    vowelrandomresult = sum / count

    if (not quiet):
        print("Using most vowels then best word")
    words.clear()
    for word in bestwords:
        words.append(word)
    words.insert(0,'audio')
    vowelbestwordresult = solve(answer)

    outstr = answer+","+str(bestwordresult)+","+str(randomwordresult)+","+str(vowelrandomresult)+","+str(vowelbestwordresult)
    print(outstr)
    output.append(outstr)


with open("experiments.csv","w") as file:
    file.write("Word,BestWordListResult,RandomWordListResult,AUDIOThenRandomWordsResult,AUDIOThenBestWordsResult\n")
    for outstr in output:
        file.write(outstr+"\n")
    file.close()
