"""Typing test implementation"""

from utils import (
    lower,
    split,
    remove_punctuation,
    lines_from_file,
    count,
    deep_convert_to_tuple,
)
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which the SELECT returns True.
    If there are fewer than K such paragraphs, return an empty string.

    Arguments:
        paragraphs: a list of strings representing paragraphs
        select: a function that returns True for paragraphs that meet its criteria
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    i = -1
    for paragraph in paragraphs:
        if select(paragraph):
            i += 1
            if i == k:
                return paragraph
    return ''
            
    # END PROBLEM 1


def about(subject):
    """Return a function that takes in a paragraph and returns whether
    that paragraph contains one of the words in SUBJECT.

    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), "subjects should be lowercase."

    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def fn(paragraph):
        s = remove_punctuation(paragraph)
        words = split(lower(s))

        for word in words:
            for sub in subject:
                if word == sub:
                    return True
        return False

    return fn
    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    compared to the corresponding words in SOURCE.

    Arguments:
        typed: a string that may contain typos
        source: a model string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    typed = typed.replace('\t', '') # 删除 \t
    typed_words = split(typed)
    source_words = split(source)

    typed = len(typed_words)
    matched = 0

    for i in range(min(len(typed_words), len(source_words))):
        if typed_words[i] == source_words[i]:
            matched += 1

    if len(typed_words) == 0 and len(source_words) == 0: # accuracy('', '') 100.0
        return float(100)
    if typed == 0 or matched == 0:
        return float(0)

    return float((matched/typed) * 100)
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, "Elapsed time must be positive"
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    word_length = 5
    words = len(typed) / word_length
    return float((words / elapsed) * 60)
    # END PROBLEM 4


################
# Phase 4 (EC) #
################


def memo(f):
    """A general memoization decorator."""
    cache = {}

    def memoized(*args):
        immutable_args = deep_convert_to_tuple(args)  # convert *args into a tuple representation
        if immutable_args not in cache:
            result = f(*immutable_args)
            cache[immutable_args] = result
            return result
        return cache[immutable_args]

    return memoized


def memo_diff(diff_function):
    """A memoization function."""
    cache = {}

    def memoized(typed, source, limit):
        # BEGIN PROBLEM EC
        "*** YOUR CODE HERE ***"
        immutable_args = (typed, source)
        
        if immutable_args in cache and cache[immutable_args][1] >= limit:
            return cache[immutable_args][0]

        result = diff_function(typed, source, limit)
        cache[immutable_args] = (result, limit)
        return result
        # END PROBLEM EC

    return memoized


###########
# Phase 2 #
###########

@memo
def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD based on DIFF_FUNCTION. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, return TYPED_WORD instead.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    """
    记录最小 diff min_diff 和最小 diff 的下标 min_idx，循环 word_list
    初始条件：min_dix = -1
    循环：if diff > limit continue，else if min_idx == -1 or diff < min_diff update min
    例外：typed_word == word_list[i]
    """
    min_idx = -1
    min_diff = 0

    for i in range(len(word_list)):
        # 例外
        if typed_word == word_list[i]:
            return typed_word

        diff = diff_function(typed_word, word_list[i], limit)
        if diff > limit:
            continue
        elif min_idx == -1 or diff < min_diff:
            min_idx = i
            min_diff = diff
    if min_idx == -1:
        return typed_word

    return word_list[min_idx]        
    # END PROBLEM 5


def furry_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> furry_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> furry_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> furry_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> furry_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> furry_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    """
    使用递归计算差异值
    1. 按字母计算
    2. 最终差值 + 长度差异
    3. 当差异达到 limit 时，直接返回差异值
    递归实现
    1. f(word, source, limit) = word[0] != source[0] + f(word[1:], source[1:], limit?)
    特殊条件
    当 word 和 source 均为空，返回 0
    当 word 或 source 为空时，返回 abs(len)
    当 limit 为 -1 时，返回 1，这个含义是已经出现最大修正了，当再次出现错误时，直接返回
    """
    if len(typed) == 0 and len(source) == 0:
        return 0
    if len(typed) == 0 or len(source) == 0:
        return abs(len(typed) - len(source))
    if limit == -1:
        return 1

    fix = 1 if typed[0] != source[0] else 0
    return fix + furry_fixes(typed[1:], source[1:], limit - fix)
    # END PROBLEM 6

@memo_diff
def minimum_mewtations(typed, source, limit):
    """A diff function for autocorrect that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """

    """
    if typed[0] == source[0]，无需修改，f = f(typed[1:], source[1:], limit)
    
    f = 1 + f(typed[1:], source[1:], limit) # subsitute
    f = 1 + f(typed[0:], source[1:], limit) # add
    f = 1 + f(typed[1:], source[0:], limit) # remove

    if len(typed) == len(source) == 0; return 0
    if len(typed) == 0 or len(typed) == 0; return abs(len-len);
    if limit == -1; return 1
    """
    
    # base case
    # 这个逻辑被下边的逻辑包含
    #if len(typed) == 0 and len(source) == 0:
    #    return 0
    if typed == source:
        return 0
    if len(typed) == 0 or len(source) == 0:
        return abs(len(typed) - len(source))
    # 优化，当长度相差过大时，直接返回 limit + 1
    if abs(len(typed) - len(source)) > limit:
        return limit + 1
    if limit == 0:
        return 1 

    # recursive
    if typed[0] == source[0]:
        return minimum_mewtations(typed[1:], source[1:], limit)
    elif limit == 0: # 优化，当 limit 为 0 时，表示不可修改
        return 1
    else:
        add = minimum_mewtations(typed, source[1:], limit - 1)
        if add == 0: # 优化，如果增加一个之后修复成功，不再尝试其他方法
            return 1
        remove = minimum_mewtations(typed[1:], source, limit - 1)
        if remove == 0: # 优化，如果删除一个之后修复成功，不再尝试其他方法
            return 1
        substitute = minimum_mewtations(typed[1:], source[1:], limit - 1)
    return 1 + min(add, remove, substitute)


# Ignore the line below
minimum_mewtations = count(minimum_mewtations)


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, "Remove this line to use your final_diff function."


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    matched = 0
    for word in source:
        if matched < len(typed) and typed[matched] == word:
            matched += 1
        else:
            break
    progress = float(matched / len(source))
    upload({"id": user_id, "progress": progress})
    return progress
    # END PROBLEM 8


def time_per_word(words, timestamps_per_player):
    """Return two values: the list of words that the players are typing and
    a list of lists that stores the durations it took each player to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        TIMESTAMPS_PER_PLAYER: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.


    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> words, times = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> words
    ['collar', 'plush', 'blush', 'repute']
    >>> times
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    def fn(ts):
            if len(ts) <= 1:
                return []
            return [ts[1] - ts[0]] + fn(ts[1:])
    times = []
    for ts in timestamps_per_player:
            times += [fn(ts)]
    return words, times
    # END PROBLEM 9


def time_per_word_match(words, timestamps_per_player):
    """Return a match object containing the words typed and the time it took each player to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match_object = time_per_word_match(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_all_words(match_object)    # Notice how we now use the selector functions to access the data
    ['collar', 'plush', 'blush', 'repute']
    >>> get_all_times(match_object)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    words, times = time_per_word(words, timestamps_per_player)
    return match(words, times)
    # END PROBLEM 10


def fastest_words(match_object):
    """Return a list of lists indicating which words each player typed the fastest.

    Arguments:
        match_object: a match data abstraction created by the match constructor

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(get_all_times(match_object)))  # contains an *index* for each player
    word_indices = range(len(get_all_words(match_object)))  # contains an *index* for each word
    # BEGIN PROBLEM 11
    "*** YOUR CODE HERE ***"
    words = get_all_words(match_object)
    times = get_all_times(match_object)

    fwords = []
    for i in range(len(times)):
        fwords += [[]]

    for wi in range(len(words)):
        fastest = 0
        for ti in range(len(times)):
           print('DEBUG: wi: %d, ti: %d' % (wi, ti))
           if get_time(match_object, fastest, wi) > get_time(match_object, ti, wi):
               fastest = ti
        fwords[fastest] += [words[wi]]

    return fwords
    # END PROBLEM 11


def match(words, times):
    """Creates a data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), "words should be a list of strings"
    assert all([type(t) == list for t in times]), "times should be a list of lists"
    assert all([isinstance(i, (int, float)) for t in times for i in t]), "times lists should contain numbers"
    assert all([len(t) == len(words) for t in times]), "There should be one word per time."
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert (0 <= word_index < len(get_all_words(match))), "word_index out of range of words"
    return get_all_words(match)[word_index]


def get_time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(get_all_words(match)), "word_index out of range of words"
    assert player_num < len(get_all_times(match)), "player_num out of range of players"
    return get_all_times(match)[player_num][word_index]


def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]


def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match data abstraction and returns a string representation of it"""
    return f"match({get_all_words(match)}, {get_all_times(match)})"


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file("data/sample_paragraphs.txt")
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print("No more paragraphs about", topics, "are available.")
            return
        print("Type the following paragraph and then press enter/return.")
        print("If you only type part of it, you will be scored only on that part.\n")
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print("Goodbye.")
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print("Words per minute:", wpm(typed, elapsed))
        print("Accuracy:        ", accuracy(typed, source))

        print("\nPress enter/return for the next paragraph or type q to quit.")
        if input().strip() == "q":
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse

    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument("topic", help="Topic word", nargs="*")
    parser.add_argument("-t", help="Run typing test", action="store_true")

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
