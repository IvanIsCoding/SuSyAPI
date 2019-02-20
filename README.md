# SuSy API

An API to get data from University of Campinas' Submission System (SuSy).

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
    completed_users (list): A dictionary where the key is the section code and the value is the section URL.

```

Example:
```Python
>>> import susyapi
>>> susyapi.get_sections()
>>> { "mc202def": "",
    "mc999": "",
    "mc901": ""
}
>>> susyapi.get_assignments("")
{}
>>> susyapi.get_users("")
["visita"]
```