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
	return pd.read_csv(locs_file, header = None)[0].tolist()

def load_data_from_file(train_file):
	sentences = []
	with open(train_file, 'r') as f:
		words = []
		for x in f.readlines():
			if(x.strip() == ""):
				if(len(words) > 0):
					sentence = Sentence(words)
					sentences.append(sentence)
					words = []
			else:
				word_arr = x.strip().split()
				word = Word(word_arr)
				words.append(word)
	return sentences
			
if(len(sys.argv) < 5): 
	print("Error. Only following arguments")
	print(len(sys.argv))
	sys.exit()

train_file = sys.argv[1]
test_file = sys.argv[2]
locs_file = sys.argv[3]
ftypes = sys.argv[4:]

locations = load_locations(locs_file)

train_data = load_data_from_file(train_file)

count = 5

for x in train_data:
	for y in x.words:
		print(y.label, y.pos, y.w)
	print("New Sent")
	count -= 1
	if(count == 0):
		sys.exit()