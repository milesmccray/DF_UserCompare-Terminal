import json                    # Loading JSON file into python
from tabulate import tabulate  # Table creation
import requests                # Requests made to https://dustkid.com
import utils


def level_set_change():
	"""Changes Level Set information."""
	level_sets_display = ['1) Stock Levels', '2) Community Map Pack',
						  '3) Dustforce Custom League',
						  '4) Backwards Dustforce',
						  '5) Nuclear Zone', '6) Rotated Clockwise',
						  '7) Rotated Counterclockwise', '8) Clunky',
						  '9) Dustforce Arcade', '10) Virtual',
						  '11) New Genesis',
						  '12) Single Screen', '13) Darkforce',
						  '14) Multiplayer',
						  '15) Color Dome', '16) Hideout']

	level_set_urls = ['all', 'cmp', 'league', 'ecroftsud', 'nuclear',
					  'rotated', 'rotatedccw', 'clunky', 'arcade',
					  'virtualnexus', 'newgenesis', 'singlescreen',
					  'darkforce', 'multi', 'colordome', 'hideout']

	level_sets = ['Stock Levels', 'Community Map Pack',
				  'Dustforce Custom League', 'Backwards Dustforce',
				  'Nuclear Zone', 'Rotated Clockwise',
				  'Rotated Counterclockwise', 'Clunky', 'Dustforce Arcade',
				  'Virtual', 'New Genesis', 'Single Screen', 'Darkforce',
				  'Multiplayer', 'Color Dome', 'Hideout']

	level_set_url = ''
	level_set_id = ''
	level_set_name = ''

	# Creates the table(s)
	draw_table, draw_header = create_table_level_set(level_sets_display)

	# Draws table to the screen
	print(draw_header)
	print(draw_table)

	# Loops through level_set_choice until a correct value is given
	while True:
		try:
			level_set_choice = input(utils.bold_underline('Enter a number: '))
			# Sets appropriate levelset information
			level_set_url = level_set_urls[int(level_set_choice) - 1]
			level_set_id = int(level_set_choice) - 1
			level_set_name = level_sets[int(level_set_choice) - 1]
			break
		except (ValueError, IndexError):
			print('You did not enter a value between 1-16')
			input(utils.bold_underline('Enter anything to try again: '))
			continue

	return level_set_name, level_set_url, level_set_id


def create_table_level_set(level_set_list):
	"""Creates a list of lists and a tabulate object and returns."""
	header = utils.header_frame_create(55, 1, 'CHOOSE YOUR LEVEL SET',
									   pad_adj=-1)

	# Creates the level_set_display data
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


def level_set_info(level_set_id, level_set_name):
	"""JSON Structure list>levelset(key)>level(key):(value)<levelset(key)>..."""
	with open('levelsets.json', 'r') as json_level_set:
		level_set_data = json.load(json_level_set)[level_set_id][level_set_name]

		return level_set_data


def level_set_get(levelset, setname):
	"""Returns a dictionary with K:Levelset name || V:List of levels."""
	level_records = {}
	while True:
		try:
			level_records = requests.get(
				f'https://dustkid.com/json/records/{levelset}').json()
			break
		except requests.exceptions.ConnectionError:
			input("Internet Connection Error...")
			continue
	level_set = []
	level_set_raw = list(level_records['Scores'].keys())
	level_set_dict = {}

	for i in range(len(level_set_raw)):
		level_set.append(level_records['Scores'][level_set_raw[i]]
						 ['levelname'])
		level_set_dict[level_set[i]] = level_set_raw[i]

	level_set_finished = {setname: level_set_dict}
	return level_set_finished


def level_set_setup():
	"""Creates a JSON file of all levelsets -- Shouldn't need to be run again"""
	master_level_set = []
	level_set = level_set_get('all', 'Stock Levels')
	master_level_set.append(level_set)
	level_set = level_set_get('cmp', 'Community Map Pack')
	master_level_set.append(level_set)
	level_set = level_set_get('league', 'Dustforce Custom League')
	master_level_set.append(level_set)
	level_set = level_set_get('ecroftsud', 'Backwards Dustforce')
	master_level_set.append(level_set)
	level_set = level_set_get('nuclear', 'Nuclear Zone')
	master_level_set.append(level_set)
	level_set = level_set_get('rotated', 'Rotated Clockwise')
	master_level_set.append(level_set)
	level_set = level_set_get('rotatedccw', 'Rotated Counterclockwise')
	master_level_set.append(level_set)
	level_set = level_set_get('clunky', 'Clunky')
	master_level_set.append(level_set)
	level_set = level_set_get('arcade', 'Dustforce Arcade')
	master_level_set.append(level_set)
	level_set = level_set_get('virtualnexus', 'Virtual')
	master_level_set.append(level_set)
	level_set = level_set_get('newgenesis', 'New Genesis')
	master_level_set.append(level_set)
	level_set = level_set_get('singlescreen', 'Single Screen')
	master_level_set.append(level_set)
	level_set = level_set_get('darkforce', 'Darkforce')
	master_level_set.append(level_set)
	level_set = level_set_get('multi', 'Multiplayer')
	master_level_set.append(level_set)
	level_set = level_set_get('colordome', 'Color Dome')
	master_level_set.append(level_set)
	level_set = level_set_get('hideout', 'Hideout')
	master_level_set.append(level_set)

	with open('levelsets.json', 'w') as file:
		json.dump(master_level_set, file, indent=2)
