import os
import time

count = 0
with open("probe_input.txt") as file:
    for line in file:
        count = 0
        while count < 6:
            os.system('python3 run_json.py -r 100 ' + line.split()[0])
            os.system('python3 run_trace.py' + line.split()[0])
            count += 1 
            time.sleep(1)
