import levelset
import finduser
import utils
import os
from termcolor import colored
from tabulate import tabulate


# TO DO
# - Add better conenciton Error system
# - Use flask / DJango to create a web based GUI
# - Add "fail-safe" if user input isn't correct
# - Consistent formatting, add bold text, make sure spacing is right
# - ORganize imports

class UserCompare:
	def __init__(self, user1_data, user2_data, user1_name,
				 user2_name, level_set_data, level_set_name, level_set_url,
				 level_set_id):
		self.user1_data = user1_data
		self.user2_data = user2_data
		self.user1_name = user1_name
		self.user2_name = user2_name
		self.level_set_data = level_set_data
		self.level_set_name = level_set_name
		self.level_set_url = level_set_url
		self.level_set_id = level_set_id

	def get_level_time_ss(self):
		"""Returns a corresponding dictionary for a user for level scoretime."""
		user1_time_ss = {}
		user2_time_ss = {}

		# Sets user K:V pair. If value doesn't exist, sets to N/A
		for level, level_raw in self.level_set_data.items():
			try:
				user1_time_ss[level] = self.user1_data['ranks_scores'][
					level_raw]['time']
			except KeyError:
				user1_time_ss[level] = 'N/A'

			try:
				user2_time_ss[level] = self.user2_data['ranks_scores'][
					level_raw]['time']
			except KeyError:
				user2_time_ss[level] = 'N/A'

		return user1_time_ss, user2_time_ss

	def get_level_time_any(self):
		"""Returns a corresponding dictionary for a user for level timetime."""
		user1_time_any = {}
		user2_time_any = {}

		# Sets user K:V pair. If value doesn't exist, sets to N/A
		for level, level_raw in self.level_set_data.items():
			try:
				user1_time_any[level] = self.user1_data['ranks_times'][
					level_raw]['time']
			except KeyError:
				user1_time_any[level] = 'N/A'

			try:
				user2_time_any[level] = self.user2_data['ranks_times'][
					level_raw]['time']
			except KeyError:
				user2_time_any[level] = 'N/A'

		return user1_time_any, user2_time_any

	def compare_users_ss(self, user1_time_ss, user2_time_ss):
		"""Compares user ss times to one another and returns a formatted table."""
		headers = ['Levels -- SS', self.user1_name, self.user2_name, '+/-']
		table_ss = []
		# Creates row data
		for level, level_raw in self.level_set_data.items():
			user1_time_fmt = UserCompare.convert_time_get(user1_time_ss[level])
			user2_time_fmt = UserCompare.convert_time_get(user2_time_ss[level])
			user_time_difference = UserCompare.user_difference_get(
				user1_time_ss[level], user2_time_ss[level])

			table_ss.append([level, user1_time_fmt, user2_time_fmt,
							 user_time_difference])

		# Creates SS table using Tabulate
		print(tabulate(table_ss, headers=headers, tablefmt="double_outline",
					   colalign=('left', 'right', 'right', 'right',)))

	def compare_users_any(self, user1_timetimes, user2_timetimes):
		"""Compares user any% times to one another and returns a formatted table."""
		headers = ['Levels -- Any%', self.user1_name, self.user2_name, '+/-']
		table_any = []
		for level in self.level_set_data:
			user1_time_fmt = UserCompare.convert_time_get(user1_timetimes[
															  level])
			user2_time_fmt = UserCompare.convert_time_get(user2_timetimes[
															  level])
			user_time_difference = UserCompare.user_difference_get(
				user1_timetimes[level], user2_timetimes[level])

			table_any.append([level, user1_time_fmt, user2_time_fmt,
							  user_time_difference])

		# Creates Any% table using Tabulate
		print(tabulate(table_any, headers, tablefmt="double_outline",
					   colalign=('left', 'right', 'right', 'right')))

	@staticmethod
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

	@staticmethod
	def user_difference_get(user1_time, user2_time):
		try:
			user_difference = int(user1_time) - int(user2_time)

			# Checks for a negative #, which is faster, otherwise it is slower
			if user_difference < 0:
				user_difference = user_difference * -1
				user_difference = UserCompare.convert_time_get(user_difference)
				user_difference = f'-{user_difference}'
				user_difference = colored(user_difference, 'light_green')
			else:
				user_difference = UserCompare.convert_time_get(user_difference)
				user_difference = f'+{user_difference}'
				user_difference = colored(user_difference, 'light_red')

			return user_difference

		except ValueError:
			user_difference = 'N/A'
			return user_difference

	def main_menu(self):
		"""Main Menu Navigation."""
		print('MAIN MENU')
		print('1) Compare Times')
		print('2) Change Users')
		print('3) Change Level Set')
		print(f'\nUser1: {self.user1_name} \nUser2: {self.user2_name}')
		print(f'Level Set: {self.level_set_name}\n')

		x = input(utils.bold('Enter a number: '))

		# Compares user times using the given levelset
		if x == '1':
			os.system('clear||cls')
			# Gets the SS & Any% times for each user
			user1_time_ss, user2_time_ss = self.get_level_time_ss()
			user1_time_any, user2_time_any = self.get_level_time_any()
			# Compares SS & Any% times between each user
			self.compare_users_ss(user1_time_ss, user2_time_ss)
			self.compare_users_any(user1_time_any, user2_time_any)

			input(utils.bold('Enter anything to return to menu: '))

		# Re-requests dustkid.com and updates class variables
		elif x == '2':
			os.system('clear||cls')
			(self.user1_data, self.user2_data, self.user1_name,
			 self.user2_name) = finduser.search_users(self.level_set_url)

		# Re-grabs levelset json / user data and updates class variables
		elif x == '3':
			os.system('clear||cls')
			# Grabs the level set information depending on user choice
			self.level_set_name, self.level_set_url, self.level_set_id = (
				levelset.level_set_change())

			# Grabs full levelset data from json
			self.level_set_data = levelset.level_set_info(
				self.level_set_id, self.level_set_name)

			# Re grabs user information according to the levelset
			self.user1_data, self.user1_name = finduser.check_user(
				self.user1_name, self.level_set_url)
			self.user2_data, self.user2_name = finduser.check_user(
				self.user2_name, self.level_set_url)
		# TODO: Add fail safe
		else:
			pass


def main():
	"""Loads the main program and acts as a navigator."""

	# Loads default information
	level_set_name, level_set_url, level_set_id = utils.load_defaults()

	# Gets User 1 & 2 json files and dictionary of level names from levelset
	user1_data, user2_data, user1_name, user2_name = finduser.search_users(
		level_set_url)
	level_set_data = levelset.level_set_info(level_set_id, level_set_name)

	# Creates class instance of all user/level data
	compare_users = UserCompare(user1_data, user2_data, user1_name,
								user2_name, level_set_data, level_set_name,
								level_set_url, level_set_id)

	# TODO: Add more breakers, clearing of screen
	# Main game loop
	while True:
		os.system('clear||cls')
		compare_users.main_menu()


if __name__ == '__main__':
	main()
