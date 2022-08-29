import random
import time

# dictionary contains the unicodes for colored squares, used for telling
# the user if a letter is in the word and if it is in the correct space
squares = {
    "green" : "\U0001F7E9",
    "yellow" : "\U0001F7E8",
    "white" : "\U00002B1C",
    "black" : "\U00002B1B",
}

alphabet = "abcdefghijklmnopqrstuvwxyz"

restrict_guess_to_wordlist = False
darkmode = False

def wait():
    time.sleep(.7)


def wordlist_gen():
    with open('wordlist1.txt', 'r') as f:
        global wordlist
        wordlist = f.readlines()

        #for word in f.readlines():
        #    wordlist.append(word.strip())


def wordle_gen():

    # select the wordle at random from wordlist
    wordle = wordlist[random.randint(0, len(wordlist)-1)].strip()

    return wordle


def take_guess():
    while True:
        wait()
        guess = input("          Guess a five-letter word: ")
        if len(guess) != 5:
            print("          Your guess must be a five-letter word!")
        elif restrict_guess_to_wordlist == True:
            if guess not in wordlist:
                print("          Not in wordlist.  Try again!")
        else:
            break
    return guess


# put spaces in guess so it lines up with square emojis when presented to user
def format_guess(guess):
    output = ""
    for letter in guess:
        output += f"{letter} "
    output += "\n"
    return output


# returns a dictionary of all the letters of the alphabet that are marked as unknown
def alphabet_gen():
    output = {}
    for letter in alphabet:
        output[letter] = squares["white"]
    return output


def keyboard_gen():
    output = "          "
    for letter in alphabet:
        output += letter + " "
    output += "\n          "
    for letter in alphabet:
        output += used_letters[letter]
    return output


# generate feedback in the form of green, yellow, and black or white squares
def square_gen(wordle, guess):
    output = format_guess(guess)

    # create a memo that records occurrences of a letter this memo will allow the user to see the
    # correct number of yellow squares: for example, a guess "messy" for wordle "sauce" will
    # return a yellow square for the first 's' and a blank one for the second.
    m = {}

    for letter in guess:
        m[letter] = wordle.count(letter)

    i = -1
    for letter in guess:
        i += 1
        if letter == wordle[i]:
            output += squares["green"]
            used_letters[letter]  = squares["green"]
            m[letter] -= 1
        elif letter in wordle and m[letter] > 0:
            output += squares["yellow"]
            m[letter] -= 1
            if used_letters[letter] != squares["green"]:
                used_letters[letter]  = squares["yellow"]
        else:
            output += squares["black"]
            print(used_letters[letter])
            if used_letters[letter] == squares["white"]: 
                print('here')
                used_letters[letter]  = squares["black"]
    return output


def play_wordle(wordle):
    tries = 6
    global used_letters
    used_letters = alphabet_gen()
    while tries > 0:

        guess = take_guess()
        print("\n", square_gen(wordle, guess), "\n")
        print(keyboard_gen())

        if wordle == guess:
            print(f"          You win! The word was '{wordle}'.")
            break

        else:
            tries -= 1
            print(f"          You have {tries} guesses left!")
            time.sleep(.7)
            if tries == 0:
                print(f"          You lose! The word was '{wordle}'.")

wordlist_gen()
play_wordle(wordle_gen())
