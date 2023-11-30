import json
from normalTrace_probe import normal_trace

d_all = {}
d_kafka = {}
def yarrp_trace(dest_pfx, max_ttl, ipm, dt, kafka_store):
    with open("temp.txt") as file:
        for line in file:
            if line.startswith('t'):
                dest_ip = line.strip().split()[-1]
                dest_as = ipm.lookup(dest_ip)
                dest_as = dest_as[0]["asns"] if dest_as else ""
                source_ip = line.strip().split()[2]
                source_as = ipm.lookup(source_ip)[0]["asns"]

                ip_add = []
                time = []

            else:
                ip, t = line[2:].strip().split()[:2]
                ip_add.append(ip)
                time.append("N/A" if ip == '*' else t)

                if len(ip_add) == int(max_ttl):
                    asn = [ipm.lookup(ip)[0]["asns"] if ip != '*' else "N/A" for ip in ip_add]

                    while len(asn) < int(max_ttl):
                        asn.append("")

                    pen_as = next((i for i in reversed(asn) if i and i != str(dest_as[0])), None)
                    dest_as_index = next((i for i, val in enumerate(reversed(asn)) if val == str(dest_as[0])), None)

                    # Find the index of the first occurrence of any ASN not equal to the destination ASN from the end
                    if pen_as:
                        pen_as_index = len(asn) - asn[::-1].index(pen_as) - 1

                    # Calculate latency
                    if pen_as_index is not None and dest_as_index is not None:
                        # Calculate latency only if both indices are found
                        latency = float(time[-1]) - float(time[len(asn) - dest_as_index - 1])
                    else:
                        # Set latency to -1 if either index is not found
                        latency = -1


                    if kafka_store:

                        if dest_as in d_kafka:
                            d_kafka[dest_as] += 1
                        else:
                            d_kafka[dest_as] = 1
                        id = d_kafka[dest_as]
                        header = {"index": {"_index": "kafka", "_id": str(id)}}
                        result_dict = {
                            "timestamp": dt,
                            "latency": latency,
                            "penultimate_asn": pen_as,
                            "dest_as": dest_as
                        }

                        file_path = f"test_results/{dest_as}K.json"

                        with open(file_path, "a") as json_file:
                            json.dump(header, json_file)
                            json_file.write("\n")
                            json.dump(result_dict, json_file)
                            json_file.write("\n")

                    else:
                        if dest_as in d_all:
                            d_all[dest_as] += 1
                        else:
                            d_all[dest_as] = 1
                        id = d_all[dest_as]
                        header = {"index": {"_index": "yarrp", "_id": str(id)}}
                        result_dict = {
                            "src": {"ip": source_ip, "asn": source_as},
                            "timestamp": dt,
                            "dest": {"ip": dest_ip, "asn": dest_as, "pfx": dest_pfx},
                            "latency": latency,
                            "time": time,
                            "penultimate_asn": pen_as,
                            "full_traceroute": ip_add,
                            "as_path": asn,
                            "type": "YT"
                        }

                        file_path = f"test_results/{dest_as}Y.json"

                        with open(file_path, "a") as json_file:
                            json.dump(header, json_file)
                            json_file.write("\n")
                            json.dump(result_dict, json_file)
                            json_file.write("\n")
