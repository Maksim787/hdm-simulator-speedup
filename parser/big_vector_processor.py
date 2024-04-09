def process_line(line):
    values = line.split()
    result = []
    for value in values:
        if value == '/':
            return result
        elif '*' in value:
            factors = value.split('*')
            result.append(float(factors[0]) * float(factors[1]))
        else:
            result.append(float(value))
    return result

def parse_big_file(file_path):
    result = []
    with open(file_path, 'r') as file:
        for line in file:
            if '--' not in line and len(line) != 0:
                result.extend(process_line(line))
    return result

