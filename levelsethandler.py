from tabulate import tabulate
import requests
from main import nav_choice


def choose_level_set():
	level_set = ['1) Standard Levels', '2) Community Map Pack',
				 '3) Dustforce Custom League', '4) Backwards Dustforce',
				 '5) Nuclear Zone', '6) Rotated Clockwise',
				 '7) Rotated Counter Clockwise', '8) Clunky',
				 '9) Dustforce Arcade', '10) Virtual', '11) New Genesis',
				 '12) Single Screen', '13) Darkforce', '14) Multiplayer',
				 '15) Color Dome', '16) Hideout']

	draw_table, header = create_table_level_set(level_set)

	print(header)
	print(draw_table)
	level_set_choice = input(nav_choice('Enter a number: '))


def create_table_level_set(level_set_list):
	"""Creates a list of lists and a tabulate object and returns."""
	header = """
╔═══════════════════════════════════════════════════════╗
║                 CHOOSE YOUR LEVEL SET                 ║
╚═══════════════════════════════════════════════════════╝"""

	# Creates the data table
	level_pair_list = []
	all_level_sets_list = []
	count = 0
	for level_set in level_set_list:
		level_pair_list.append(level_set)
		count += 1
		if count == 2:
			all_level_sets_list.append(level_pair_list)
			level_pair_list = []
			count = 0
	level_sets = all_level_sets_list

	# Creates a table object with tabulate
	draw_table = tabulate(level_sets, tablefmt='double_outline')

	return draw_table, header


def level_set_get():
	"""Returns all the levels as a list."""
	try:
		level_records = requests.get('https://dustkid.com/json/records').json()
		level_set = []
		level_set_raw = list((level_records['Scores'].keys()))
		# Renames the raw level names to the standard level names
		for i in range(len(level_set_raw)):
			level_set.append(level_records['Scores'][level_set_raw[i]]
							 ['levelname'])

		return level_set, level_set_raw

	except requests.exceptions.ConnectionError:
		print('bad connection')
		print('exiting...')
