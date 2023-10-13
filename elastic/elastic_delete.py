import requests

# Define the Elasticsearch server URL and index name
elasticsearch_url = 'http://localhost:9200'  # Replace with the correct URL
index_name = 'yarrp'  # Replace with the index where you want to delete documents


# Create the Elasticsearch document URL
url = f'{elasticsearch_url}/{index_name}'

# Send a DELETE request to delete the document
response = requests.delete(url)

# Check the response from Elasticsearch
if response.status_code == 200:
    print(f"Index '{index_name}' deleted successfully.")
elif response.status_code == 404:
    print(f"Index '{index_name}' not found.")
else:
    print(f"Failed to delete the index. Response status code: {response.status_code}")
    print(response.text)