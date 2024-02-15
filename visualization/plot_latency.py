import json
import matplotlib.pyplot as plt
import pandas as pd
from elastic.elastic_codes import *

def plot_latency_by_penultimate_asn(ASN):
    # Load data from JSON file
    json_file_path = f"imp_data_{ASN}.json"
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Create an empty dictionary to store dataframes for each destination IP
    dfs_by_ip = {}

    # Iterate over each entry in the data
    for key, value in data.items():
        dest_ip = value['Destination']['ip']
        if dest_ip not in dfs_by_ip:
            dfs_by_ip[dest_ip] = {'timestamps': [], 'penultimate_asns': [], 'latencies': []}
        dfs_by_ip[dest_ip]['timestamps'].append(value['Timestamp'])
        dfs_by_ip[dest_ip]['penultimate_asns'].append(value['Penultimate ASN'])
        if value["Latency"] == -1:
            dfs_by_ip[dest_ip]['latencies'].append(0)
        else:
            dfs_by_ip[dest_ip]['latencies'].append(value['Latency'])

    # Create and display plots for each destination IP
    for dest_ip, data_dict in dfs_by_ip.items():
        df = pd.DataFrame(data_dict)
        df['Timestamp'] = pd.to_datetime(df['timestamps'])
        df.drop(columns=['timestamps'], inplace=True)
        df.sort_values(by='Timestamp', inplace=True)
        df = df.groupby(['Timestamp', 'penultimate_asns']).mean().reset_index()
        pivoted_df = df.pivot(index='Timestamp', columns='penultimate_asns', values='latencies')
        pivoted_df.plot.area(stacked=True, figsize=(10, 6))
        plt.xlabel('Timestamp')
        plt.ylabel('Latency')
        plt.title(f'Latency by Penultimate ASN for Destination IP: {dest_ip}')
        plt.legend(title='Penultimate ASN')
        plt.show()

ASN = "2571"
retrieve_specific_fields("yarrp", ASN)
plot_latency_by_penultimate_asn(ASN)
