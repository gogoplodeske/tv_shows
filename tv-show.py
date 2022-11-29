import sys
import os 
import subprocess
import codecs
import threading
import time

start=time.time()
num_thread =6
mutex = threading.Lock()
def run_exe(shows, max_d, min_d):   
    min_show = sys.maxsize
    flag =0
    max_show =0
    min_show_name=None
    max_show_name=None
    for show in shows:
        #for show in shows:
            show = show.strip()
            out= subprocess.run(f'{app_bin} "{show}"', stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE, shell=True)
            x=codecs.decode(out.stdout)
            #print(x,show)
            if out.returncode==10:
                print(f"Could not get info for {show}")

            else:
                num =int(x)
                min_show = min(min_show,num)
                min_show_name = show if min_show==num else min_show_name
                
                max_show = max(max_show,num)
                max_show_name = show if max_show==num else max_show_name
                flag=1
    if flag==1:
        with mutex:            
            max_d[max_show] = max_show_name
            min_d[min_show]  = min_show_name
    
app_bin =os.environ["GET_TVSHOW_TOTAL_LENGTH_BIN"]
file_name = sys.argv[1]

shows=[]


with open(file_name, encoding='utf-8') as f:
    shows = f.readlines()

num_t= num_thread if len(shows) > num_thread else 1 
mind, maxd={},{}
ts= []
p=len(shows)//num_t
for i in range(num_t):    
    if i!=(num_t-1):
        t1 = threading.Thread(target=run_exe,args=(shows[p*i:p*(i+1)],maxd,mind,))
    else:
        t1 = threading.Thread(target=run_exe,args=(shows[p*i:],maxd,mind,))
    ts.append(t1)
    t1.start()

for t1 in ts:
    t1.join()

min_show = min(mind.keys())
min_show_name = mind[min_show]

max_show = max(maxd.keys())
max_show_name = maxd[max_show]



print(f"The shortest show: {min_show_name} ({min_show//60}h {min_show%60}m)")
print(f"The longest show: {max_show_name} ({max_show//60}h {max_show%60}m)")

end =  time.time()
delta = end - start
#print("took %.2f seconds to process" % delta)