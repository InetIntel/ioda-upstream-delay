import pickle

def serialize_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def deserialize_data(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data