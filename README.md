# SuSy API [![Python 3.5+](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/download/releases/3.5.0/) [![PyPI release](https://img.shields.io/pypi/v/susyapi.svg)](https://pypi.org/project/susyapi/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

An API to get data from [University of Campinas' Submission System (SuSy)](https://www.ic.unicamp.br/~susy/).

## Install

To install the API, simply run: 
`pip install susyapi`

## Usage

The main endpoints are the `get_sections`, `get_assignments` and `get_users`  functions.

```
susyapi.get_sections()

Fetch list of sections from SuSy's page

Args:
    url (str): The URL of SuSy's main page. If none is provided, the default one is used.

Returns:
    sections (dict): A dictionary where the key is the section code and the value is the section URL.

susyapi.get_assignments()

Fetch list of assignments from a SuSy's section's page

Args:
    url (str): The URL of  a SuSy's section's page.

Returns:
    assignments (dict): A dictionary where the key is the assignment code and the value is a dictionary
    containing the assignment name, due date and a list of its groups.

susyapi.get_users()

Fetch list of users who completed the assignment from a SuSy's assignment's group page

Args:
    url (str or list): The URL (or list of URLs) of a SuSy's assignment's group page.

Returns:
    completed_users (list): A list of the id of the users that completed the assignment.

```

Example:
```Python
>>> import susyapi
>>> susyapi.get_sections()
{'mc202def': 'https://susy.ic.unicamp.br:9999/mc202def',
 'mc999': 'https://susy.ic.unicamp.br:9999/mc999',
 'mo901a': 'https://susy.ic.unicamp.br:9999/mo901a'}
>>> susyapi.get_assignments("https://susy.ic.unicamp.br:9999/mc999")
{'00': {'url': 'https://susy.ic.unicamp.br:9999/mc999/00',
  'name': 'Contagem de linhas e caracteres  ',
  'due_date': datetime.datetime(2020, 12, 31, 23, 59, 59),
  'groups': ['https://susy.ic.unicamp.br:9999/mc999/00/relatoA.html',
   'https://susy.ic.unicamp.br:9999/mc999/00/relatoB.html']},
 '01': {'url': 'https://susy.ic.unicamp.br:9999/mc999/01',
  'name': 'Contagem de linhas: seleção de processador  ',
  'due_date': datetime.datetime(2020, 12, 28, 23, 59, 59),
  'groups': ['https://susy.ic.unicamp.br:9999/mc999/01/relatoA.html',
   'https://susy.ic.unicamp.br:9999/mc999/01/relatoB.html']}}
>>> susyapi.get_users("https://susy.ic.unicamp.br:9999/mc999/01/relatoA.html")
["visita"]
```