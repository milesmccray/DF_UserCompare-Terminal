from termcolor import colored
import json


# Find a way to not under line space?

def underline(string):
	x = colored(string, attrs=['underline'])
	return x


def bold(string):
	x = colored(string, attrs=['bold'])
	return x


def load_defaults():
	"""Loads default information from defaults.json."""
	with open('defaults.json', 'r') as f:
		defaults = json.load(f)

	level_set_name = defaults['level_set_name']
	level_set_url = defaults['level_set_url']
	level_set_id = defaults['level_set_id']

	return level_set_name, level_set_url, level_set_id
