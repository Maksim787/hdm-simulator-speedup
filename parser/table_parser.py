import re

def parse_table(text):
    if text == None:
        return {}
    # Initialize an empty dictionary to store the data
    data = {}

    # Define regular expressions to match table rows
    row_pattern = r'\|(.+?)\|(.+?)\|'

    # Find all headers and rows in the text
    rows = re.findall(row_pattern, text)

    for row in rows:
        # Extract key and value from the row
        key = row[0].strip()
        value = row[1].strip()

        # Store the data in the dictionary
        data[key] = value

    return data

