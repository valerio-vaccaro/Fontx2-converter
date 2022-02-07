#!/usr/bin/env pyhton3

import os
import glob
from fontx2 import FontX2

def convert_all():
	directory = 'fontx'
	try:
		os.mkdir(f'./{directory}/jpg/')
		os.mkdir(f'./{directory}/json/')
		os.mkdir(f'./{directory}/recreated/')
	except:
		pass

	for filename in glob.glob(f'./{directory}/*.fnt'):
		filename = os.path.basename(filename)
		print(filename+' ', end = '')

		# import binary
		font = FontX2()
		font.from_binary(f'./{directory}/'+filename)
		font.to_picture(f'./{directory}/jpg/'+filename+'.orig.jpg')
		fs = (font.width + 7) // 8 * font.height # font size
		print(f'size {fs} chars {font.chars_number} ', end = '')
		print('to_picture ... ', end = '')

		# convert to json
		json_file = open(f'./{directory}/json/'+filename+'.json', 'w')
		json_file.write(font.to_json())
		json_file.close()
		print('to_json ... ', end = '')

		# import json and save as binary
		font2 = FontX2()
		json_file = open(f'./{directory}/json/'+filename+'.json','r+')
		font2.from_json(json_file.read())
		json_file.close()
		font2.to_picture(f'./{directory}/jpg/'+filename+'.from_json.jpg')
		print('to_picture ... ', end = '')
		font2.to_binary(f'./{directory}/recreated/'+filename+'.new.fnt')
		print('to_binary ... END!')

		# recreated from new binary
		print('Recreated ... ', end = '')
		font = FontX2()
		font.from_binary(f'./{directory}/recreated/'+filename+'.new.fnt')
		font.to_picture(f'./{directory}/jpg/'+filename+'.recreated.jpg')
		fs = (font.width + 7) // 8 * font.height # font size
		print(f'size {fs} chars {font.chars_number} ', end = '')
		print('to_picture  ... END!')

		# strip
		print('Stripping ... ', end = '')
		font = FontX2()
		font2 = FontX2()
		json_file = open(f'./{directory}/json/'+filename+'.json','r+')
		font.from_json(json_file.read())
		json_file.close()
		font.crop(font2, 0, 0, 2, 0)
		json_file = open(f'./{directory}/json/'+filename+'.stripped.json', 'w')
		json_file.write(font2.to_json())
		json_file.close()
		print('to_json ... ', end = '')
		font2.to_picture(f'./{directory}/jpg/'+filename+'.stripped.jpg')
		print('to_picture ... ', end = '')
		font2.to_binary(f'./{directory}/recreated/'+filename+'.stripped.fnt')
		print('to_binary ... END!')

if __name__ == "__main__":
	convert_all()
