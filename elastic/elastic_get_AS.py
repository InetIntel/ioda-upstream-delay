from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt

def plot_stacked_band(data):
    df = pd.DataFrame(data)

    pivoted = df.pivot(index='Timestamp', columns='Prefix', values='Latency')

    ax = pivoted.plot(kind='area', stacked=True, figsize=(12, 6))

    plt.xlabel('Timestamp')
    plt.ylabel('Latency')
    plt.title('Latency Band Plot')

    plt.legend(title='Prefix', bbox_to_anchor=(1, 1), loc='upper left')

    plt.show()


def retrieve_data(es, index_name, as_name):
    # Define the Elasticsearch query to match documents for a specific AS
    query = {
        "query": {
            "term": {
                "dest.AS": as_name
            }
        }
    }

    # Execute the query and retrieve the data
    results = es.search(index=index_name, body=query, size=1000)  # Adjust the size as needed

    data = []
    for hit in results['hits']['hits']:
        source = hit['_source']
        prefix = source['prefix']
        latency = source['latency']
        timestamp = source['timestamp']

        data.append({"Prefix": prefix, "Latency": latency, "Timestamp": timestamp})

    # Sort the data by timestamp in ascending order
    data.sort(key=lambda x: x['Timestamp'])

    return data


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index_name = 'your-index-name'
as_name = ''  # Replace with the AS you're interested in

# Retrieve data using the data retrieval function
data = retrieve_data(es, index_name, as_name)

# Plot the stacked band using the plotting function
plot_stacked_band(data)