import re, random
import itertools
from typing import List

word_len = 5
max_guesses = 0
auto_guess = True


def get_letter_dist(word_list):
    dist = {}
    for word in word_list:
        for letter in word:
            if letter in dist:
                dist[letter] += 1
            else:
                dist[letter] = 1
    return dist


def write_filtered(src_file):
    filtered = []
    pattern = re.compile(f"^([a-z]){'{' + str(word_len) + '}'}$")

    with open(src_file) as words:
        for w in words:
            w = w.strip()
            if re.match(pattern, w):
                filtered += [w]

    with open(f'filtered_{src_file}', 'w') as new_words:
        for w in filtered:
            new_words.write(w + '\n')


def do_guess(guess, target):
    if not len(guess) == len(target):
        raise ValueError("guess word length should equal target word length")

    ret = []
    for g, t in zip(guess, target):
        if g == t:
            ret += [g]
        elif g in target:
            ret += [1]
        else:
            ret += [0]
    return ret


def make_pattern(letters: List[set]):
    def pos_pattern(ltr_set):
        s = ''
        for a in ltr_set:
            s += a
        return s

    pattern_str = '^'
    for ltr_set in letters:
        pattern_str += f"([{pos_pattern(ltr_set)}])"
    pattern_str += '$'
    return re.compile(pattern_str)


def get_guess(last_guess, last_guess_result, words: list):
    if 'possible_letters' not in get_guess.__dict__:
        get_guess.possible_letters = set('abcdefghijklmnopqrstuvwxyz')
    if 'guessed_words' not in get_guess.__dict__:
        get_guess.guessed_words = set()
    if 'possible_words_set' not in get_guess.__dict__:
        get_guess.possible_words_set = set(words)

    letters = []
    for i, p in enumerate(last_guess_result):
        if isinstance(p, str):
            letters += [{p}]
        elif isinstance(p, int):
            if p == 0 and last_guess is not None and last_guess[i] in get_guess.possible_letters:
                get_guess.possible_letters.remove(last_guess[i])
            elif p == 1:
                pass
            letters += [get_guess.possible_letters]
        else:
            raise ValueError("Unexpected result type")

    pattern = make_pattern(letters)
    to_remove = set()
    for w in words:
        if w not in get_guess.possible_words_set:
            continue
        if re.match(pattern, w):
            if w in get_guess.guessed_words:
                continue
            else:
                get_guess.guessed_words.add(w)
                for r in to_remove:
                    get_guess.possible_words_set.remove(r)
                return w
        else:
            to_remove.add(w)
    return 'i give up'


if __name__ == '__main__':
    # write_filtered('words_freq.txt')
    with open('wordle_list.txt') as file:
        words = [w.strip() for w in file]
    print(sorted(get_letter_dist(words).items(), key=lambda x: x[1], reverse=True))
    for p in itertools.permutations('earotliu', 5):
        s = ''
        for i in p:
            s += i
        if s in words:
            print(s)
    # target = random.choice(words)
    # result = [0] * word_len
    # guess = None
    # num_guesses = 0
    # for _ in (range(max_guesses) if max_guesses > 0 else itertools.count()):
    #     if auto_guess:
    #         guess = get_guess(guess, result, words)
    #         print(guess)
    #     else:
    #         guess = input()
    #     if guess.lower() == 'i give up':
    #         print(target)
    #         break
    #     if len(guess) != word_len:
    #         print(f'guess must have {word_len} letters')
    #         continue
    #     if guess not in words:
    #         print(f'{guess} is not a valid word')
    #         continue
    #     result = do_guess(guess, target)
    #     num_guesses += 1
    #     for i in result:
    #         print('🟥' if i == 0 else '🟨' if i == 1 else '🟩', end='')
    #     if guess == target:
    #         print(f'\n{num_guesses=}')
    #         break
    #     print()
