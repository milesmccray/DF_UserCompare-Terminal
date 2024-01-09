import json                    # Loading JSON file into python
from sys import platform
import os
from termcolor import colored  # Colored text/terminal (bold/underline MAC only)


def bold_underline(string):
	"""Removes trailing space, underlines, and then adds it back."""
	x = colored(string.rstrip(), attrs=['bold', 'underline'])
	x = x + ' '

	return x


def color_string(string, color):
	col_string = colored(string, color)
	return col_string


def program_exit():
	exit()


def check_os():
	"""Checks if user system is windows and runs color command."""
	if platform == 'win32':
		os.system('color')
	elif platform == 'linux':
		print('This version of the program does not work with Linux!')
	elif platform == 'darwin':
		pass


def clear():
	if platform == 'win32':
		os.system('cls')
	elif platform == 'linux':
		print('This version of the program does not work with Linux!')
	elif platform == 'darwin':
		os.system('clear')


def header_frame_create(hlength, vlength, string, pad_adj=None):
	"""Creates a box with given values."""
	string_pad_1 = ' ' * (round((hlength - len(string)) / 2))
	if pad_adj is not None:
		string_pad_2 = ' ' * (round((hlength - len(string)) / 2) + pad_adj)
	else:
		string_pad_2 = ' ' * (round((hlength - len(string)) / 2))
	title_str = bold_underline(string)
	# Set the table values
	hframe = '═' * hlength
	vframe = f'║{string_pad_1}{title_str}{string_pad_2}║'
	cframe = ['╔', '╗', '╚', '╝']

	# Build the table
	header_frame_top = f'{cframe[0]}{hframe}{cframe[1]}\n'
	header_frame_line = f'{vframe}\n' * vlength
	header_frame_bottom = f'{cframe[2]}{hframe}{cframe[3]}'

	header_frame = header_frame_top + header_frame_line + header_frame_bottom

	return header_frame


def load_defaults():
	"""Loads default information from defaults.json."""
	with open('defaults.json', 'r') as f:
		defaults = json.load(f)

	level_set_name = defaults['level_set_name']
	level_set_url = defaults['level_set_url']
	level_set_id = defaults['level_set_id']

	return level_set_name, level_set_url, level_set_id

