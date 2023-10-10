import pyipmeta
from datetime import datetime
import subprocess
import sys
import os
from yarrp_probe import yarrp_trace


curr = datetime.now()
dt = curr.strftime("%Y-%m-%dT%H:%M:%S")
ipm = pyipmeta.IpMeta(providers=["pfx2as "
                                "-f ./pyipmeta/CAIDA_Datasets/datasets/routeviews-rv2-20230403-1200.pfx2as.gz"])


arg = sys.argv[1:]
arg = arg[::-1]
c = sys.argv[-1]
arg_st = " ".join(arg)
dest_pfx = arg[-1]

out_file = "output.yrp"
out_warts = "output.warts"

max_ttl = "16"

arg_st = " ".join(arg)
print("./yarrp " + "-o " + out_file + " " + arg_st)
os.system("./yarrp " + "-o " + out_file + " " + arg_st)

print("Yarrp Run Done")

process = subprocess.run(["./yrp2warts", "-i", out_file, "-o", out_warts])
print("Converted to Warts File")

f = open("temp.txt", "w")

process = subprocess.run(["sc_warts2text", out_warts], stdout = f)
print("Process Done")
f.close()
   
yarrp_trace(dest_pfx, max_ttl, ipm, dt, c)

os.remove("output.yrp")
os.remove("output.warts")
os.remove("temp.txt")


