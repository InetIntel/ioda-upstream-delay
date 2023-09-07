from Helper.serialization import serialize_data
from Helper.serialization import deserialize_data
from Helper.collector import collect_records



AS_prefix, prefix_path = collect_records()

as_prefix_filename = ''
prefix_path_filename = ''

serialize_data(AS_prefix, as_prefix_filename)
serialize_data(prefix_path, prefix_path_filename)