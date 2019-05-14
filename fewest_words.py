from typing import Dict, List, Tuple

letters = ["s", "t", "r", "t", "n", "b", "k", "r"]
dictionary = ["start", "nob", "key", "ray", "see", "tartine", "bakery"]


# Assumptions:
#	y is a vowel
#	letters will only contain lowercase letters
# 	letters will not be empty, can add a check outside of function to check this

def process_words(words: List[str]) -> Dict[str, List[str]]:
	"""
	precompute a data structure that represents the words
	without vowels for easy lookup. This could be optimized
	to a trie or something for larger data sets, but a dict
	should be sufficient for this simple example

	for simplicty, and based on the example, 'y' is considered a vowel
	but this could be tweaked in a more complex processing.
	"""
	processed = {}
	vowels = 'aeiouy'
	for word in words:
		stripped = ''.join([char for char in word if char not in vowels])
		processed[stripped] = processed.get(stripped, []) + [word]
	return processed

words_dict = process_words(dictionary)

assert process_words(dictionary) == {
	'strt': ['start'], 
	'nb': ['nob'], 
	'k': ['key'], 
	'r':['ray'], 
	's': ['see'], 
	'trtn': ['tartine'],
	'bkr': ['bakery']}


def split_words_recursive(letters: List[str], words: Dict[str, List[str]]) -> Tuple[str]:
	"""this should be memoized for best performance, otherwise it will be slow"""
	
	# base case, there are no results in an empty list
	if not letters:
		return []

	# pick out the max word length in the dictionary, this is an optimization
	# that could potentially be skipped depending on the use case
	max_length = max([len(key) for key in words.keys()])

	# store results of recursive calls
	results = []
	# pick letters off the front of the letters, potentially limited by max word length
	test_word = ''
	# if you don't want to calculate max length, iterate over the entire letters lest
	for idx, char in enumerate(letters[:max_length]):
		test_word += char
		# only make recursive calls if the current set of letters can potentially make a word
		if test_word in words:
			# find fewest words in the rest of the list of letters:
			res = split_words_recursive(letters[idx+1:], words)
			# res could be None, which means we failed to find anything in the recursive call
			# so only include results that aren't None
			if res is not None:
				results.append(([test_word] + res))

	# if there are no results, we failed to find a word, so return None
	if not results:
		return None

	# return the result with the fewest words
	return min(results, key=len)

assert split_words_recursive('b', {'b': ['be']}) == ['b']
assert split_words_recursive('bd', {'b': ['be'], 'd': ['do'], 'bd': ['bad']}) == ['bd']
assert split_words_recursive(letters, words_dict) == ['s', 'trtn', 'bkr']
assert split_words_recursive(['q', 'z', 'x'], words_dict) == None

def inflate_words(res, words_dict):
	return [words_dict[word][0] for word in res]

assert inflate_words(('s', 'trtn', 'bkr'), words_dict) == ['see', 'tartine', 'bakery']





