import os

def find_result_logs(root_dir):
    result_logs = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "result.log":
                result_logs.append(os.path.join(root, file))
    return result_logs

# Example usage:
root_directory = "data/Д3"
result_log_files = find_result_logs(root_directory)

print("List of result.log files:")
for result_log_file in result_log_files:
    print(result_log_file)
