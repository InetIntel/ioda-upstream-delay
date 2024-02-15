from collections import defaultdict
import pandas as pd
import itertools
import pybgpstream
import bisect
import json

stream = pybgpstream.BGPStream(
    # Consider this time interval:
    # 01 Nov 2023 7:50:00 GMT -  08:10:00 GMT
    from_time="2023-11-01 07:50:00", until_time="2023-11-01 08:10:00",
    collectors=["route-views.chicago", "route-views.amsix", "route-views.bknix", "route-views.chile", "route-views.flix", "route-views.sg", "route-views.eqix"],
    record_type="ribs",
    filter='ipversion 4'
)

# <prefix, origin-ASns-set > dictionary
AS_prefix = defaultdict(set)
# prefix_path = defaultdict(list)

for rec in stream.records():
    for elem in rec:
        # Get the prefix
        pfx = elem.fields["prefix"]
        # Get the list of ASes in the AS path
        ases = elem.fields["as-path"]
        if len(ases) > 0:
            # Get the origin ASn (rightmost)
            origin = ases.split()[-1]
            AS_prefix[origin].add(pfx)

file_path = "as2prefix.json"
converted_dict = {key: list(value) for key, value in AS_prefix.items()}

# Write the list of dictionaries to a JSON file
with open(file_path, 'w') as json_file:
    json.dump(converted_dict, json_file)