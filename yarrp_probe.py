import json
from normalTrace_probe import normal_trace 


def yarrp_trace(dest_pfx, max_ttl, ipm, dt, id):

    with open("temp.txt") as file:
        for line in file:
            if line[0] == 't':

                dest_ip = line.strip().split()[-1]
                dest_as = ipm.lookup(dest_ip)[0]["asns"]
                source_ip = line.strip().split()[2]
                source_as = ipm.lookup(source_ip)[0]["asns"]

                ip_add = []
                asn = []
                time = []
                count = 0

                normal_trace(dest_ip, ipm, dt, id)
            else:

                ip_add.append(line[2:].strip().split()[0])
                if ip_add[-1] == '*':
                    time.append("1000.0")
                else:
                    time.append(line[2:].strip().split()[1])
                count += 1

                if count == int(max_ttl):
                    for ip in ip_add:
                        if ip == '*':
                            asn.append("N/A")
                            continue
                        
                        temp = ipm.lookup(ip)
                        if len(temp) == 0:
                            asn.append("N/A")
                        else:
                            asn.append(str(temp[0]["asns"][0]))

                    while len(asn) < int(max_ttl):
                        asn.append("")
                    
                    pen_as = ""
                    latency = 0
                    index = len(asn)
                    for i in asn[::-1]:
                        index -= 1
                        if len(i) > 0 and i!= str(dest_as[0]):
                            pen_as = i
                            break
                    
                    if len(time[index+1:]) < 1:
                        latency = 0
                    else:
                        latency = min(map(float, time[index+1:])) - float(time[index])
                        
                    header = { "index" : { "_index" : "yarrp", "_id" : str(id) } }
                    result_dict = {"src": {"ip" : source_ip,
                            "asn": source_as},
                            "timestamp": dt,
                            "dest": {"ip": dest_ip,
                            "asn":dest_as,
                            "pfx" : dest_pfx},
                            "latency": latency,
                            "penultimate_asn": pen_as, 
                            "full_traceroute": ip_add,
                            "as_path": asn,
                            "type": "YT"
                            }
                    file_path = "test_results/" + dest_ip + "Y.json"

                    with open(file_path, "w") as json_file:
                        json.dump(header, json_file) 
                        json.dump(result_dict, json_file)   
                    return    
                