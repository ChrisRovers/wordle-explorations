# wordle-explorations

I've been enjoying (like half the internet), the word game WORDLE - https://www.powerlanguage.co.uk/wordle/

I decided to play with some ideas.

The first is a best/worst guess word list creator, which tries to produce a word list that is ordered by how likely a word is to match arbitrary other words.

The second is a wordle solver - given a word, it tries to guess the word using wordle rules (it'd be possible to write a cheater for the online game with this, but I have not done so)

I intend to do some testing, using a random word list and a list sorted by "best" score, to see which allows the solver to solve the most words - it might be that given a list of all words in the world, having a good starting word just isn't important.

The dictionary I used was the TWL06 list

