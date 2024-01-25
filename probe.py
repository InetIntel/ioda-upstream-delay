import os
import time
import argparse
from optimiseIP import get_single_ip
from get_prefix_list import as2prefix_get_list
from get_ip_list import generate_ips_for_prefixes

def run_probe(input_file, input_type, probe_rate):

        if input_type == "A":
            as2prefix_get_list(input_file)
            generate_ips_for_prefixes("prefix2ip.json", "prefixes.txt", "optimized_ip.txt")

        else:
            generate_ips_for_prefixes("prefix2ip.json", input_file, "optimized_ip.txt")

        for rate in probe_rate:
           # get_single_ip("prefix_list.txt", "optimized_ip.txt", 9000000)

            count_total = 0
            count_iter = 0

            while count_total < 1:
                count_iter = 0
                while count_iter < 1:
                    count = count_total * 1 + count_iter
                    os.system(f'python3 run_json.py -r {rate} -n 5 -i optimized_ip.txt {count}')
                    print("Done")
                    time.sleep(1)
                    count_iter += 1
                count_total += 1
                # Sleep for 10 seconds
                time.sleep(10)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the probe script.")
    parser.add_argument("-i", "--input_file", help="Input file name")
    parser.add_argument("-t", "--input_type", help="Type of file list: A/P")
    parser.add_argument("-r", "--probe_rate", nargs='+', help="Probe rate")

    args = parser.parse_args()

    run_probe(args.input_file, args.input_type, args.probe_rate)

