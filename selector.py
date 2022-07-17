import numpy as np
import argparse
from googletrans import Translator
import os
import re

def sort_words():
	try:
		sorted_words_path = './data/sorted_words.txt'
		with open(sorted_words_path, 'w') as sorted_words_file:
			raw_words_path = './data/collection.txt'
			with open(raw_words_path,'r') as raw_words_file:
				lines = raw_words_file.readlines()
				##index = 0
				for line in lines:
					if line != '\n':
						#print(line)正常
						words = line.split(',')
						#print(words)正常
						for word in words:
							#print(word)正常
							##index += 1
							word = word.strip()#bug1:鬼使神差把word传为参数了...
							#print(word)
							##sorted_words_file.write(f'{index} '+word+'\n')
							sorted_words_file.write(word+'\n')
	except FileNotFoundError:
		print("raw_words_file is not found.")
	except PermissionError:
		print("You don't have permission to access raw_words_file.")

				

def pipeline():
	sort_words()
	#translate_words()
	#select_words()

if __name__ == '__main__':
	pipeline()
