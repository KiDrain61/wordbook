import numpy as np
import argparse
from googletrans import Translator
import os
import linecache
from pathlib import Path

def generate_base():
	'''
	若原单词表修改时间早于新单词表创建时间，则
		1.将collection.txt中的单词提取出来
		2.将单词储存到sorted_words.txt中
		3.将单词及其翻译储存到translated_words.txt中
		4.输出单词总个数
	否则仅输出单词总个数
	'''
	global raw_words_path
	global sorted_words_path
	global translated_words_path
	translator = Translator(service_urls=["translate.googleapis.com"])
	global total_num_of_words # 声明全局变量
	# 根据文件修改时间判断是否需要重新生成全单词表(默认两个单词表创建时间相同)
	if os.path.exists(sorted_words_path):
		if os.stat(raw_words_path).st_mtime < os.stat(sorted_words_path).st_ctime:
			total_num_of_words = len(open(sorted_words_path).readlines()) - 1
			print(f"There are {total_num_of_words} words in total.\n")
			return
	# 生成不带翻译的及带翻译的全单词表
	try:
		with open(raw_words_path,'r') as raw_words_file, \
	  	open(sorted_words_path, 'w') as sorted_words_file, open(translated_words_path, 'w') as translated_words_file:
				lines = raw_words_file.readlines()
				for line in lines:
					if line != '\n':
						words = line.split(',')
						for word in words:
							total_num_of_words += 1
							word = word.strip()#bug1:鬼使神差把word传为参数了...
							sorted_words_file.write(word+'\n')
							translation = translator.translate(word,dest='zh-cn').text
							translated_words_file.write(f'{word:-<25}{translation}\n')
				print(f"There are {total_num_of_words} words in total.\n")
	except FileNotFoundError:
		print("raw_words_file is not found.")
	except PermissionError:
		print("You don't have permission to access raw_words_file.")
	
def parse_cmd():
	'''
	具体使用参数约定如下：
	1. -n 表示用户希望从自己所选择范围内具体想要复习的单词数量
	2. --r 表示用户希望随机选择单词（不输入 --r 则表示不希望随机选择）
	3. -s 表示用户希望从第几个单词开始
	4. -l 表示用户希望复习的单词范围大小，也即从 start 开始，长度为 length
	'''
	parser = argparse.ArgumentParser(description='传入生成单词本的需求')

	parser.add_argument('-n', type=int, default=100, help='从自己所选择范围内具体想要复习的单词数量')
	parser.add_argument('--r', action='store_true', help='输入之，表示希望随机选择单词')
	parser.add_argument('-s', type=int, default=1, help='希望从第几个单词开始')
	parser.add_argument('-l', type=int, default=200, help='希望复习的单词范围大小，也即从 start 开始，长度为 length')

	args = parser.parse_args()
	return (args.n, args.r, args.s, args.l)

def select_words():
	nums, random, start, length = parse_cmd()
	# 检测是否单词选择是否超出范围
	if nums > length or start + length - 1 > total_num_of_words:
		print('error: range exceeded')
		return
	# 根据是否随机选择不同的单词序号集
	if random:
		rng = np.random.default_rng()
		selected = np.nditer(rng.integers(start, start + length -1,size=nums))
	else:
		selected = range(start, start + length -1)
	# 生成对应的输出文件名

	file_index = 1
	output_path = Path.cwd() / 'output'# 突然想起来用一下，不要在意前后路径表示不一致的问题_(:з」∠)_
	if not os.path.exists(output_path):
		os.system('mkdir output')
	while os.path.exists(output_path / f'untranslated_{file_index}'):
		file_index += 1
	# 生成对应的输出文件
	with open(output_path / f'untranslated_{file_index}','w') as untranslated_output,\
    	open(output_path / f'translated_{file_index}','w') as translated_output:
		for each in selected:
			untranslated_output.write(linecache.getline(sorted_words_path,each)+'\n')
			translated_output.write(linecache.getline(translated_words_path,each)+'\n')
	linecache.clearcache()

def pipeline():
	generate_base()
	select_words()
 

raw_words_path = './data/collection.txt'
sorted_words_path = './data/sorted_words.txt'
translated_words_path = './data/translated_words.txt'
total_num_of_words = 0

if __name__ == '__main__':
	pipeline()
 

