import os
import time

count_total = 0
count_iter = 0

while count_total < 15:
    count_iter = 0
    while count_iter < 5:
        with open("probe_input.txt") as file:
            for line in file:
                os.system('python3 run_json.py -r 100 ' + line.split()[0] + " " + str(count))
                print("Done")
                time.sleep(1)
        count_iter += 1
    count_total += 1
    # Sleep for 1 hour
    time.sleep(3600)
