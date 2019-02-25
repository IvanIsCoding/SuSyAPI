import requests
import datetime
import re
import urllib3
from bs4 import BeautifulSoup
import urllib.parse

SUSY_PATH = "https://susy.ic.unicamp.br:9999"
__version__ = "0.1.1"


def _format_user_id(user_id):
    """Given an user id, removes the ra prefix from it."""

    if type(user_id) is not str:
        raise TypeError("Erro: o argumento devem ser uma string.")

    if len(user_id) >= 3 and user_id[:2] == "ra":
        return user_id[2:]  # the prefix ra should be removed
    else:
        return user_id


def _get_html(url, error_message="Erro: "):
    """Fetches the HTML source of the given URL using the requests lib."""

    # Checking arguments type
    if (type(url) is not str) or (type(error_message) is not str):
        raise TypeError("Erro: os argumentos devem ser strings.")

    # Obtaining the html of the page
    try:
        # TODO: solve the SSL problem
        urllib3.disable_warnings()
        response = requests.get(url, timeout=5, verify=False)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise requests.exceptions.Timeout(
            error_message + "O servidor do IC demorou demais para responder."
        )
    except requests.exceptions.SSLError:
        raise requests.exceptions.SSLError(
            error_message
            + "Não foi possível conectar seguramente com o servidor do IC."
        )
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError(
            error_message + "O servidor do IC retornou um erro de conexão."
        )
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError(
            error_message + "O servidor do IC retornou um erro HTTP."
        )
    except Exception as e:
        raise e(error_message + "Erro desconhecido.")

    return response.text


def get_sections(url=SUSY_PATH):
    """Returns a dictionary of all active sections listed on SuSy's main page.
    The key is the code of the section and the value is the section's SuSy address."""

    # Checking argument type
    if type(url) is not str:
        raise TypeError("Erro: o argumento devem ser uma string.")

    error_message = "Não foi possível obter todas as turmas: "

    # Obtaining the html of the page
    try:
        html_source = _get_html(url, error_message)
    except Exception as e:
        raise e

    # Finding the table with the sections
    soup = BeautifulSoup(html_source, "html.parser")
    html_table = soup.find(lambda tag: tag.name == "table")

    # no match, return empty dict
    if html_table is None:
        return {}

    table_rows = html_table.findAll(lambda tag: tag.name == "tr")

    # Iterates over all sections to build the final dictionaty
    sections = {}
    for row in table_rows:
        row_elements = row.findAll(lambda tag: tag.name == "td")
        section_reference = row_elements[0].find(
            lambda tag: tag.name == "a"
        )  # link to the section page
        section_code = str(section_reference.contents[0])
        section_url = urllib.parse.urljoin(url, section_reference["href"])
        sections[section_code] = section_url

    return sections


def _get_due_date(html_source):
    """Given the HTML source of a SuSy assignment page, uses regex returns the due date of the assignment.
    Note: Dates are formated in dd/mm/YYYY and hours are formated in HH:MM:SS."""

    # Checking argument type
    if type(html_source) is not str:
        raise TypeError("Erro: o argumento devem ser uma string.")

    list_days = re.findall(r"\d+/\d+/\d+", html_source)  # finds the pattern dd/mm/YYYY
    list_hours = re.findall(r"\d+:\d+:\d+", html_source)  # finds the pattern HH:MM:SS

    try:

        if list_hours[1] == "24:00:00":
            # this is a very uncommon format and should be changed
            list_hours[1] = "23:59:59"

        due_date = list_days[1] + " " + list_hours[1]  # concatenating dates
        return datetime.datetime.strptime(
            due_date, "%d/%m/%Y %H:%M:%S"
        )  # converting and returning date

    except IndexError:
        raise IndexError("Erro: a data de entrega não foi encontrada.")


def _get_groups(html_source, url):
    """Given the HTML source of a SuSy assignment page and the URL of the section, returns the groups of the assignment."""

    # Checking arguments type
    if (type(html_source) is not str) or (type(url) is not str):
        raise TypeError("Erro: os argumentos devem ser strings.")

    soup = BeautifulSoup(html_source, "html.parser")
    page_groups = []  # list that contains the URLs of the groups
    anchor_tags = soup.findAll(lambda tag: tag.name == "a")

    for anchor in anchor_tags:
        try:
            tag_reference = anchor["href"]
            if "relato" in tag_reference:
                page_groups.append(
                    urllib.parse.urljoin(url, tag_reference)
                )  # we found a group
        except KeyError:
            continue  # the anchor tag does not have an href element. very unusual

    return page_groups


def get_assignments(url):
    """Given a URL, returns a dictionary of all assignments listed on the section's page.
    The key is the name of the assignments and the value is a dictionary that contains
    the assignments SuSy address, the date it is due and its groups."""

    # Checking argument type
    if type(url) is not str:
        raise TypeError("Erro: o argumento devem ser uma string.")

    error_message = "Não foi possível obter as tarefas: "

    # Obtaining the html of the page
    try:
        html_source = _get_html(url, error_message)
    except Exception as e:
        raise e

    # Finding the table with the assignments
    soup = BeautifulSoup(html_source, "html.parser")
    html_table = soup.find(lambda tag: tag.name == "table")

    # no match, return empty dict
    if html_table is None:
        return {}

    table_rows = html_table.findAll(lambda tag: tag.name == "tr")

    # Iterates over all assignments to build the final dictionaty
    assignments = {}
    for row in table_rows:

        assignment_dictionary = {}

        # Getting the code and url
        row_elements = row.findAll(lambda tag: tag.name == "td")
        assignment_reference = row_elements[0].find(
            lambda tag: tag.name == "a"
        )  # link to the assignment page
        assignment_code = str(assignment_reference.contents[0])
        assignment_dictionary["url"] = urllib.parse.urljoin(
            url, assignment_reference["href"]
        )

        # Getting the name, the due date and the groups
        assignment_dictionary["name"] = (
            row_elements[1].contents[0].replace(u"\xa0", " ")
        )  # we replace unicode spaces
        assignment_html = _get_html(
            assignment_dictionary["url"], "Erro ao processar " + assignment_code + ": "
        )
        assignment_html = BeautifulSoup(assignment_html, "html.parser").prettify()
        assignment_dictionary["due_date"] = _get_due_date(assignment_html)
        assignment_dictionary["groups"] = _get_groups(
            assignment_html, assignment_dictionary["url"]
        )

        assignments[assignment_code] = assignment_dictionary

    return assignments


def get_users(url):
    """Given a URL of a group or a list of URLs, returns a list all the users that have completed the assignment in that group"""

    # Checking argument type
    if type(url) not in (list, str):
        raise TypeError("Erro: o argumento devem ser uma lista ou string.")

    # Handling list case
    if type(url) is list:

        completed_users = []  # list of users that have done the assignment

        for url_link in url:
            # We get the users for each link and append it to the list
            completed_users.extend(get_users(url_link))

        return completed_users

    error_message = "Não foi possível obter os usuários: "

    # Obtaining HTML page
    try:
        html_source = _get_html(url)
    except Exception as e:
        raise e

    # Finding the table with the users
    soup = BeautifulSoup(html_source, "html.parser")
    html_table = soup.find(lambda tag: tag.name == "table")

    # no match, return empty list
    if html_table is None:
        return []

    table_rows = html_table.findAll(lambda tag: tag.name == "tr")

    # Geting user id from the table
    completed_users = []  # list of users that have done the assignment
    for index, row in enumerate(table_rows):

        if index == 0:
            continue  # we skip the table head

        row_elements = row.findAll(lambda tag: tag.name == "td")
        user_id = str(row_elements[0].contents[0])
        correct_submissions = int(row_elements[2].contents[0])

        if correct_submissions > 0:
            # The user has at least one correct submission, add the id to the list
            completed_users.append(_format_user_id(user_id))

    return completed_users
