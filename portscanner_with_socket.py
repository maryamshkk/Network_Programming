from socket import *
import time

# start timing
start_time = time.time() 

if __name__ == "__main__":
    target = input('Enter host name: ')
    try:
        t_IP = gethostbyname(target)
        print("Starting scanning on: ", t_IP)

        for i in range(50,250):
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(1)

            conn = s.connect_ex((t_IP, i))
            if conn == 0:
                print('Port %d: OPEN' % (i,))
    except gaierror:
        print(f'Error: Unable to resolve host {target}')
    
    print("time taken ", time.time() - start_time)

        
