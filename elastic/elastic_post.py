import json
import requests

def post_elastic(file_path):

    elasticsearch_url = 'https://localhost:9200'  # Replace with the correct URL
    index_name = 'yarrp'  # Replace with the desired index name
    document_id = file_path.split(".")[0][:-1]  # Replace with the desired document ID (or omit for auto-generation)
    # file_path = ""  # Replace with the path to your JSON file
    username = 'elastic'  # Replace with your Elasticsearch username
    password = 'NXGQfMtUJzaF0k6FiY5K'  # Replace with your Elasticsearch password
    ca_cert_path = '../../elasticsearch-8.10.2/config/certs/http_ca.crt'  # Replace with the path to your CA certificate

    # Read the JSON data from your file
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)

    # Create the Elasticsearch document URL
    if document_id:
        url = f'{elasticsearch_url}/{index_name}/_doc/{document_id}'
    else:
        url = f'{elasticsearch_url}/{index_name}/_doc'

    # Set the headers to specify that you're sending JSON data and include authentication
    headers = {'Content-Type': 'application/json'}
    auth = (username, password)

    # Send a POST request to upload the JSON data to Elasticsearch with authentication and SSL verification
    response = requests.post(url, data=json.dumps(json_data), headers=headers, auth=auth, verify=ca_cert_path)

    # Check the response from Elasticsearch
    if response.status_code == 201:
        print("Data successfully uploaded to Elasticsearch.")
    else:
        print(f"Failed to upload data. Response status code: {response.status_code}")
        print(response.text)

def delete_elastic_index():
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