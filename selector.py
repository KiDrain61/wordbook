import numpy as np
import argparse
from googletrans import Translator
import os
import re

def base_generator():
	'''
	1.将collection.txt中的单词提取出来
 	2.将单词储存到sorted_words.txt中
	3.将单词及其翻译储存到translated_words.txt中
	'''
	raw_words_path = './data/collection.txt'
	sorted_words_path = './data/sorted_words.txt'
	translated_words_path = './data/translated_words.txt'
	translator = Translator(service_urls=["translate.googleapis.com"])
	# 根据文件修改时间判断是否需要重新生成全单词表(默认两个单词表创建时间相同)
	if os.path.exists(sorted_words_path):
		if os.stat(raw_words_path).st_mtime < os.stat(sorted_words_path).st_ctime:# 如果原单词表修改时间早于新单词表创建时间，则不再生成
			return
	# 生成不带翻译的及带翻译的全单词表
	try:
		with open(raw_words_path,'r') as raw_words_file, \
	  	open(sorted_words_path, 'w') as sorted_words_file, open(translated_words_path, 'w') as translated_words_file:
				lines = raw_words_file.readlines()
				##index = 0
				for line in lines:
					if line != '\n':
						words = line.split(',')
						for word in words:
							word = word.strip()#bug1:鬼使神差把word传为参数了...
							sorted_words_file.write(word+'\n')
							translated_words_file.write(word+'='+translator.translate(word,dest='zh-cn').text+'\n')
	except FileNotFoundError:
		print("raw_words_file is not found.")
	except PermissionError:
		print("You don't have permission to access raw_words_file.")
	

def pipeline():
	base_generator()
	#select_words()

if __name__ == '__main__':
	pipeline()
 

