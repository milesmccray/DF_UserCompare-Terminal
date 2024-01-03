from bs4 import BeautifulSoup
import requests


# TO DO
# Add terminal clearing functionality


def search_users(level_set):
	"""Returns a dictionary from the user JSON """
	user1 = input('Enter username or ID of user1: ')
	user1 = check_user(user1, level_set)

	user2 = input('Enter username or ID of user2: ')
	user2 = check_user(user2, level_set)

	return user1, user2


def check_user(user, level_set):
	"""Checks the given user if valid and returns json dictionary."""
	while True:
		URL_J = 'https://dustkid.com/json/profile'
		URL = 'https://dustkid.com/profile'
		flag = 0

		if ' ' in user:
			user.replace(' ', '%20')

		# Flag is raised if they entered an ID number
		if user.isnumeric():
			flag = 1

		try:
			if flag != 1:
				user_page = requests.get(f'{URL_J}/{user}/{level_set}').json()

				return user_page

			# If flag was raised, reconstruct request call to contain username
			if flag == 1:
				user_page_id = requests.get(f'{URL_J}/{user}/').json()
				user_name = user_page_id['ranks_scores']['newtutorial1'][
					'username']
				user_id = user_page_id['ranks_scores']['newtutorial1']['user']
				user_page_id = requests.get(f'{URL_J}/{user_id}/'
											f'{user_name}/{level_set}').json()
				return user_page_id

		except requests.exceptions.ConnectionError:
			print("Connection Error")
			print('exiting...')

		# Checks why the json url failed, and what page it is on
		except requests.exceptions.JSONDecodeError:
			error_page = requests.get(f'{URL}/{user}/')

			# Checks can't find user page
			if 'Profile - Cannot find user' in error_page.text:
				print("\nCouldn't find user")
				user_retry = input('Enter username or ID of a user: ')

				# Resets the user variable and tries again
				user = user_retry
				continue

			# Checks multiple user page
			elif 'Please select a user' in error_page.text:
				multiple_users_html = BeautifulSoup(error_page.content,
													'html.parser')
				print('Multiple users found')
				for user_found in multiple_users_html.find_all('li'):
					print(user_found.get_text())
				user_retry = input('\nType the ID number of the correct user or '
								   'try again: ')

				# Resets the user variable and tries again
				user = user_retry
				continue

			# TODO FAIL SAFE ADD
			else:
				print('Error')
