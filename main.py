import os                      # Terminal Clearing
from tabulate import tabulate  # Table creation
import levelset
import finduser
import utils


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
		"""Returns a corresponding dictionary for SS leve:time."""
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
		"""Returns a corresponding dictionary for any% leve:time."""
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
		"""Compares user ss times and prints a formatted table."""
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
		"""Compares user any% and prints a formatted table."""
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
		"""Converts milliseconds to seconds/minutes/hours X:XX:XX.XXX fmt."""
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
		"""Returns the difference in milliseconds between users and colors"""
		try:
			user_difference = int(user1_time) - int(user2_time)

			# Checks for a negative #, which is faster, otherwise it is slower
			if user_difference < 0:
				user_difference = user_difference * -1
				user_difference = UserCompare.convert_time_get(user_difference)
				user_difference = f'-{user_difference}'
				user_difference = utils.color_string(user_difference,
													 'light_green')
			else:
				user_difference = UserCompare.convert_time_get(user_difference)
				user_difference = f'+{user_difference}'
				user_difference = utils.color_string(user_difference,
													 'light_red')

			return user_difference

		except ValueError:
			user_difference = 'N/A'
			return user_difference

	def main_menu(self):
		"""Main Menu Navigation."""
		table = [['1) Compare Times'], ['2) Change Users'], ['3) Change Level'
															 ' Set']]
		header = utils.header_frame_create(21, 1, 'MAIN MENU', pad_adj=-1)

		# Print Main Menu Table
		print(header)
		print(tabulate(table, tablefmt='double_outline'))

		# Print current level/user data
		print(f"\n{utils.bold_underline('User 1:')}{self.user1_name}\n"
			  f"{utils.bold_underline('User 2:')}{self.user2_name}")
		print(f"{utils.bold_underline('Level Set:')}{self.level_set_name}")

		menu_nav = input(utils.bold_underline('\nEnter a number: '))
		# Compares user times using the given levelset
		if menu_nav == '1':  # Compare Times
			os.system('clear||cls')

			# Gets the SS & Any% times for each user
			user1_time_ss, user2_time_ss = self.get_level_time_ss()
			user1_time_any, user2_time_any = self.get_level_time_any()
			# Compares SS & Any% times between each user
			self.compare_users_ss(user1_time_ss, user2_time_ss)
			self.compare_users_any(user1_time_any, user2_time_any)

			input(utils.bold_underline('Enter anything to return to menu: '))

		# Re-requests dustkid.com and updates class variables
		elif menu_nav == '2':  # Change Users
			os.system('clear||cls')
			(self.user1_data, self.user2_data, self.user1_name,
			 self.user2_name) = finduser.search_users(self.level_set_url)

		# Re-grabs levelset json / user data and updates class variables
		elif menu_nav == '3':  # Change Level Set
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
		else:  # Catch fail-safe
			print('\nYou did not enter one of the options...')
			input(utils.bold_underline('Enter anything to return to menu: '))


def main():
	"""Loads the main program and acts as a navigator."""

	# Loads default information stored in defaults.json
	level_set_name, level_set_url, level_set_id = utils.load_defaults()

	# Pulls levelset list using defaults
	level_set_data = levelset.level_set_info(level_set_id, level_set_name)

	# Requests User 1 & 2 JSON files
	user1_data, user2_data, user1_name, user2_name = finduser.search_users(
		level_set_url)

	# Creates class instance using user/level data
	compare_users = UserCompare(user1_data, user2_data, user1_name,
								user2_name, level_set_data, level_set_name,
								level_set_url, level_set_id)

	# Main game loop
	while True:
		os.system('clear||cls')
		compare_users.main_menu()


if __name__ == '__main__':
	main()
