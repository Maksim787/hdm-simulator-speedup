import re

def parse_table(text : str) -> dict:
    if text == None:
        return {}
    data = {}

    row_pattern = r'\|(.+?)\|(.+?)\|'

    rows = re.findall(row_pattern, text)

    for row in rows:
        key = row[0].strip()
        value = row[1].strip()

        data[key] = value

    return data

