import os
import sys
import numpy as np
import pandas as pd

word_list = []
pos_list = []

class Word:
	def __init__(self, word_arr):
		self.label = word_arr[0]
		self.pos = word_arr[1]
		self.w = word_arr[2]

class Sentence:
	def __init__(self, words):
		self.words = words

unknown = Word(["","UNKPOS","UNK"])

class Output:
	def __init__(self, word, word_pos, sentence, ftypes):
		self.word = word.w
		self.abbr = "no"	
		self.pos = word.pos
		
		w_prev = w_next = unknown.w
		pos_prev = pos_next = unknown.pos
		
		if sentence.words[word_pos - 1].w in word_list:
			w_prev = sentence.words[word_pos - 1].w
		if sentence.words[word_pos + 1].w in word_list:
			w_next = sentence.words[word_pos + 1].w

		if sentence.words[word_pos - 1].pos in word_list:
			pos_prev = sentence.words[word_pos - 1].pos
		if sentence.words[word_pos + 1].pos in word_list:
			pos_next = sentence.words[word_pos + 1].pos

		self.poscon = " ".join([pos_prev, pos_next])
		self.wordcon = " ".join([w_prev, w_next])


		if(len(self.word) < 5 and self.word[-1] == '.' and self.word.replace('.','').isalpha()):
			self.abbr = "yes"
		
		self.cap = "no"
		if(self.word[0].isupper()):
			self.cap = "yes"

		self.loc = "no"
		if(self.word in locations):
			self.loc = "yes"

		if "wordcon" not in ftypes:
			self.wordcon = "n/a"
		if "pos" not in ftypes:
			self.pos = "n/a"
		if "poscon" not in ftypes:
			self.poscon = "n/a"
		if "abbr" not in ftypes:
			self.abbr = "n/a"
		if "cap" not in ftypes:
			self.cap = "n/a"
		if "location" not in ftypes:
			self.loc = "n/a"

	def print_o(self):
		print(self.word, self.wordcon, self.pos, self.poscon, self.abbr, self.cap, self.loc)

def process_outputs(data, ftypes):
	outputs_readable = []
	for sent in data:
		for i,word in enumerate(sent.words):
			output = Output(word, i, sent, ftypes)
			output.print_o()


def load_locations(locs_file):
	return pd.read_csv(locs_file, header = None)[0].tolist()

def load_data_from_file(train_file, train_flag = True):
	sentences = []
	all_words = []
	with open(train_file, 'r') as f:
		w = Word(["","PHIPOS","PHI"])
		words = []
		words.append(w)
		for x in f.readlines():
			if(x.strip() == ""):
				if(len(words) > 0):
					w = Word(["","OMEGAPOS","OMEGA"])
					words.append(w)
					sentence = Sentence(words)
					sentences.append(sentence)
					w = Word(["","PHIPOS","PHI"])
					words = []
					words.append(w)
			else:
				word_arr = x.strip().split()
				word = Word(word_arr)
				words.append(word)
				if train_flag:
					word_list.append(word.w)
					pos_list.append(word.pos)
	return sentences

if(len(sys.argv) < 5): 
	print("Error. Only following arguments")
	print(len(sys.argv))
	sys.exit()

train_file = sys.argv[1]
test_file = sys.argv[2]
locs_file = sys.argv[3]
ftypes = [x.lower() for x in sys.argv[4:]]

locations = load_locations(locs_file)
test_data = load_data_from_file(test_file, False)
train_data = load_data_from_file(train_file)

process_outputs(train_data, ftypes)