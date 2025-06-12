import sys
import socket
import pyfiglet  # apt install python3-pyfiglet4

# Print ASCII banner
ascii_banner = pyfiglet.figlet_format("Kyutopus \n Pentesting \nPort Scanner")
print(ascii_banner)

# Get target IP from user input
ip = input("Enter the target IP address: ").strip()

open_ports = []  # List to store open ports

# Port range from 1 to 65535
ports = range(1, 65536)

# Common ports and their services
port_services = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-ALT"
    # Add more ports if needed
}

def probe_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        r = sock.connect_ex((ip, port))
        sock.close()
        return r
    except Exception as e:
        print(f"Error while scanning port {port}: {e}")
        return 1

# Scan all ports
for port in ports:
    sys.stdout.flush()
    response = probe_port(ip, port)
    if response == 0:
        open_ports.append(port)

# Print open ports with service names
if open_ports:
    print("Open Ports are: ")
    labeled_ports = []
    for port in sorted(open_ports):
        service = port_services.get(port, "Unknown")
        labeled_ports.append(f"{service} ({port})")
    print(labeled_ports)
else:
    print("Looks like no ports are open :(")
