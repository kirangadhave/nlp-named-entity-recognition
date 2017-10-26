a)  Programming language used: Python
    Version: Python3.6

b)  Instructions for running:
    1. cd into the programming-assignment-3 directory.

    2. Type - "python3.6 ner.py <train_file> <test_file> <loc_file> WORD [< optional ftypes >]" to run "ner" program.

    3. Type - "python3.6 eval.py <prediction_file> <gold_file>" to run "eval" program. Output is printed in eval.txt file.

c) Could not test the machine learning part on CADE machine lab1-1 due to error machine learning library. Tested and ran all the program 		    successfully on my linux laptop.
	
	c.i) Error on CADE during compiling: 

					g++ -Wall -Wconversion -O3 -fPIC -o train train.c tron.o linear.o blas/blas.a
					/usr/bin/ld: tron.o: unrecognized relocation (0x2a) in section `.text'
					/usr/bin/ld: final link failed: Bad value
					collect2: error: ld returned 1 exit status
					make: *** [Makefile:20: train] Error 1


	c.ii) Error on CADE after using precompiled train and predict files:	
					./train: /lib64/libstdc++.so.6: version `CXXABI_1.3.8' not found (required by ./train)
					./train: /lib64/libstdc++.so.6: version `CXXABI_1.3.9' not found (required by ./train)

d) Limitations, bugs or problems - None as per tests and runs on my linux machine. The python code runs successfully on both my laptop and CADE machines. Could not get the machine learning tool executables to run on CADE.