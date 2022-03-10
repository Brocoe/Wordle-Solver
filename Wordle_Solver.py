### Data ###
# word test: plume
from random import randint
dictionary = 'Dictionary.txt'
available_words = []
selected_word = ''
program_word = ''
user_word = ''
bad_letters = [' ']
good_letters = []
wordVals = {}
position_good_known = {0:'abcdefghijklmnopqrstuvwxyz',
                       1:'abcdefghijklmnopqrstuvwxyz',
                       2:'abcdefghijklmnopqrstuvwxyz',
                       3:'abcdefghijklmnopqrstuvwxyz',
                       4:'abcdefghijklmnopqrstuvwxyz'}
position_bad_known = {0:'',1:'',2:'',3:'',4:''}
userSelectedWord = ''
turn = 1
previous_word = ['--Previous Guesses--']
killSwitch = 0
### Processing ###
def letterCount(wordlst=[],badletters=[]):
    letterCount = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,
                   'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}
    for word in wordlst:
        for letter in set(word):
            letterCount[letter] += 1
    for key, value in letterCount.items():
        if key in badletters:
            letterCount[key] = 0
    return letterCount
def wordValue(availableWords=[],letterCount={}):
    '''
    Calculates a value of each word based on how often each letter appears in the list of
    available words.

    :param availableWords: a list of all the available words
    :param letterCount: a dictionary that's keys are letters in the alphabet and values that
    show how many times the letters appear in the remaining words.
    :return: a dictionary that returns a key, value pair of remaining words and their value.
    '''
    guessValue = {}
    for word in availableWords:
        wordVal = 0
        for letter in set(word):
            wordVal += letterCount[letter]
            guessValue[word] = wordVal
    return guessValue
def BasicLetters(word_list=[],badLetters=[],goodletters=[]):
    '''
    This is an elimination program.
    First, it looks at letters that have been eliminated and then removes words that have
    those letters.
    Second, it looks a letters that are known to be in the words (anything with a G or Y clue)
    and ensures that the words have all of those letters in them.

    :param word_list: list of words that have not been previously eliminated
    :param badLetters: list of letters that have been eliminated (marked with a 'B' in the clue)
    :param goodletters: list of letters that are known to be in the word (tagged 'Y' and 'G')
    :return: Returns a list of words that have none of the badletters and all the goodletters
    '''
    firstWords = []
    goodWords = []
    for word in word_list:
        bW = 0
        for letter in badLetters:
            if letter in word:
                bW += 1
        if bW == 0:
            firstWords.append(word)
    for word in firstWords:
        gW = 0
        for letter in goodletters:
            if letter in word:
                gW+=1
        if gW == len(goodletters):
            goodWords.append(word)
    return goodWords
def correctPositions(word_list=[],goodPos={},badPos={}):
    '''
    This function looks at know letter positions (letters that have been coloured in green) and
    letters of that have been colored in yellow. Yellow letters represent bad letter positions
    (i.e. letters that cannot go in that position)

    :param word_list: the current list of words that have not been eliminated.
    :param goodPos: a dictionary that shows the available letters for each position.
    :param badPos: a dictionary that shows the letter that are not available for each position
    (shows the letters that have gotten a yellow clue).
    :return:
    '''
    goodWords = []
    for word in word_list:
        clearcnt = 0
        for letter in word:
            if letter not in badPos[word.index(letter)] and letter in goodPos[word.index(letter)]:
                clearcnt +=1
            if clearcnt == 5:
                goodWords.append(word)
    return goodWords
def ClueSolver(puzzleWord='',guessWord=''):
    '''
    When a playing a game with the program this function automatically calculates the user clue
    using the BGY framework.

    :param puzzleWord: The word that was selected by the computer
    :param guessWord: The word that was guessed by the user
    :return: returns the BGY clue
    '''
    clue = ''
    pos = 0
    for letter in guessWord:
        if letter == puzzleWord[pos]:
            clue += 'G'
        elif letter in set(puzzleWord):
            clue += 'Y'
        else:
            clue += 'B'
        pos += 1
    clue.strip()
    return clue
def PreviousWords(previous_words=[],clue='',guess='',turn=0):
    '''
    This creates a list of the previous words that have been guessed and returns a colour coded
    listing of these words in a similar manner to the actual Wordle Game

    :param previous_words: previous words that have been guessed
    :param clue: either a user generated or computer generated code that colours letters black, green or yellow
    :param guess: The current word that was guessed to be appended to prvious_words
    :param turn: which turn the user is on
    :return: returns a list of colour formatted words.
    '''
    dict_color ={'G':'92','Y':'93','B':'37'}
    colorlst = []
    colorword = ''
    for a in range(0,5):
        colorlst.append("\033[1;"+dict_color[clue[a]]+";1m"+guess[a]+"\033[0m")
    for letter in colorlst:
        colorword += letter
    colorword = "Turn "+str(turn)+" --> "+colorword
    previous_words.append(colorword)
    return previous_words


### Input and output ###
objFile = open(dictionary,'r')
for row in objFile:
    available_words.append(row.strip())
while True:
    userSelectedWord = input("select word for training or type 'random' for a random word : ")
    userSelectedWord = userSelectedWord.lower()
    if userSelectedWord in available_words:
        break
    elif userSelectedWord == 'random':
        ran = randint(0,len(available_words))
        userSelectedWord = available_words[ran]
        break
    elif userSelectedWord == '':
        break
    else:
        print('That word is not in the Wordle dictionary.\n'
              'Please select another word.')
print("\n\nWelcome to the Wordle Solver. Type 'exit' at any time to end the program.\n"
      "When filling out move information using the following key\n\n"
      "B = black square (letter is not in the word)\n"
      "G = green square (the right letter in the right spot)\n"
      "Y = yellow square (thr right letter in the wrong spot)\n\n"
      "It looks like you haven't made a move yet.\n")
while True:
    helper = input("\nWould you like to use the helper (Yes or No)? ")
    helper = helper.lower()
    if helper == 'yes' or helper == 'no':
        break
    else:
        print('\nPlease select Yes or No.')
while True:
    wordVals = wordValue(available_words,letterCount(available_words,bad_letters))
    program_word = max(wordVals,key=wordVals.get)
    if helper == 'yes':
        if len(wordVals) == 1:
            print("\nThe word is: \033[1;96;1m{}\033[0m.\n".format(program_word))
            print("System word check \033[1;95;1m'{}'\033[0m.".format(userSelectedWord))
            print('The game is over.')
            break
        else:
            print("\nThe best move for turn {} based on the algorithm is: \033[1;96;1m'{}'\033[0m.\n".format(turn,program_word))
    while True:
        user_word = input("\nPlease choose a word or leave blank to use suggested word: ")
        user_word = user_word.lower()
        if user_word.lower() == 'exit':
            break
        elif user_word == '' and helper == 'yes':
            selected_word = program_word
            break
        elif len(user_word) == 5:
            selected_word = user_word
            break
        else:
            print("\nThat word is not 5 letters. Please try again.")
    if user_word.lower() == 'exit':
        break
    while True:
        if userSelectedWord == '':
            clue = input("\nWhat was your result? (remember to use B,G,Y): ")
        else:
            clue = ClueSolver(userSelectedWord,selected_word)
            print('\nYour result was {}'.format(clue))
        clue = clue.upper()
        a = 0
        for letter in clue:
            if letter in "BGY":
                a+=1
        if a==5:
            break
        else:
            print('\nYou entered the clue incorrectly. Please try again.')
    a = 0
    for letters in clue:
        if letters == 'B':
            bad_letters.append(selected_word[a])
        else:
            good_letters.append(selected_word[a])
        if letters == 'G':
            position_good_known[a] = selected_word[a]
        elif letters == 'Y':
            if position_bad_known[a] == '':
                position_bad_known[a] = selected_word[a]
            else:
                position_bad_known[a] += selected_word[a]
        a+=1
    # print(position_good_known)
    # print(position_bad_known)
    available_words = BasicLetters(available_words,bad_letters,good_letters)
    # print(available_words)
    available_words = correctPositions(available_words,position_good_known,position_bad_known)
    # print(available_words)
    previous_word = PreviousWords(previous_word,clue,selected_word,turn)
    for word in previous_word:
        print(word)
    turn += 1
    if turn == 7:
        print("\nThe word is: \033[1;96;1m{}\033[0m.\n".format(program_word))
        print("System word check \033[1;95;1m'{}'\033[0m.".format(userSelectedWord))
        print('The game is over.')
        break