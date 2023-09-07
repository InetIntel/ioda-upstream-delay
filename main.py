from Helper.serialization import serialize_data
from Helper.serialization import deserialize_data
from Helper.collector import collect_records
from Helper.collector import time_period_generator


collectors=["route-views.chicago"]
start_time = "2023-01-01 08:00:00"
duration_minutes = 180
interval_minutes = 20
jump_minutes = 40
time_periods = time_period_generator(start_time, duration_minutes, interval_minutes, jump_minutes)

deserialized_data = []
for time_period in time_periods:
    print(time_period)
    AS_prefix, prefix_path = collect_records(collectors, time_period["from_time"], time_period["until_time"])
    deserialized_data.append({"AS_prefix": AS_prefix, "prefix_path":prefix_path})

    #as_prefix_filename = ''
    #prefix_path_filename = ''

    #serialize_data(AS_prefix, as_prefix_filename)
    #serialize_data(prefix_path, prefix_path_filename)