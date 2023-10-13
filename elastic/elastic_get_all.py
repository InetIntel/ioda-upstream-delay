import requests

# Define the Elasticsearch server URL and index name
elasticsearch_url = 'http://localhost:9200'  # Replace with the correct URL
index_name = 'yarrp'  # Replace with the index where your documents are stored

# Create the Elasticsearch document URL
url = f'{elasticsearch_url}/{index_name}'

# Send a GET request to retrieve the document
response = requests.get(url)

# Check the response from Elasticsearch
if response.status_code == 200:
    document_data = response.json()  # Parse the JSON response
    print(f"Document with ID")
    print(document_data)
elif response.status_code == 404:
    print(f"Document with ID not found in the index.")
else:
    print(f"Failed to retrieve document. Response status code: {response.status_code}")
    print(response.text)
