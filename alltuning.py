import os
import subprocess
import sys
from multiprocessing import Process, Queue, current_process, Value, Lock
from queue import Empty
from tqdm import tqdm


def worker(task_queue, process_id, visible_device, tuning_file, progress, lock):
    while True:
        try:
            command = task_queue.get(timeout=1)
        except Empty:
            break

        full_command = f"ROCR_VISIBLE_DEVICES={visible_device} HIPBLASLT_TUNING_FILE={tuning_file} {command}"
        print(f"Process {process_id}: Executing {full_command}")

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            print(f"Process {process_id} Output:\n{result.stdout}")
            if result.stderr:
                print(f"Process {process_id} Errors:\n{result.stderr}")

        except Exception as e:
            print(f"Process {process_id} encountered an error: {e}")

        with lock:
            progress.value += 1


def process_log(file_path, rocm_bin_prefix, processes):
    with open(file_path, "r") as file:
        lines = file.readlines()

    commands = []
    for line in lines:
        line = line.strip()
        modified_command = f"{rocm_bin_prefix}{line} -i 1000 -j 1000"
        commands.append(modified_command)

    task_queue = Queue()

    for command in commands:
        task_queue.put(command)

    progress = Value("i", 0)
    total_tasks = len(commands)
    lock = Lock()

    processes_list = []
    with tqdm(total=total_tasks, desc="Progress", unit="task") as pbar:
        for process_id, visible_device in enumerate(processes):
            tuning_file = f"tuning{visible_device}.txt"
            p = Process(
                target=worker,
                args=(task_queue, process_id, visible_device, tuning_file, progress, lock),
            )
            processes_list.append(p)
            p.start()

        while any(p.is_alive() for p in processes_list):
            with lock:
                completed_tasks = progress.value
            pbar.n = completed_tasks
            pbar.refresh()

    for p in processes_list:
        p.join()

    pbar.close()


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(
            "Usage: python script.py <hipblaslt.log> </path/to/rocm/bin/> -p <list_of_devices>"
        )
        sys.exit(1)

    log_file_path = sys.argv[1]
    rocm_bin_prefix = sys.argv[2]
    if not rocm_bin_prefix.endswith("/"):
        rocm_bin_prefix += "/"

    if "-p" not in sys.argv:
        print("Error: Missing -p parameter for process devices.")
        sys.exit(1)

    p_index = sys.argv.index("-p")
    devices = list(map(int, sys.argv[p_index + 1 :]))

    process_log(log_file_path, rocm_bin_prefix, devices)

      
