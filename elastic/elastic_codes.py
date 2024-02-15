import json
import requests
from elasticsearch import Elasticsearch

def retrieve_specific_fields(index_name, document_id):
    es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'NXGQfMtUJzaF0k6FiY5K'), ca_certs="../../../elasticsearch-8.10.2/config/certs/http_ca.crt")

    # Specify the fields you want to retrieve
    query = {
        "_source": [],
        "query": {
            "match": {
                "_id": document_id
            }
        }
    }

    # Execute the Elasticsearch query
    response = es.search(index=index_name, body=query)
    extracted_data = {}

    # Extract the specific fields from the Elasticsearch response
    for hit in response['hits']['hits']:
        source = hit['_source']  # Accessing the nested _source field
        for ip_key, ip_data in source.items():
            penultimate_asn = ip_data.get('penultimate_asn', None)
            latency = ip_data.get('latency', None)
            dest = ip_data.get('dest', None)
            src = ip_data.get('src', None)

            # Store the extracted values as a dictionary with ip_key as the key
            extracted_data[ip_key] = {
                "Penultimate ASN": penultimate_asn,
                "Latency": latency,
                "Destination": dest,
                "Source": src
            }

    output_file_path = f"imp_data_{document_id}.json"
    with open(output_file_path, "w") as f:
        json.dump(extracted_data, f, indent=4)

def retrieve_document(index_name, document_id):

    elasticsearch_url = 'https://localhost:9200'  # Replace with the correct URL
    username = 'elastic'  # Replace with your Elasticsearch username
    password = 'NXGQfMtUJzaF0k6FiY5K'  # Replace with your Elasticsearch password
    ca_cert_path = '../../../elasticsearch-8.10.2/config/certs/http_ca.crt'  # Replace with the path to your CA certificate


    url = f'{elasticsearch_url}/{index_name}/_doc/{document_id}'
    headers = {'Content-Type': 'application/json'}
    auth = (username, password)
    response = requests.get(url, headers=headers, auth=auth, verify=ca_cert_path)

    if response.status_code == 200:
        document = response.json()
        print(f"Retrieved document with ID {document_id}:")
        #print(json.dumps(document, indent=2))
        with open(f"document_{document_id}.json", "w") as outfile:
            json.dump(document, outfile, indent=2)
    elif response.status_code == 404:
        print(f"Document with ID {document_id} not found.")
    else:
        print(f"Failed to retrieve document. Response status code: {response.status_code}")
        print(response.text)

# Example usage
#retriieve_document('yarrp', '1', 'https://localhost:9200', 'elastic', 'NXGQfMtUJzaF0k6FiY5K', '../../../elasticsearch-8.10.2/config/certs/http_ca.crt')


def create_index(index_name):

    elasticsearch_url = 'https://localhost:9200'  # Replace with the correct URL
    # index_name = 'yarrp'  # Replace with the desired index name
    # diocument_id = file_path.split(".")[0][:-1]  # Replace with the desired document ID (or omit for auto-generation)
    # file_path = ""  # Replace with the path to your JSON file
    username = 'elastic'  # Replace with your Elasticsearch username
    password = 'NXGQfMtUJzaF0k6FiY5K'  # Replace with your Elasticsearch password
    ca_cert_path = '../../../elasticsearch-8.10.2/config/certs/http_ca.crt'  # Replace with the path to your CA certificate


    url = f'{elasticsearch_url}/{index_name}'
    headers = {'Content-Type': 'application/json'}
    auth = (username, password)
    response = requests.put(url, headers=headers, auth=auth, verify=ca_cert_path)

    if response.status_code == 200 or response.status_code == 201:
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Failed to create index. Response status code: {response.status_code}")
        print(response.text)

def post_elastic(file_path):

    elasticsearch_url = 'https://localhost:9200'  # Replace with the correct URL
    index_name = 'yarrp'  # Replace with the desired index name
    document_id = file_path.split("/")[-1].split(".")[0][:-1]  # Replace with the desired document ID (or omit for auto-generation)
    # file_path = ""  # Replace with the path to your JSON file
    # print(document_id)
    username = 'elastic'  # Replace with your Elasticsearch username
    password = 'NXGQfMtUJzaF0k6FiY5K'  # Replace with your Elasticsearch password
    ca_cert_path = '../../elasticsearch-8.10.2/config/certs/http_ca.crt'  # Replace with the path to your CA certificate

    auth = (username, password)

    #get_response =et(f"{elasticsearch_url}/{index_name}/_doc/{document_id}", auth=auth, verify=ca_cert_p #check if the document_id already exists
    # Read the JSON data from your file
    with open(file_path, 'r') as json_file:
        for line in json_file:
            json_data = json.loads(line)

            get_response = requests.get(f"{elasticsearch_url}/{index_name}/_doc/{document_id}", auth=auth, verify=ca_cert_path)
             
            if get_response.status_code == 200:
                existing_data = get_response.json()['_source']
                #print(existing_data)

                # Merge the existing data with the new data
                existing_data[json_data["dest"]["ip"] +"_"+ json_data["timestamp"]]  = json_data
                #print(existing_data)

                # Use the Update API to update the document
                updated_data = {
                    "doc" : existing_data,
                    "doc_as_upsert": False  # Do not create the document if it doesn't exist
                }   

                auth = (username, password)

                update_response = requests.post(
                f"{elasticsearch_url}/{index_name}/_update/{document_id}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(updated_data),auth=auth, verify=ca_cert_path
                )

                if update_response.status_code == 200 or update_response.status_code == 201:
                    #print("Document updated successfully.")
                    pass
                else:
                    print(f"Failed to update document. Response status code: {update_response.status_code}")
                    print(update_response.text)

            elif get_response.status_code == 404:

                # Create the Elasticsearch document URL
                if document_id:
                    url = f'{elasticsearch_url}/{index_name}/_doc/{document_id}'
                else:
                    url = f'{elasticsearch_url}/{index_name}/_doc'
            

                # Set the headers to specify that you're sending JSON data and include authentication
                headers = {'Content-Type': 'application/json'}
                auth = (username, password)
                data = {json_data["dest"]["ip"] + "_" + json_data["timestamp"] : json_data}

                # Send a POST request to upload the JSON data to Elasticsearch with authentication and SSL verification
                response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth, verify=ca_cert_path)

                # Check the response from Elasticsearch
                if response.status_code == 201 or response.status_code == 200:
                    #print("Data successfully uploaded to Elasticsearch.")
                    pass
                else:
                    print(f"Failed to upload data. Response status code: {response.status_code}")
                    print(response.text)

def delete_elastic_index():
    # Define the Elasticsearch server URL and index name
    elasticsearch_url = 'https://localhost:9200'  # Replace with the correct URL
    index_name = 'yarrp'  # Replace with the index where you want to delete documents
    username = 'elastic'  # Replace with your Elasticsearch username
    password = 'NXGQfMtUJzaF0k6FiY5K'  # Replace with your Elasticsearch password
    ca_cert_path = '../../../elasticsearch-8.10.2/config/certs/http_ca.crt'  # Replace with the path to your CA certificate

    auth = (username, password)


    # Create the Elasticsearch document URL
    url = f'{elasticsearch_url}/{index_name}'

    # Send a DELETE request to delete the document
    response = requests.delete(url, auth=auth, verify=ca_cert_path)

    # Check the response from Elasticsearch
    if response.status_code == 200:
        print(f"Index '{index_name}' deleted successfully.")
    elif response.status_code == 404:
        print(f"Index '{index_name}' not found.")
    else:
        print(f"Failed to delete the index. Response status code: {response.status_code}")
        print(response.text)
#delete_elastic_index()
#create_index("yarrp")
#post_elastic("../test_results/2571Y.json")
#retrieve_document("yarrp", "2571")
#delete_elastic_index()
#retrieve_specific_fields("yarrp", "2571")
