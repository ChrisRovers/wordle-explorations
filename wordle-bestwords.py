from collections import defaultdict

words = []

def getScores(wordcheck):
    score = 0
    elimscore = 0
    for word in words:
        if word == wordcheck:
            continue
        lettercount = 0
        uniqueletters = []
        elimword = False
        for letter in wordcheck:
            # calc our orig scoring system
            if (letter == word[lettercount]):
                # we get 3 points for every letter than exactly matches another
                score = score + 3
            else:
                if letter not in uniqueletters:
                    # only get credit for the first of a given letter
                    uniqueletters.append(letter)
                    if letter in word:
                        # if our letter is in another word, we get a point
                        score = score + 1

            # calc our elim score - get 3 points for every word we eliminate
            if letter in word:
                elimword = True
            
            lettercount = lettercount + 1
        if elimword:
            elimscore = elimscore+3
    
    repeatCost = 1
    letterpos = 0
    for letter in wordcheck:
        if (wordcheck.count(letter) > 1):
            repeatCost = 2
    return ((score // repeatCost),elimscore)
                
             

with open("twl06.txt") as file:
    wordtemp = file.readlines()
    counter = 0
    for word in wordtemp:
        counter = counter + 1
        #if (counter > 500):
        #    break
        word = word.rstrip()
        word = word.lower()
        if (len(word) == 5):
            words.append(word)

scores = defaultdict(int)
elimscores = defaultdict(int)

print("Found "+str(len(words))+" 5 letter words.")


count = 0
percent = 0
per = len(words) // 100
for word in words:
    (score,elimscore) = getScores(word)
    print(word+" has "+str(score)+","+str(elimscore))
    scores[word] += score
    elimscores[word] += elimscore
    count = count + 1
    if (count == per):
        count = 0
        percent = percent + 1
        print(str(percent)+"%")

finalscores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)

print("Top 20 words")
for count in range(0,19):
    print(finalscores[count])
print("Bottom 20 words")
for count in range(len(finalscores)-20,len(finalscores)-1):
    print(finalscores[count])

with open("bestwords.csv","w") as file:
    for score in finalscores:
        file.write(score[0]+","+str(score[1])+"\n")
    file.close()

finalscores = sorted(elimscores.items(), key=lambda kv: kv[1], reverse=True)
with open("bestelimwords.csv","w") as file:
    for score in finalscores:
        file.write(score[0]+","+str(score[1])+"\n")
    file.close()
