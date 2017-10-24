import os
import sys
import numpy as np
import pandas as pd

if(len(sys.argv) < 5): 
	print("Error. Only following arguments")
	print(len(sys.argv))

train_file = sys.argv[1]
test_file = sys.argv[2]
locs_file = sys.argv[3]
ftypes = sys.argv[4:]

print(ftypes) 
