import argh
from argh import arg
import requests
import re
import string
from itertools import combinations

dictionary_url = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"

NONALPHANUMERIC = re.compile(r'[\W_]+')

class Words:
  def __init__(self, dictionary_url=dictionary_url):
    """Utility class for word puzzles."""
    self.words = []
    self.graph = {}
    self.dictionary_url = dictionary_url

  def load_words(self):
    """Loads a newline separated word list from a url."""
    r = requests.get(self.dictionary_url)
    if r.status_code == 200:
      self.words = r.text.split()
    return self.words

  def preprocess_dict(self):
    """Loads the word list into a map with sorted letters as the keys."""
    for word in self.words:
      unfiltered = "".join(sorted(word))
      s = remove_nonalphanumeric(unfiltered)
      if s in self.graph:
        self.graph[s].append(word)
      else:
        self.graph[s] = [word]
    return self.graph

  def decompose(self, word):
    """Returns all words that can be made from letters in word."""
    response = set()
    tested = set() # eliminate redundant tests when duplicate letters exist
    sorted_word = remove_nonalphanumeric("".join(sorted(word)))
    for i in range(1, len(sorted_word)):
      combos = combinations(sorted_word, i)
      for comb in combos:
        test = "".join(comb)
        if test not in tested:
          tested.update(test)
          if test in self.graph:
            response.update(self.graph[test])
    return response

def remove_nonalphanumeric(word):
  """Remove nonalphanumeric characters from word"""
  return NONALPHANUMERIC.sub('', word)

def decompose(word):
  """Returns all words that can be made from letters in word."""
  words = Words()
  words.load_words()
  words.preprocess_dict()
  response = words.decompose(word)
  for elem in sorted(response):
    print(elem)

if __name__ == '__main__':
  parser = argh.ArghParser()
  parser.add_commands([decompose])
  parser.dispatch()
