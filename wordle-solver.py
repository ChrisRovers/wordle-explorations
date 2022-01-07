import random
import sys

words = []
badletters = []
positionsknown = []
contained = []
previousguesses = []
badposletter = []

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

#with open("bestwords.csv") as file:
with open("randomwords.csv") as file:
    wordtemp = file.readlines()
    counter = 0
    for wordline in wordtemp:
        counter = counter + 1
        #if (counter > 500):
        #    break
        (word,temp) = wordline.split(",")
        word = word.rstrip()
        word = word.lower()
        words.append(word)


if (len(sys.argv) == 1):
    answer = random.choice(words)
else:
    answer = sys.argv[1].strip()

print("It will be hunting "+answer)

goes = 0
   
guess = ""
lastguess = ""
while (guess != answer):
    guess = getGuess(lastguess,answer)
    print("Guessing "+guess) 
    lastguess = guess
    previousguesses.append(lastguess)
    goes = goes + 1 

print("Found the answer in "+str(goes)+ " tries.")
