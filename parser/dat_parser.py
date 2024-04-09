def extract_key_values(file_path: str) -> dict:
    key_values = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        runctrl_found = False
        for line in file:
            line = line.strip()
            if runctrl_found:
                if line == '/':
                    break
                elif line:
                    key, val = line.split()
                    key_values[key] = float(val)
            elif line == 'RUNCTRL':
                runctrl_found = True
    return key_values
