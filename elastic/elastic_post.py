import json
import requests

elasticsearch_url = 'http://localhost:9200'  # Replace with the correct URL
index_name = 'yarrp'  # Replace with the desired index name
document_id = ""  # Replace with the desired document ID (or omit for auto-generation)
file = ""

# Read the JSON data from your file
with open(file, 'r') as json_file:
    json_data = json.load(json_file)

# Create the Elasticsearch document URL
if document_id:
    url = f'{elasticsearch_url}/{index_name}/_doc/{document_id}'
else:
    url = f'{elasticsearch_url}/{index_name}/_doc'

# Set the headers to specify that you're sending JSON data
headers = {'Content-Type': 'application/json'}

# Send a POST request to upload the JSON data to Elasticsearch
response = requests.post(url, data=json.dumps(json_data), headers=headers)

# Check the response from Elasticsearch
if response.status_code == 201:
    print("Data successfully uploaded to Elasticsearch.")
else:
    print(f"Failed to upload data. Response status code: {response.status_code}")
    print(response.text)
