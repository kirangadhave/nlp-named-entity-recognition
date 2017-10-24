import os
import sys
import numpy as np
import pandas as pd

class Word:
	def __init__(self, word_arr):
		self.label = word_arr[0]
		self.pos = word_arr[1]
		self.w = word_arr[2]

class Sentence:
	def __init__(self, words):
		self.words = words

def load_locations(locs_file):
	return pd.read_csv(locs_file, header = None)

if(len(sys.argv) < 5): 
	print("Error. Only following arguments")
	print(len(sys.argv))
	sys.exit()

train_file = sys.argv[1]
test_file = sys.argv[2]
locs_file = sys.argv[3]
ftypes = sys.argv[4:]

locations = load_locations(locs_file)[0].tolist()

