import csv
import re
import subprocess
import sys


def parse_and_execute(file_path, output_csv, visible_device, prefix_string):
    with open(file_path, "r") as f:
        lines = f.readlines()

    with open(output_csv, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ["transA", "transB", "m", "n", "k", "hipblaslt-Gflops", "hipblaslt-GB/s", "us"]
        )

        for line in lines:
            modified_command = re.sub(r"--solution_index \d+.*", "", line.strip())
            modified_command += " --algo_method heuristic --requested_solution 1 --print_kernel_info -i 1000 -j 1000"

            modified_command = (
                f"ROCR_VISIBLE_DEVICES={visible_device} {prefix_string}{modified_command}"
            )

            try:
                result = subprocess.run(
                    modified_command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                )

                output = result.stdout + result.stderr

                match = re.search(
                    r"transA,transB.*?hipblaslt-Gflops,hipblaslt-GB/s,us\n(.*?)\n",
                    output,
                    re.DOTALL,
                )
                if match:
                    data_line = match.group(1).strip()
                    data_values = data_line.split(",")
                    
                    transA, transB = data_values[0], data_values[1]
                    m, n, k = data_values[4], data_values[5], data_values[6]
                    gflops, gbps, us = data_values[-3:]

                    csv_writer.writerow([transA, transB, m, n, k, gflops, gbps, us])

            except Exception as e:
                print(f"Error executing command: {modified_command}")
                print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Usage: python script.py <hipblaslt.log> <output.csv> <visible_device> <prefix_string>"
        )
        sys.exit(1)

    log_file = sys.argv[1]
    output_csv = sys.argv[2]
    visible_device = sys.argv[3]
    prefix_string = sys.argv[4]

    parse_and_execute(log_file, output_csv, visible_device, prefix_string)

