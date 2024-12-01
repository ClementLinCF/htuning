import os

def merge_and_remove_duplicates(directory, output_file):
    line_count = {}

    for filename in os.listdir(directory):
        if filename.startswith("tuning") and filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.rstrip("\n")
                    if line in line_count:
                        line_count[line] += 1
                    else:
                        line_count[line] = 1

    sorted_lines = sorted(line_count.keys(), key=lambda x: -line_count[x])

    with open(output_file, "w") as output:
        output.writelines(line + "\n" for line in sorted_lines)

    print(f"All files have been merged and duplicate lines removed; the results are saved in {output_file}")


os.system("rm -f tuning.txt")

directory = "."
output_file = "tuning.txt"
merge_and_remove_duplicates(directory, output_file)

