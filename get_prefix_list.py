import json

# Load the JSON file with AS numbers and corresponding prefixes
with open('as2prefix.json', 'r') as json_file:
    as_dict = json.load(json_file)

# Read AS numbers from the text file
with open('as_numbers.txt', 'r') as as_numbers_file:
    as_numbers = [line.strip() for line in as_numbers_file]

# Get corresponding prefixes for each AS number
prefixes = []
for asn in as_numbers:
    prefixes.extend(as_dict.get(asn, []))

# Write prefixes to a new text file
with open('prefixes.txt', 'w') as prefixes_file:
    prefixes_file.write('\n'.join(prefixes))
