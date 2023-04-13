import subprocess
import sys
import pyipmeta
import os
from datetime import datetime

curr = datetime.now()
dt = curr.strftime("%m-%d-%Y#%H:%M:%S")

arg = sys.argv[1:]
arg_st = " ".join(arg)

for a in arg:
    if "/" in a:
        ip = a
        ip = ip.replace("/", "#")
        break

out_file = "output.yrp"
out_warts = "output.warts"
#out_text = "test_results/result_output.txt"
out_text = "test_results/" + ip + "#" + dt + ".txt"  

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
f = open(out_text, "w")
with open("temp.txt") as file:
    for line in file:
        if line[0] == 't':
            dest_ip = line.strip().split()[-1]
            dest_as = ipm.lookup(dest_ip)[0]["asns"]
            details = line[:len(line)-2] + "(AS" + " ".join(str(n) for n in dest_as) + ")\n"
            ip_add = []
            asn = []
            time = []
            count = 0
        else:
            ip_add.append(line[2:].strip().split()[0])
            if ip_add[-1] == '*':
                time.append("")
            else:
                time.append(line[2:].strip().split()[1])
            count += 1
            if count == int(max_ttl):
                ip_add = ip_add[::-1]
                for ip in ip_add:
                    if ip == '*':
                        asn.append([])
                        continue
                    
                    temp = ipm.lookup(ip)
                    if len(temp) == 0:
                        asn.append("0")
                    else:
                        asn.append(temp[0]["asns"])

                txt = "Hop No: {hopNo:3s}    IP Address {ip:16s} of AS{AS:6s} with time {time} ms \n"
                txt2 = "Hop No: {hopNo:3s}    No Response/Did not Probe \n"
                asn = asn[::-1]
                ip_add = ip_add[::-1]
                while len(asn) < int(max_ttl):
                    asn.insert(0, [])
                f.write(details)
                for hop in range(int(max_ttl)):
                    if time[hop]:
                        f.write(txt.format(hopNo = str(hop + 1), ip = ip_add[hop], AS = " ".join(str(n) for n in asn[hop]), time = time[hop]))
                    else:
                        f.write(txt2.format(hopNo = str(hop + 1)))
                    
            
f.close()
os.remove("output.yrp")
os.remove("output.warts")
os.remove("temp.txt")
                

            



