import os
import json

visited = set()

def process_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    ips_satisfying_condition = []
    
    for entry in data["_source"]['data']:
        dest_ip = entry['dest']['ip']
        as_path = entry['as_path']

        if dest_ip in visited:
            continue
        visited.add(dest_ip)
        
        # Check if at least 80% of the hops have a value and not 'N/A'
        num_valid_hops = sum(1 for hop in as_path if hop.strip() != '' and hop != 'N/A')
        total_non_empty_hops = sum(1 for hop in as_path if hop.strip() != '')
        if total_non_empty_hops > 0 and num_valid_hops / total_non_empty_hops >= 0.7:
            ips_satisfying_condition.append(dest_ip)
            if len(ips_satisfying_condition) == 20:
                break
    
    return ips_satisfying_condition

def main():
    folder_path = 'elastic_docs'
    ips_found = []
    
    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            ips = process_file(file_path)
            ips_found.extend(ips)
            #if len(ips_found) >= 20:
                #break
    
    print("20 IPs satisfying the condition:")
    for i, ip in enumerate(ips_found, start=1):
        print(f"{i}. {ip}")

if __name__ == "__main__":
    main()

