import os
import json

as_path_threshold = 0.7
visited = set()

def process_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    ips_satisfying_condition = []
    visited_asn = set()
    total = 0

    for entry in data['data']:
        dest_ip = entry['dest']['ip']
        as_path = entry['as_path']

        if dest_ip in visited:
            continue
        visited.add(dest_ip)
        total += 1

        # Check if at least 80% of the hops have a value and not 'N/A'
        num_valid_hops = sum(1 for hop in as_path if hop.strip() != '' and hop != 'N/A')
        total_non_empty_hops = sum(1 for hop in as_path if hop.strip() != '')
        if total_non_empty_hops > 0 and num_valid_hops / total_non_empty_hops >= 0.7:
            ips_satisfying_condition.append(dest_ip)
            #if len(ips_satisfying_condition) == 20:
                #break

    return len(ips_satisfying_condition) >= 0.8*total


def main():
    folder_path = 'elastic_docs'

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            if process_file(file_path):
                print(filename)

    # Print AS numbers with at least 70% full AS paths for all IPs
    print("AS numbers satisfying the condition:")
    #for as_number, stats in as_paths.items():
        #if stats['total_ips'] > 0 and stats['ips_with_full_as_path'] / stats['total_ips'] >= as_path_threshold:
            #print(f"AS{as_number}: {stats['ips_with_full_as_path']} out of {stats['total_ips']} IPs")

if __name__ == "__main__":
    main()
