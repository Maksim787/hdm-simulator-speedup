def extract_key_values(file_path):
    key_values = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        runctrl_found = False
        for line in file:
            line = line.strip()
            if runctrl_found:
                if line == '/':  # End of block
                    break
                elif line:
                    key, val = line.split()
                    key_values[key] = float(val)
            elif line == 'RUNCTRL':
                runctrl_found = True
    return key_values

if __name__ == "__main__":
    file_path = input("Enter the path to the text file: ")
    key_values = extract_key_values(file_path)
    if key_values:
        print("KEY - VALUE pairs:")
        for key, value in key_values.items():
            print(f"{key}: {value}")
    else:
        print("No 'RUNCTRL' found or no 'KEY val' pairs found after 'RUNCTRL'.")
