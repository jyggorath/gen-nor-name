#!/usr/bin/env python
from sys import stderr
from argparse import ArgumentParser
from requests import get
from random import choice
from bs4 import BeautifulSoup
from typing import Union


def get_names(category: str) -> list:
	if category == 'surname':
		response = get('https://no.wikipedia.org/wiki/Liste_over_norske_etternavn')
	elif category == 'female':
		response = get('https://no.wikipedia.org/wiki/Liste_over_norske_kvinnenavn')
	elif category == 'male':
		response = get('https://no.wikipedia.org/wiki/Liste_over_norske_mannsnavn')
	else:
		raise Exception('Unsupported name category: ' + category)
	html = BeautifulSoup(response.text, 'html.parser')
	table = html.findAll('table')[-1]
	name_links = table.findAll('a')
	names = []
	for name_link in name_links:
		names.append(name_link.text.strip())
	return names


def to_int(s: str) -> Union[int, None]:
	try:
		return int(s)
	except ValueError:
		return None


if __name__ == '__main__':

	argument_parser = ArgumentParser()
	argument_parser.add_argument('--number', '-n', help="number of names to generate, by default it's just one")
	argument_parser.add_argument('--female', '-f', action='store_true', help='generate female name (default is random if male or female)')
	argument_parser.add_argument('--male', '-m', action='store_true', help='generate male name (default is random if male or female)')
	argument_parser.add_argument('--first-name', '-fn', action='store_true', help='generate first name only (default is firstname + surname)')
	argument_parser.add_argument('--surname', '-s', action='store_true', help='generate surname only (default is firstname + surname)')
	arguments = argument_parser.parse_args()

	number = 1

	if arguments.number is not None:
		number = to_int(arguments.number)
		if number is None:
			print('Invalid number:', arguments.number, file=stderr)
			exit(1)

	surnames = []
	female_names = []
	male_names = []

	if arguments.first_name or (not arguments.first_name and not arguments.surname):
		if arguments.female or (not arguments.female and not arguments.male):
			female_names = get_names('female')
		if arguments.male or (not arguments.female and not arguments.male):
			male_names = get_names('male')
	if arguments.surname or (not arguments.first_name and not arguments.surname):
		surnames = get_names('surname')

	for i in range(number):

		first_name = None
		surname = None

		if arguments.first_name or (not arguments.first_name and not arguments.surname):
			if (not arguments.female and not arguments.male) or (arguments.female and arguments.male):
				first_name = choice([choice(female_names), choice(male_names)])
			elif arguments.female:
				first_name = choice(female_names)
			elif arguments.male:
				first_name = choice(male_names)
		
		if arguments.surname or (not arguments.first_name and not arguments.surname):
			surname = choice(surnames)
		
		if first_name and surname:
			print(first_name, surname)
		elif first_name:
			print(first_name)
		elif surname:
			print(surname)
