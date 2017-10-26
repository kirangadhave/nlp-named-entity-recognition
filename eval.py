#!/usr/bin/env python3.6
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

	def isEqual(self, entity):
		if self.type == entity.type and self.start == entity.start and self.end == entity.end:
			return True
		return False

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
	elif "B-" in x[0] or 'O' == x[0]:
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
		elif "B-" in x[0]:
			en_start = en_end = i
			en_type = x[0]
			en_values = []
			en_values.append(x[1])
	elif "I-" in x[0] and x[0][2:] == en_type[2:]:
		if "B-" in en_type or "I-" in en_type:
			en_values.append(x[1])
			en_end += 1

predictions = entities
entities = []

for i,x in enumerate(gold_data):
	if en_start == -1:
		en_start = en_end = i
		en_type = x[0]
		en_values.append(x[1])
	elif "B-" in x[0] or 'O' == x[0]:
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
		elif "B-" in x[0]:
			en_start = en_end = i
			en_type = x[0]
			en_values = []
			en_values.append(x[1])
	elif "I-" in x[0] and x[0][2:] == en_type[2:]:
		if "B-" in en_type or "I-" in en_type:
			en_values.append(x[1])
			en_end += 1

gold = entities

per_corr = 0
loc_corr = 0
org_corr = 0
total_corr = 0

per_arr = []
loc_arr = []
org_arr = []

for x in predictions:
	for y in gold:
		if x.isEqual(y):
			total_corr += 1
			if x.type == "PERSON":
				per_corr += 1
				per_arr.append(x)
			if x.type == "LOCATION":
				loc_corr += 1
				loc_arr.append(x)
			if x.type == "ORGANIZATION":
				org_corr += 1
				org_arr.append(x)

output = []

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
if len(per_arr) > 0:
	per = []
	for x in per_arr:
		per.append(" ".join(x.value) + "[" + str(x.start +1 ) + "-" + str(x.end +1) + "]")
	output.append("Correct PER = " + " | ".join(per))
else:
	output.append("Correct PER = " + "NONE")

per_pred = len([x for x in predictions if x.type == "PERSON"])
per_gold = len([x for x in gold if x.type == "PERSON"])

if per_gold == 0:
	output.append("Recall PER = " + "n/a")
else:
	output.append("Recall PER = " + str(per_corr) + "/" + str(per_gold))


if per_pred == 0:
	output.append("Precision PER = " + "n/a")
else:
	output.append("Precision PER = " + str(per_corr) + "/" + str(per_pred))

output.append("")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
if len(loc_arr) > 0:
	loc = []
	for x in loc_arr:
		loc.append(" ".join(x.value) + "[" + str(x.start + 1) + "-" + str(x.end + 1) + "]")
	output.append("Correct LOC = " + " | ".join(loc))
else:
	output.append("NONE")

loc_pred = len([x for x in predictions if x.type == "LOCATION"])
loc_gold = len([x for x in gold if x.type == "LOCATION"])

if loc_gold == 0:
	output.append("Recall LOC = " + "n/a")
else:
	output.append("Recall LOC = " + str(loc_corr) + "/" + str(loc_gold))

if loc_pred == 0:
	output.append("Precision LOC = " + "n/a")
else:
	output.append("Precision LOC = " + str(loc_corr) + "/" + str(loc_pred))


output.append("")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
if len(org_arr) > 0:
	org = []
	for x in org_arr:
		org.append(" ".join(x.value) + "[" + str(x.start + 1) + "-" + str(x.end + 1) + "]")
	output.append("Correct ORG = " + " | ".join(org))
else:
	output.append("Correct ORG = " + "NONE")

org_pred = len([x for x in predictions if x.type == "ORGANIZATION"])
org_gold = len([x for x in gold if x.type == "ORGANIZATION"])

if org_gold == 0:
	output.append("Recall ORG = " + "n/a")
else:
	output.append("Recall ORG = " + str(org_corr) + "/" + str(org_gold))

if org_pred == 0:
	output.append("Precision ORG = " + "n/a")
else:
	output.append("Precision ORG = " + str(org_corr) + "/" + str(org_pred))
 
output.append("")

output.append("Average Recall = " + str(org_corr + per_corr + loc_corr) + "/" + str(len(gold)))
output.append("Average Precision = " + str(org_corr + per_corr + loc_corr) + "/" + str(len(predictions)))

with open("eval.txt", "w") as f:
	for x in output:
		f.write(x)
		f.write("\n")