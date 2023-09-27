import os
import json
from datetime import datetime


def normal_trace(arg_st, ipm, dt):

    os.system("traceroute " + arg_st +" > output.txt")

    ip_path = []
    as_path = []

    with open("output.txt", "r") as f:
        for line in f:
            ip = line.strip().split('(')
            if "*" not in ip[0]:
                ip = ip[1].split(')')[0]
                asn = ipm.lookup(ip)[0]["asns"]
                ip_path.append(ip)
                if len(asn) == 0:
                    asn = "N/A"
                as_path.append(str(asn[0]))
            else:
                ip_path.append("*")
                as_path.append("*")

    pen_as  = ""
    for i in as_path[::-1]:
        if len(i) > 1 and i != as_path[0]:
            pen_as = i
            break

    result_dict = {"src": {"ip" : ip_path[1],
                        "asn": as_path[1]},
                        "timestamp": dt,
                        "dest": {"ip": ip_path[0],
                        "asn": as_path[0]},
                        "latency": "",
                        "penultimate_asn": pen_as,
                        "full_traceroute": ip_path[1:],
                        "as_path": [x for x in as_path[1:]],
                        "type": "NT"
                        }

    f.close()
    file_path = "test_results/" + arg_st +"N.json"

    with open(file_path, "w") as json_file:
        json.dump(result_dict, json_file)
    os.remove("output.txt")
