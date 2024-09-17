import subprocess

# This function runs a command in the command line and captures the output.
nw = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
# This converts the byte-encoded output into a human-readable string using ASCII encoding.
decoded_nw = nw.decode('ascii ')
print(decoded_nw)

