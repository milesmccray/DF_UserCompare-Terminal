from bs4 import BeautifulSoup
import requests


# TO DO
# Add terminal clearing functionality
# Check for duplicates on common names


def search_users():
	user1 = input('Enter username or ID of user1: ')
	user1 = check_user(user1)

	user2 = input('Enter username or ID of user2: ')
	user2 = check_user(user2)

	return user1, user2


def check_user(user):
	URL_J = 'https://dustkid.com/json/profile'
	URL = 'https://dustkid.com/profile'
	if ' ' in user:
		user.replace(' ', '%20')

	try:
		user_page = requests.get(f'{URL_J}/{user}/').json()
		return user_page

	except requests.exceptions.ConnectionError:
		print("Connection Error")
		print('exiting...')

	# Checks why the json url failed, and what page it is on
	except requests.exceptions.JSONDecodeError:
		error_page = requests.get(f'{URL}/{user}/')

		# Checks page
		if 'Profile - Cannot find user' in error_page.text:
			print("Couldn't find user")
			user_retry = input('Enter username or ID of user1: ')
			check_user(user_retry)

		elif 'Please select a user' in error_page.text:
			multiple_users_html = BeautifulSoup(error_page.content,
											   'html.parser')
			print('Multiple users found')
			for user_found in multiple_users_html.find_all('li'):
				print(user_found.get_text())
			user_retry = input('\nType the ID number of the correct user: ')
			check_user(user_retry)

		else:
			print('Error')




search_users()
