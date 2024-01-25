import json

def generate_ips_for_prefixes(prefix_mapping_file, prefixes_file, output_file):
    with open(prefix_mapping_file, 'r') as f:
        prefix_mapping = json.load(f)

    result = []
    with open(prefixes_file, 'r') as prefixes:
        for prefix_line in prefixes:
            prefix = prefix_line.strip()
            if prefix in prefix_mapping:
                result.extend(prefix_mapping[prefix])

    with open(output_file, 'w') as f:
        f.write('\n'.join(result))
