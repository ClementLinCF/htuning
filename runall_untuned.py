import csv
import os
import subprocess

def process_log(file_path, output_csv, exec_prefix, visible_device):
    headers = ["transA", "transB", "m", "n", "k", "hipblaslt-Gflops", "hipblaslt-GB/s", "us"]

    with open(output_csv, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)

        with open(file_path, "r") as log_file:
            for line in log_file:
                line = line.strip()

                if "--algo_method" in line:
                    parts = line.split("--algo_method")
                    modified_line = (
                        f"{exec_prefix}{parts[0]}--algo_method heuristic --requested_solution 1 -i 1000 -j 1000"
                    )

                    command = f"ROCR_VISIBLE_DEVICES={visible_device} {modified_line}"

                    try:
                        result = subprocess.run(
                            command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                        )
                        output = result.stdout.splitlines()

                        for idx, out_line in enumerate(output):
                            if out_line.startswith("[0]:"):
                                next_line = output[idx + 1]
                                values = next_line.split(",")

                                transA, transB = values[0], values[1]
                                m, n, k = values[4], values[5], values[6]
                                gflops, gbps, us = values[-3:]
                                csv_writer.writerow([transA, transB, m, n, k, gflops, gbps, us])
                                break

                    except Exception as e:
                        print(f"Error executing command: {command}")
                        print(f"Exception: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 5:
        print(
            "Usage: python script.py <hipblaslt.log> <output.csv> </path/to/rocm/bin/> <visible_device>"
        )
        sys.exit(1)

    log_file_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    rocm_bin_prefix = sys.argv[3]
    visible_device = sys.argv[4]

    if not rocm_bin_prefix.endswith("/"):
        rocm_bin_prefix += "/"

    process_log(log_file_path, output_csv_path, rocm_bin_prefix, visible_device)

