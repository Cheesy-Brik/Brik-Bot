import subprocess
import time
import sys

error_times = []

count = 0

reserved_error_codes = [3, 4]

while True:
    process = subprocess.run(
        ["python", "Main.py"] + sys.argv[1:], stdout=subprocess.PIPE
    )

    # If the process exited due to an error, then process.returncode will not be 0, and process.stderr will contain the error message.
    print("---------------------------------------------")
    if process.returncode not in reserved_error_codes:
        try:
            print(process.stderr.decode("utf-8"))
        except:
            pass
        error_times.append(time.time())
        if len(error_times) > 1 and error_times[-1] - error_times[-2] < 5 * count:
            count += 1
        else:
            count = 0
        time.sleep(min(2 * count, 300))
    elif process.returncode == reserved_error_codes[0]:
        print("\033[1m" + "User Initiated Restart")
    elif process.returncode == reserved_error_codes[1]:
        print("\033[1m" + "User Initiated Exit")
        break
    print("\033[0m" + "---------------------------------------------")
