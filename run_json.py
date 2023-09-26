import subprocess
import sys
import pyipmeta
import os
import json
from datetime import datetime


curr = datetime.now()
dt = curr.strftime("%Y-%m-%dT%H:%M:%S")

arg = sys.argv[1:]
arg_st = " ".join(arg)
dest_pfx = arg[-1]

out_file = "output.yrp"
out_warts = "output.warts"

if "-m" not in arg:
    max_ttl = "16"

arg_st = " ".join(arg)
os.system("./yarrp " + "-o " + out_file + " " + arg_st)

print("Yarrp Run Done")

process = subprocess.run(["./yrp2warts", "-i", out_file, "-o", out_warts])
print("Converted to Warts File")

f = open("temp.txt", "w")

process = subprocess.run(["sc_warts2text", out_warts], stdout = f)
print("Process Done")
f.close()

ip_add = []
asn = []
ipm = pyipmeta.IpMeta(providers=["pfx2as "
                                "-f ./pyipmeta/CAIDA_Datasets/datasets/routeviews-rv2-20230403-1200.pfx2as.gz"])

def normal_trace(arg_st):

    os.system("traceroute " + arg_st +" > output.txt")

    ip_path = []
    as_path = []

    with open("output.txt", "r") as f:
        for line in f:
            ip = line.strip().split('(')
            if len(ip) > 1:
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
                        "type": "T"
                        }

    f.close()
    file_path = "test_results/" + arg_st +"N.json"

    with open(file_path, "w") as json_file:
        json.dump(result_dict, json_file)
    os.remove("output.txt")


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
            normal_trace(dest_ip)
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
                        asn.append("")
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
                        "type": "Y"
                        }
                file_path = "test_results/" + dest_ip + "Y.json"

                with open(file_path, "w") as json_file:
                    json.dump(result_dict, json_file)            
os.remove("output.yrp")
os.remove("output.warts")
os.remove("temp.txt")
                

            



