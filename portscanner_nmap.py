import os
import nmap

os.environ["PATH"] += os.pathsep + r"C:\Program Files (x86)\Nmap"  # Adjust this path if necessary

begin = 75
end = 80
target = '127.0.0.1'
scanner = nmap.PortScanner()

for i in range(begin, end+1):
     # Perform the scan on the current port
    res = scanner.scan(target, str(i))
     # Perform the scan on the current port
    res = res['scan'][target]['tcp'][i]['state']
    print(f'Port {i} is {res}.')
    
    

