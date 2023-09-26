import os
import time

count = 0
with open("probe_input.txt") as file:
    while count < 10:
        for line in file:
            os.system('python3 run_json.py -r 100 ' + line.split()[0])
            print("Done Y")
            print("Done N")
            time.sleep(1)
        count += 1
