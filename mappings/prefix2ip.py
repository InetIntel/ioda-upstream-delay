import json
def get_prefix(ip_address):
    # Split the IP address into octets
    octets = ip_address.split('.')

    # Get the last octet
    last_octet = octets[-1]

    # Create the prefix by replacing the last octet and adding a /24
    prefix = '.'.join(octets[:-1] + ['0']) + '/24'

    return prefix

# Example IP file path
ip_file_path = '../hitlist/internet_address_hitlist_it105w-20230926/internet_address_hitlist_it105w-20230926.fsdb'

# Dictionary to store the mapping of prefixes to sets of IP addresses
prefix_to_ip_mapping = {}
prefix_to_val = {}

# Read the IP file and populate the dictionary
with open(ip_file_path, 'r') as ip_file:
    for line in ip_file:
        columns = line.split()
        if len(columns) == 3:
            ip_address = columns[2]
            prefix = get_prefix(ip_address)

            # If the prefix is not in the dictionary, add it with an empty set
            if prefix not in prefix_to_ip_mapping:
                prefix_to_ip_mapping[prefix] = set()

            # Add the current IP address to the set for the corresponding prefix
            prefix_to_ip_mapping[prefix].add(ip_address)
            prefix_to_val[prefix] = int(columns[1])

# Example prefix file path
prefix_file_path = '../hitlist/internet_address_hitlist_it105w-20230926/internet_address_verfploeter_hitlist_it105w-20230926.fsdb'

# Update the IP values based on the hex values from the prefix file
with open(prefix_file_path, 'r') as prefix_file:
    for line in prefix_file:
        columns = line.split()
        if len(columns) == 2:
            hex_prefix = columns[0]
            hex_values = columns[1].split(",")
            if hex_values[0] == "-":
                continue
            prefix = '.'.join(str(int(hex_prefix[i:i+2], 16)) for i in (0, 2, 4, 6)) + "/24"
            if prefix_to_val[prefix] < 90:
                for hex_value in hex_values:
                
                    # Add the decimal value of hex_value to the last octet of the prefix
                    ip = prefix[:len(prefix) - 3].split('.')
                    ip = ip[0] + "." + ip[1] + "." + ip[2] + "." + str(int(hex_value, 16))

                    # Check if the prefix exists in the mapping
                    if prefix in prefix_to_ip_mapping:
                        # Add the updated prefix to the mapping
                        prefix_to_ip_mapping[prefix].add(ip)

# Print the updated mapping
json_data = json.dumps({prefix: list(ip_set) for prefix, ip_set in prefix_to_ip_mapping.items()}, indent=2)

# Write the JSON data to a file
json_output_file = 'prefix2ip.json'
with open(json_output_file, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON data has been written to {json_output_file}")
