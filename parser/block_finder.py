import re

def find_last_block_with_min_lines(file_path: str, regexes = [
        r'\|(.+?)\|(.+?)\|', 
        r'\+(\=+)\+',
        r'\+[\-=]+\+'
    ], min_lines = 20) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[::-1]
        block = []
        found_last_block = False
        for line in lines:
            if any(re.match(regex, line) for regex in regexes):
                block.append(line)
            else:
                if found_last_block and len(block) >= min_lines:
                    return ''.join(block[::-1])
                if len(block) >= min_lines:
                    found_last_block = True
                block = []
        return None