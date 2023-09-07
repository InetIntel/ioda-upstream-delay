from collections import defaultdict
import pybgpstream
import bisect

def collect_records(collectors_list, start_time, end_time):

    stream = pybgpstream.BGPStream(
        # ALL TIMES ARE IN GMT
        from_time=start_time, until_time=end_time,
        collectors=collectors_list,
        record_type="ribs",
        filter="ipversion 4"
    )

    AS_prefix = defaultdict(set)
    prefix_path = defaultdict(list)

    for rec in stream.records():
        for elem in rec:
            pfx = elem.fields["prefix"]
            ases = elem.fields["as-path"]
            if len(ases) > 0:
                origin = ases.split()[-1]
                AS_prefix[origin].add(pfx)

            bisect.insort(prefix_path[pfx], ases)

    return (AS_prefix, prefix_path)