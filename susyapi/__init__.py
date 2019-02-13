import requests
import datetime
import re
import urllib3
from bs4 import BeautifulSoup

SUSY_PATH = "https://susy.ic.unicamp.br:9999"

def concatenate_url(url,new_part):
	"""Given a URL a new part that is trying to be appended to it, generates the new URL accordingly"""

	if url[-1] == "/":
		if new_part[0] == "/":
			return url + new_part[1:] # we avoid having two forward slashes
		else:
			return url + new_part
	elif new_part[0] == "/":
		return url + new_part
	else:
		return url + "/" + new_part

def get_html(url, error_message = "Erro: "):
	"""Fetches the HTML source of the given URL using the requests lib."""

	# Obtaining the html of the page
	try:
		# TODO: solve the SSL problem
		urllib3.disable_warnings()
		response = requests.get(url, timeout = 5, verify = False)
		response.raise_for_status()
	except requests.exceptions.Timeout:
		raise requests.exceptions.Timeout(error_message + "O servidor do IC demorou demais para responder.")
	except requests.exceptions.SSLError:
		raise requests.exceptions.SSLError(error_message + "Não foi possível conectar seguramente com o servidor do IC.")
	except requests.exceptions.ConnectionError:
		raise requests.exceptions.ConnectionError(error_message + "O servidor do IC retornou um erro de conexão.")
	except requests.exceptions.HTTPError:
		raise requests.exceptions.HTTPError(error_message + "O servidor do IC retornou um erro HTTP.")
	except Exception as e:
		raise e(error_message + "Erro desconhecido.")

	return response.text

def get_sections(url = SUSY_PATH):
	"""Returns a dictionary of all active sections listed on SuSy's main page.
	The key is the code of the section and the value is the section's SuSy address."""

	error_message = "Não foi possível obter todas as turmas: "

	# Obtaining the html of the page
	try:
		html_source = get_html(url,error_message)
	except Exception as e:
		raise e

	# Finding the table with the sections
	soup = BeautifulSoup(html_source, "html.parser")
	html_table = soup.find(lambda tag: tag.name == "table")
	table_rows = html_table.findAll(lambda tag: tag.name == "tr")

	# Iterates over all sections to build the final dictionaty
	sections = {}
	for row in table_rows:
		row_elements = row.findAll(lambda tag: tag.name == "td")
		section_reference = row_elements[0].find(lambda tag: tag.name == "a") # link to the section page
		section_code = section_reference.contents[0]
		section_url = concatenate_url(url,section_reference["href"])
		sections[section_code] = section_url

	return sections

def get_due_date(html_source):
	"""Given the HTML source of a SuSy assignment page, uses regex returns the due date of the assignment.
	Note: Dates are formated in dd/mm/YYYY and hours are formated in HH:MM:SS."""
	
	list_days = re.findall(r'\d+/\d+/\d+',html_source) # finds the pattern dd/mm/YYYY
	list_hours = re.findall(r'\d+:\d+:\d+',html_source) # finds the pattern HH:MM:SS

	try:

		if list_hours[1] == "24:00:00":
			# this is a very uncommon format and should be changed
			list_hours[1] = "23:59:59"

		due_date = list_days[1] + " " + list_hours[1] # concatenating dates
		return datetime.datetime.strptime(due_date, "%d/%m/%Y %H:%M:%S") # converting and returning date

	except IndexError:
		raise IndexError("Erro: a data de entrega não foi encontrada.")

def get_groups(html_source, url):
	"""Given the HTML source of a SuSy assignment page and the URL of the section, returns the groups of the assignment."""
	
	soup = BeautifulSoup(html_source,"html.parser")
	page_groups = [] # list that contains the URLs of the groups
	anchor_tags = soup.findAll(lambda tag: tag.name == "a")

	for anchor in anchor_tags:
		try:
			tag_reference = anchor["href"]
			if "relato" in tag_reference:
				page_groups.append(concatenate_url(url,tag_reference)) # we found a group
		except KeyError:
			continue # the anchor tag does not have an href element. very unusual

	return page_groups

def get_assignments(url):
	"""Returns a dictionary of all assignments listed on the section's page.
	The key is the name of the assignments and the value is a dictionary that contains
	the assignments SuSy address, the date it is due and its groups."""

	error_message = "Não foi possível obter as tarefas: "

	# Obtaining the html of the page
	try:
		# TODO: solve the SSL problem
		html_source = get_html(url,error_message)
	except Exception as e:
		raise e

	# Finding the table with the assignments
	soup = BeautifulSoup(html_source, "html.parser")
	html_table = soup.find(lambda tag: tag.name == "table")
	table_rows = html_table.findAll(lambda tag: tag.name == "tr")

	# Iterates over all assignments to build the final dictionaty
	assignments = {}
	for row in table_rows:

		assignment_dictionary = {}
		
		# Getting the code and url
		row_elements = row.findAll(lambda tag: tag.name == "td")
		assignment_reference = row_elements[0].find(lambda tag: tag.name == "a") # link to the assignment page
		assignment_code = assignment_reference.contents[0]
		assignment_dictionary["url"] = concatenate_url(url,assignment_code)

		# Getting the name, the due date and the groups
		assignment_dictionary["name"] = row_elements[1].contents[0].replace(u'\xa0'," ") # we replace unicode spaces
		assignment_html = get_html(assignment_dictionary["url"], "Erro ao processar " + assignment_code + ": ")
		assignment_html = BeautifulSoup(assignment_html,"html.parser").prettify()
		assignment_dictionary["due_date"] = get_due_date(assignment_html)
		assignment_dictionary["groups"] = get_groups(assignment_html,url)

		assignments[assignment_code] = assignment_dictionary

	return assignments
