import levelset_utils
import finduser
from termcolor import colored
from tabulate import tabulate


# TO DO
# - Add a way to choose levelset
# who have that name. Type dustkid.com/profiles/miles
# - Add better conenciton Error system
# - Use flask / DJango to create a web based GUI
# - Make a 'loading' bar during a request?
# - Create a class and organize document around it
# - Add "fail-safe" if user input isn't correct
# - Consistent formatting


def nav_choice(string):
	x = colored(string, attrs=['bold', 'underline'])
	return x


class UserCompare:
	def __init__(self, userid1, userid2, levelset):
		self.userid1 = userid1
		self.userid2 = userid2
		self.levelset = levelset


def get_level_time_ss(user1, user2, level_set_data):
	"""Returns a corresponding dictionary for a user for level scoretime."""
	user1_time_ss = {}
	user2_time_ss = {}

	# Sets user K:V pair. If value doesn't exist, sets to N/A
	for level, level_raw in level_set_data.items():
		try:
			user1_time_ss[level] = user1['ranks_scores'][level_raw]['time']
		except KeyError:
			user1_time_ss[level] = 'N/A'

		try:
			user2_time_ss[level] = user2['ranks_scores'][level_raw]['time']
		except KeyError:
			user2_time_ss[level] = 'N/A'

	return user1_time_ss, user2_time_ss


def level_timetime_get(user1, user2, level_set, level_set_raw):
	"""Returns a corresponding dictionary for a user for level timetime."""
	user1_timetimes = {}
	user2_timetimes = {}

	# Sets user K:V pair. If value doesn't exist, sets to N/A
	for i, level in enumerate(level_set):
		try:
			user1_timetimes[level] = user1['ranks_times'][
				level_set_raw[i]]['time']
		except KeyError:
			user1_timetimes[level] = 'N/A'

		try:
			user2_timetimes[level] = user2['ranks_times'][
				level_set_raw[i]]['time']
		except KeyError:
			user2_timetimes[level] = 'N/A'

	return user1_timetimes, user2_timetimes


def user_difference_get(user1_time, user2_time):
	try:
		user_difference = int(user1_time) - int(user2_time)

		# Checks for a negative #, which is faster, otherwise it is slower
		if user_difference < 0:
			user_difference = user_difference * -1
			user_difference = convert_time_get(user_difference)
			user_difference = f'-{user_difference}'
			user_difference = colored(user_difference, 'light_green')
		else:
			user_difference = convert_time_get(user_difference)
			user_difference = f'+{user_difference}'
			user_difference = colored(user_difference, 'light_red')

		return user_difference

	except ValueError:
		user_difference = 'N/A'
		return user_difference


def convert_time_get(user_time):
	"""Converts milliseconds to seconds."""
	if user_time == 'N/A':
		return user_time
	else:
		# Converts to seconds & cuts off decimal at 3 places
		user_time_fmt = format(round(user_time / 1000, 3), '.3f')

		# Checks if time is above 1 min, and properly converts
		if 3600 > float(user_time_fmt) > 59.999:
			# Returns a tuple containing quotient and remainder
			user_time_min, user_time_sec = divmod(float(user_time_fmt), 60)
			user_time_min = int(user_time_min)
			user_time_sec = format(user_time_sec, '.3f')

			# Checks if seconds are below 10 and adds a 0
			if float(user_time_sec) < 10:
				user_time_sec = f'0{user_time_sec}'

			# Create a string with proper clock format
			user_time_fmt = f'{user_time_min}:{user_time_sec}'
			return user_time_fmt

		# Checks if time is above 1 hour, and properly converts
		elif float(user_time_fmt) > 3600:
			user_time_min, user_time_sec = divmod(float(user_time_fmt), 60)
			user_time_hour, user_time_min = divmod(user_time_min, 60)
			user_time_sec = format(user_time_sec, '.3f')
			user_time_min = int(user_time_min)
			user_time_hour = int(user_time_hour)

			# Checks if seconds are below 10 and adds a 0
			if float(user_time_sec) < 10:
				user_time_sec = f'0{user_time_sec}'

			# Checks if minutes are below 10 and adds a 0
			if int(user_time_min) < 10:
				user_time_min = f'0{user_time_min}'

			# Create a string with proper clock format
			user_time_fmt = f'{user_time_hour}:{user_time_min}:{user_time_sec}'
			return user_time_fmt

		else:
			return user_time_fmt


def compare_users_ss(user1_scoretimes, user2_scoretimes, level_set):
	"""Compares user ss times to one another and returns a formatted table."""
	headers = ['Levels -- SS', 'USER 1', 'USER 2', '+/-']
	table = []
	# Creates row data
	for level in level_set:
		user1_time = convert_time_get(user1_scoretimes[level])
		user2_time = convert_time_get(user2_scoretimes[level])
		user_difference = user_difference_get(user1_scoretimes[level],
											  user2_scoretimes[level])
		table.append([level, user1_time, user2_time, user_difference])

	# Creates SS table using Tabulate
	print(tabulate(table, headers=headers, tablefmt="double_outline",
				   colalign=('left', 'right', 'right', 'right',)))


def compare_users_any(user1_timetimes, user2_timetimes, level_set):
	"""Compares user any% times to one another and returns a formatted table."""
	headers = ['Levels -- Any%', 'USER 1', 'USER 2', '+/-']
	table = []
	for level in level_set:
		user1_time = convert_time_get(user1_timetimes[level])
		user2_time = convert_time_get(user2_timetimes[level])
		user_difference = user_difference_get(user1_timetimes[level],
											  user2_timetimes[level])
		table.append([level, user1_time, user2_time, user_difference])

	# Creates Any% table using Tabulate
	print(tabulate(table, headers, tablefmt="double_outline",
				   colalign=('left', 'right', 'right', 'right')))


def main_menu(level_set):
	"""Main Menu Navigation."""
	levelset_default = 'Stock Levels'
	levelset = levelset_default
	print('1) Compare Times')
	print('2) Change Level Set')
	print(f'\nCurrent Level Set: {levelset}\n')
	x = input(nav_choice('Enter a number: '))
	return x


def main():
	"""Loads the main program and acts as a navigator."""

	# Default levelset information
	level_set_name = 'Stock Levels'
	level_set_url = 'all'
	level_set_id = 0

	# Returns user time information on level set
	user1, user2 = finduser.search_users(level_set_url)

	x = main_menu(level_set_name)
	if x == '1':
		level_set_data = levelset_utils.level_set_info(
			level_set_id, level_set_name)

		user1_time_ss, user2_time_ss = get_level_time_ss(user1, user2,
														 level_set_data)
		print(user1_time_ss)
		print(user2_time_ss)

		#user1_timetimes, user2_timetimes = level_timetime_get(user1, user2,
															  #level_set,
															 # level_set_raw)
		#compare_users_ss(user1_scoretimes, user2_scoretimes, level_set)
		#compare_users_any(user1_timetimes, user2_timetimes, level_set)
	if x == '2':
		level_set, level_set_url, level_set_id = (
			levelset_utils.level_set_change())


if __name__ == '__main__':
	main()
