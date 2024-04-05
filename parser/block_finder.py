import re

def find_last_block_with_min_lines(file_path, regexes = [
        r'\|(.+?)\|(.+?)\|', 
        r'\+(\=+)\+',
        r'\+[\-=]+\+'
    ], min_lines=20):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()[::-1]  # Reverse the lines
        block = []
        lines_count = 0
        found_last_block = False
        for line in lines:
            if any(re.match(regex, line) for regex in regexes):
                block.append(line)
            else:
                if found_last_block and len(block) >= min_lines:
                    return ''.join(block[::-1])  # Reverse the block to its original order
                if len(block) >= min_lines:
                    found_last_block = True
                block = []  # Reset block if a line that doesn't match is encountered
            lines_count = len(block)
        return None  # Return None if no second last block with the specified minimum lines is found

def count_data_blocks_with_min_lines(file_path, regexes = [
        r'\|(.+?)\|(.+?)\|', 
        r'\+(\=+)\+',
        r'\+[\-=]+\+'
    ], min_lines=20):
    with open(file_path, 'r', encoding='utf-8') as file:
        block_count = 0
        lines_in_block = 0
        for line in file:
            if any(re.match(regex, line) for regex in regexes):
                lines_in_block += 1
            else:
                if lines_in_block >= min_lines:
                    block_count += 1
                lines_in_block = 0  # Reset lines_in_block for a new block
    # Check if the last block meets the criteria
    if lines_in_block >= min_lines:
        block_count += 1
    return block_count - 1