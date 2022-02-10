#!/usr/bin/env pyhton3

from PIL import Image
import os
import json
import math
import copy

class FontX2:
	def __init__(self):
		pass

	def new(self, start, stop, width, height):
		self.type = 'FONTX2' # magic code
		self.name = 'NEW     ' # font name
		self.width = width # width
		self.height = height # height

		fs = (self.width + 7) // 8 * self.height # font size
		self.flag = 1

		self.cb = [{'start': start,'end': stop}]
		self.chars_number = stop - start
		self.chars = []
		for c in range(start, stop):
			font = [[0 for i in range(self.width)] for j in range(self.height)]
			self.chars.append({'char': c, 'bitmap': font})

	def from_binary(self, filename):
		self.filename = filename # filename
		with open(filename,'rb') as f:
			self.type = f.read(6).decode('ascii') # magic code
			self.name = f.read(8).decode('ascii') # font name
			self.width = int.from_bytes(f.read(1), 'little') # width
			self.height = int.from_bytes(f.read(1), 'little') # height

			fs = (self.width + 7) // 8 * self.height # font size
			offset = 0
			filesize = os.path.getsize(filename)
			self.flag = int.from_bytes(f.read(1), 'little')
			if self.flag == 0: # flag = 0 -> single byte
				offset = 17
			else: # flag = 1 -> double byte
				self.cb = []
				cb = int.from_bytes(f.read(1), 'little') # number of code blocks

				for i in range(cb):
					cbs = int.from_bytes(f.read(2), 'little') # start code
					cbe = int.from_bytes(f.read(2), 'little') # end code
					self.cb.append({'start': cbs, 'end': cbe})

				offset = 18 + 4 * cb

			self.chars = []
			self.chars_number = round((filesize - offset) / fs)

			for c in range(self.chars_number): # read a single char
				fontpat = f.read(fs)
				x = 0
				y = 0
				font = [[0 for i in range(self.width)] for j in range(self.height)]

				for s in range(fs):
					for b in range(8):
						if fontpat[s] & 0b10000000 >> b > 0:
							font[y][x] = 1

						x += 1
						if x == self.width:
							x = 0
							y += 1
							break
				self.chars.append({'char': c, 'bitmap': font})

	def invert(self):
		for c in self.chars: # read a single char
			y = 0;
			for row in c['bitmap']:
				x = 0
				for col in row:
					if col == 1:
						c['bitmap'][y][x] = 0
					else:
						c['bitmap'][y][x] = 1
					x += 1
				y += 1

	def crop(self, result, sx=0, dx=0, top=0, bottom=0):
		result.type = self.type # magic code
		result.name = self.name # font name
		result.width = self.width - sx - dx # width
		result.height = self.height - top - bottom # height

		fs = (self.width + 7) // 8 * self.height # font size
		result.flag = self.flag

		if self.flag != 0: # flag = 1 -> double byte
			result.cb =  copy.deepcopy(self.cb)

		result.chars = []
		for char in self.chars:
			new_char = {'char': char['char'], 'bitmap': []}
			row_counter = -1
			for row in char['bitmap']:
				row_counter += 1
				if row_counter < top:
					continue
				if row_counter > self.height - bottom - 1:
					continue

				col_counter = -1
				line = []
				for col in row:
					col_counter += 1
					if col_counter < sx:
						continue
					if col_counter > self.width - dx - 1:
						continue

					line.append(col)

				new_char['bitmap'].append(line)
				line = []

			result.chars.append(new_char)
		result.chars_number = len(result.chars)

	def to_binary(self, filename):
		with open(filename,'wb') as f:
			f.write(self.type.encode()) # magic code
			f.write(self.name.encode()) # font name
			f.write(self.width.to_bytes(1, 'little')) # width
			f.write(self.height.to_bytes(1, 'little')) # height
			f.write(self.flag.to_bytes(1, 'little')) # flag = 0 -> single byte
			fs = (self.width + 7) // 8 * self.height # font size
			if self.flag != 0: # flag = 1 -> double byte
				f.write(len(self.cb).to_bytes(1, 'little')) # blocks numbers
				for i in self.cb:
					f.write(i['start'].to_bytes(2, 'little')) # start code
					f.write(i['end'].to_bytes(2, 'little')) # end code
			for char in self.chars:
				for byte in char['bitmap']:
					b = 8
					value = 0
					for bit in byte:
						b -= 1
						value += bit * 2 ** b
						written = False
						if b == 0:
							f.write(value.to_bytes(1, 'little'))
							written = True
							value = 0
							b = 8
					if written == False:
						f.write(value.to_bytes(1, 'little'))

	def from_json(self, json_str):
		font_json = json.loads(json_str)
		self.type = font_json['type'] # magic code
		self.name = font_json['name']  # font name
		self.width = font_json['width']  # width
		self.height = font_json['height']  # height
		self.flag = font_json['flag'] # flag = 0 -> single byte
		if self.flag != 0:
			self.cb = font_json['cb']
		self.chars = font_json['chars']
		self.chars_number = len(self.chars)

	def to_json(self):
		serialized = '{'
		serialized += f'\t"type": "{self.type}",\n'
		serialized += f'\t"name": "{self.name}",\n'
		serialized += f'\t"width": {self.width},\n'
		serialized += f'\t"height": {self.height},\n'
		serialized += f'\t"flag": {self.flag},\n'

		if self.flag == 0:
			pass
		else:
			serialized += '\t"cb": [\n'
			for block in  self.cb[:-1]:
				serialized += '\t\t'+json.dumps(block)+',\n'
			serialized += '\t\t'+json.dumps(self.cb[-1])+'\n'
			serialized += '\t],\n'

		serialized += '\t"chars": [\n'
		for char in self.chars[:-1]:
			serialized += '\t\t{\n'
			serialized += f'\t\t\t"char": {char["char"]},\n'
			serialized += '\t\t\t"bitmap": [\n'
			for row in char['bitmap'][:-1]:
				serialized += '\t\t\t\t'+json.dumps(row)+',\n'
			serialized += '\t\t\t\t'+json.dumps(char['bitmap'][-1])+'\n'
			serialized += '\t\t\t]\n'
			serialized += '\t\t},\n'

		char = self.chars[-1]
		serialized += '\t\t{\n'
		serialized += f'\t\t\t"char":{char["char"]},\n'
		serialized += '\t\t\t"bitmap":[\n'
		for row in char['bitmap'][:-1]:
			serialized += '\t\t\t\t'+json.dumps(row)+',\n'
		serialized += '\t\t\t\t'+json.dumps(char['bitmap'][-1])+'\n'
		serialized += '\t\t\t]\n'
		serialized += '\t\t}\n'
		serialized += '\t]\n'
		serialized += '}\n'

		return serialized

	def to_picture(self, filename):
		cols = 52
		rows = math.ceil(self.chars_number / cols)

		img = Image.new('RGB', (self.width * cols, self.height * rows))

		for row in range(rows):
			for col in range(cols):
				try:
					char = self.chars[row * cols + col]
					for i in range(self.width):
						for j in range(self.height):
							if char['bitmap'][j][i] == 1:
								img.putpixel((col * self.width + i, row * self.height + j), (255,255,255))
				except:
					pass
		img.save(filename)
