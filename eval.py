import os
import sys
import pandas as pd
import numpy as np

class Entity:
	def __init__(self):
		self.value = []
		self.type = []
		self.start = -1
		self.end = -1

ent_val = {"LOC": "LOCATION", "PER":"PERSON", "ORG":"ORGANIZATION"}

prediction_file = sys.argv[1]
gold_file = sys.argv[2]

prediction_data = pd.read_csv(prediction_file, sep = '\t', header = None).values.tolist()
gold_data = pd.read_csv(gold_file, sep = '\t', header = None).values.tolist()

prediction_data = np.array([x[0].split() for x in prediction_data])
gold_data = np.array([x[0].split() for x in gold_data])

en_start = -1
en_end = -1
en_type = []
en_values = []

entities = []

for i,x in enumerate(prediction_data):
	
	if en_start == -1:
		en_start = en_end = i
		en_type = x[0]
		en_values.append(x[1])
	elif "B-" in x[0] or "O" is x[0]:
		if "B-" in en_type or "I-" in en_type:
			ent = Entity()
			ent.value = en_values
			ent.type = ent_val[en_type[2:]]
			ent.start = en_start
			ent.end = en_end
			entities.append(ent)
			en_start = en_end = i
			en_type = x[0]
			en_values = []
			en_values.append(x[1])
	elif "I-" in x[0] and x[0][2:] == en_type[2:]:
		if "B-" in en_type or "I-" in en_type:
			en_values.append(x[1])
			en_end += 1


for x in entities:
	print(x.value, x.type, x.start+1, x.end+1)