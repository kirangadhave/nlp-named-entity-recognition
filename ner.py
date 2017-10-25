import os
import sys
import numpy as np
import pandas as pd

word_list = ["PHI", "OMEGA"]
pos_list = ["PHIPOS", "OMEGAPOS"]

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
		self.abbr = "no"	
		self.word = word.w
		self.pos = unknown.pos
		if word.pos in pos_list:
			self.pos = word.pos
		
		w_prev = w_next = unknown.w
		pos_prev = pos_next = unknown.pos
		
		if sentence.words[word_pos - 1].w in word_list:
			w_prev = sentence.words[word_pos - 1].w
		if sentence.words[word_pos + 1].w in word_list:
			w_next = sentence.words[word_pos + 1].w

		if sentence.words[word_pos - 1].pos in pos_list:
			pos_prev = sentence.words[word_pos - 1].pos
		if sentence.words[word_pos + 1].pos in pos_list:
			pos_next = sentence.words[word_pos + 1].pos

		self.poscon = " ".join([pos_prev, pos_next])
		self.wordcon = " ".join([w_prev, w_next])

		if( self.word[-1] == '.' and len(self.word) < 5 and (self.word.replace('.','').isalpha() or self.word.replace('.','') == "")):
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

		if word.w not in word_list:
			self.word = unknown.w


	def print_o(self):
		to_print = []
		to_print.append(" ".join(["WORD:", self.word]))
		to_print.append(" ".join(["WORDCON:", self.wordcon]))
		to_print.append(" ".join(["POS:", self.pos]))
		to_print.append(" ".join(["POSCON:", self.poscon]))
		to_print.append(" ".join(["ABBR:", self.abbr]))
		to_print.append(" ".join(["CAP:", self.cap]))
		to_print.append(" ".join(["LOCATION:", self.loc]))
		to_print.append("")
		return to_print

def process_outputs(data, ftypes):
	outputs_readable = []
	for sent in data:
		for i,word in enumerate(sent.words):
			if i != 0 and i != (len(sent.words) - 1):
				output = Output(word, i, sent, ftypes)
				outputs_readable.append(output)	
	return outputs_readable

def load_locations(locs_file):
	return pd.read_csv(locs_file, header = None)[0].tolist()

def load_data_from_file(train_file, train_flag = True):
	sentences = []
	all_words = []
	with open(train_file, 'r') as f:
		w = Word(["","PHIPOS","PHI"])
		words = []
		words.append(w)

		lines = f.readlines()
		lines.append(" ")
		for x in lines:
			if(x.strip() == ""):
				if(len(words) > 1):
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

train_readable = process_outputs(train_data, ftypes)
test_readable = process_outputs(test_data, ftypes)


with open("train.txt.readable", 'w') as f:
	for x in train_readable:
		for y in x.print_o():
			f.write(y)
			f.write('\n')

with open("test.txt.readable", 'w') as f:
	for x in test_readable:
		for y in x.print_o():
			f.write(y)
			f.write('\n')
