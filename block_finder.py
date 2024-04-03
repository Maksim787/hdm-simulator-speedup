import re

def find_block_with_min_lines(file_path, regexes = [
        r'\|(.+?)\|(.+?)\|', 
        r'\+(\=+)\+',
        r'\+[\-=]+\+'
    ], min_lines=20):
    with open(file_path, 'r', encoding='utf-8') as file:
        print(file)
        block = []
        lines_count = 0
        for line in file:
            print(line)
            if any(re.match(regex, line) for regex in regexes):
                block.append(line)
            else:
                lines_count = len(block)
                if lines_count >= min_lines:
                    return block
                block = []  # Reset block if a line that doesn't match is encountered
        # Check if the last block meets the criteria
        lines_count = len(block)
        if lines_count >= min_lines:
            return block
    return None  # Return None if no block with the specified minimum lines is found
