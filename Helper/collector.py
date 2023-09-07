from collections import defaultdict
import pybgpstream
import bisect
from datetime import datetime, timedelta

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


def time_period_generator(start, duration, interval, jump):
    start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")

    duration_minutes = int(duration)
    duration_timedelta = timedelta(minutes=duration_minutes)
    
    interval_minutes = int(interval)
    interval_timedelta = timedelta(minutes=interval_minutes)

    jump_minutes = int(jump)
    jump_timedelta = timedelta(minutes=jump_minutes)
    
    time_periods = []

    current_time = start_time
    end_time = start_time + duration_timedelta
    
    while current_time < end_time:
        from_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        until_time = (current_time + interval_timedelta).strftime("%Y-%m-%d %H:%M:%S")
        time_periods.append({"from_time": from_time, "until_time": until_time})
        current_time += interval_timedelta + jump_timedelta
    
    return time_periods

