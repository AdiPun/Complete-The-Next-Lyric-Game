# run_all_profiles.py
import os
import subprocess
import time
from datetime import datetime

SCRIPTS = [
    ("Slow Version", "optical_sweep_slow.py"),
    ("Optimized Version", "optical_sweep_fast.py")
]

REPORT_FILE = "profiling_report.txt"

def run_and_time(cmd):
    """Run a command and return elapsed time (seconds)."""
    start = time.perf_counter()
    subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end = time.perf_counter()
    return round(end - start, 3)

def log(line):
    with open(REPORT_FILE, "a") as f:
        f.write(line + "\n")
    print(line)

def main():
    with open(REPORT_FILE, "w") as f:
        f.write(f"==== Optical Sweep Profiling Report ====\n")
        f.write(f"Generated: {datetime.now()}\n\n")

    for label, script in SCRIPTS:
        log(f"\n### {label} ({script}) ###\n")

        # --- 1. cProfile ---
        log("Running cProfile...")
        cprof_out = f"{script}_cprofile.txt"
        subprocess.run(
            f"python -m cProfile -s cumtime {script} > {cprof_out}", shell=True
        )
        time_cprof = run_and_time(f"python -m cProfile -s cumtime {script}")
        log(f"cProfile Total Time: {time_cprof} s")

        # --- 2. Scalene ---
        log("Running Scalene...")
        time_scalene = run_and_time(f"scalene --cli {script} > {script}_scalene.txt")
        log(f"Scalene Total Time: {time_scalene} s")

        # --- 3. Memory Profiler ---
        log("Running Memory Profiler...")
        time_mem = run_and_time(f"python -m memory_profiler {script} > {script}_mem.txt")
        log(f"Memory Profiler Total Time: {time_mem} s")

        log("\n-------------------------------------")

    log("\nAll profiling completed.\n")

if __name__ == "__main__":
    main()
