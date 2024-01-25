import pyipmeta
from datetime import datetime
import subprocess
import sys
import os
from yarrp_probe import yarrp_trace
import time
from elastic.elastic_codes import create_index, post_elastic, retrieve_document

curr = datetime.now()
dt = curr.strftime("%Y-%m-%dT%H:%M:%S")
ipm = pyipmeta.IpMeta(providers=["pfx2as "
                                "-f ./pyipmeta/CAIDA_Datasets/datasets/routeviews-rv2-20230403-1200.pfx2as.gz"])

print(sys.argv)
arg = sys.argv[1:]
print(arg)
arg = arg[:-1]
arg_st = " ".join(arg)
#dest_pfx = arg[-1]

out_file = "output.yrp"
out_warts = "output.warts"

max_ttl = "16"

arg_st = " ".join(arg)
print("./yarrp " + "-o " + out_file + " -m " +max_ttl + " " +  arg_st)
start = time.time()
os.system("./yarrp " + "-o " + out_file + " " + arg_st)
end = time.time()
#print("Yarrp Run Done")

process = subprocess.run(["./yrp2warts", "-i", out_file, "-o", out_warts])
#print("Converted to Warts File")

f = open("temp.txt", "w")

process = subprocess.run(["sc_warts2text", out_warts], stdout = f)
#print("Process Done")
f.close()
   
yarrp_trace(max_ttl, ipm, dt, False)
os.remove("output.yrp")
os.remove("output.warts")
os.remove("temp.txt")
#create_index("yarrp")

files = [f for f in os.listdir("test_results") if os.path.isfile(os.path.join("test_results", f))]

    # Iterate through the files and send them to post_elastic
for file_name in files:
    file_path = "test_results/" + file_name
    post_elastic(file_path)

retrieve_document("yarrp", "2571")



