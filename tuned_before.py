
def process_log(file_path):
    unique_lines = set()
    results = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            
            parts = line.split("--solution_index")
            base_line = parts[0].strip()
            
            if base_line not in unique_lines:
                unique_lines.add(base_line)
                results.append(line)

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <hipblaslt.log>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    filtered_lines = process_log(log_file_path)

    for line in filtered_lines:
        print(line)
