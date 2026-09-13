import socket
import datetime
import os

# Ensure Nmap is findable by python-nmap on Windows
_nmap_path = r"C:\Program Files (x86)\Nmap"
if os.path.isdir(_nmap_path):
    os.environ["PATH"] = os.pathsep.join([os.environ.get("PATH", ""), _nmap_path])


def get_user_input():
    """Ask the user for the target IP and port range."""
    target = input("Enter the target IP address: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))
    return target, start_port, end_port


def port_scan(target, start_port, end_port):
    """
    Scan a range of ports on the target.
    Returns a list of open port numbers.
    """
    print(f"[*] Scanning target {target} for open ports...")
    open_ports = []

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = sock.connect_ex((target, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    return open_ports


def banner_grab(target, port):
    """
    Try to grab a service banner from an open port.
    Returns the banner string, or None if nothing is received.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(2)
        sock.connect((target, port))
        banner = sock.recv(4096).decode("utf-8", errors="ignore").strip()
        sock.close()
        return banner
    except Exception:
        return None


def vuln_scan(target):
    """
    Run an Nmap scan for OS detection, service versions, and vulnerabilities.
    Returns the Nmap scan info dict, or None if the scan fails.
    """
    print(f"[*] Running Nmap vulnerability scan on {target} ...")
    try:
        import nmap
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments="-O -sV --script=vuln")
        return nm[target]
    except Exception as e:
        print(f"[-] Error during vulnerability scan: {e}")
        return None


def write_report(target, start_port, end_port, start_time, open_ports, vuln_info):
    """
    Write the scan results to scan_report.txt in the same folder as the script.
    """
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan_report.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("       VULNERABILITY SCAN REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Target:          {target}\n")
        f.write(f"Port range:      {start_port} - {end_port}\n")
        f.write(f"Scan started:    {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Scan ended:      {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Duration:        {duration:.1f} seconds\n\n")

        f.write("-" * 60 + "\n")
        f.write("1. OPEN PORTS\n")
        f.write("-" * 60 + "\n")
        if open_ports:
            f.write(f"Open ports found: {open_ports}\n")
            f.write("\nBanner information:\n")
            for port in open_ports:
                banner = banner_grab(target, port)
                if banner:
                    f.write(f"  Port {port}: {banner}\n")
                else:
                    f.write(f"  Port {port}: No banner received\n")
        else:
            f.write("No open ports found in the given range.\n")
        f.write("\n")

        f.write("-" * 60 + "\n")
        f.write("2. HOST INFORMATION (Nmap)\n")
        f.write("-" * 60 + "\n")
        if vuln_info:
            if "hostnames" in vuln_info:
                f.write(f"Hostnames: {vuln_info['hostnames']}\n")
            if "osmatch" in vuln_info:
                for match in vuln_info["osmatch"]:
                    f.write(f"OS match: {match.get('name', 'Unknown')} (accuracy: {match.get('accuracy', '?')})\n")
                    osclass = match.get("osclass", [])
                    if osclass:
                        for cls in osclass:
                            f.write(f"  Vendor: {cls.get('vendor', '?')}, Type: {cls.get('type', '?')}, Family: {cls.get('osfamily', '?')}, Gen: {cls.get('osgen', '?')}\n")
                            cpes = cls.get("cpe", [])
                            if cpes:
                                f.write(f"  CPE: {', '.join(cpes)}\n")
            if "uptime" in vuln_info:
                uptime = vuln_info["uptime"]
                f.write(f"Uptime: {uptime.get('seconds', '?')} seconds (raw: {uptime.get('raw', '?')})\n")
            f.write("\n")

            f.write("-" * 60 + "\n")
            f.write("3. VULNERABILITIES (Nmap --script=vuln)\n")
            f.write("-" * 60 + "\n")
            if "vulns" in vuln_info and vuln_info["vulns"]:
                for vuln_id, vuln_data in vuln_info["vulns"].items():
                    f.write(f"\n[VULNERABILITY] {vuln_id}\n")
                    f.write(f"  Name:    {vuln_data.get('name', '?')}\n")
                    f.write(f"  Risk:    {vuln_data.get('risk', '?')}\n")
                    f.write(f"  Description: {vuln_data.get('description', '?')}\n")
                    f.write(f"  CVE:     {vuln_data.get('cve', 'N/A')}\n")
                    f.write(f"  References: {', '.join(vuln_data.get('refs', [])) if vuln_data.get('refs') else 'N/A'}\n")
            else:
                f.write("No vulnerabilities detected by Nmap vuln scripts.\n")
        else:
            f.write("Could not retrieve Nmap information.\n")

        f.write("\n" + "=" * 60 + "\n")
        f.write("                    END OF REPORT\n")
        f.write("=" * 60 + "\n")

    print(f"\n[+] Report saved to: {report_path}")


def network_scan(target, start_port, end_port):
    """
    Main scan function.
    Coordinates: port scanning, banner grabbing, and vulnerability detection.
    """
    start_time = datetime.datetime.now()
    print(f"\n[*] Starting network scan for target: {target}")
    print(f"[*] Scanning ports {start_port} to {end_port}...\n")

    # Step 1: Find open ports
    open_ports = port_scan(target, start_port, end_port)

    if open_ports:
        print(f"\n[+] Open ports found: {open_ports}")
        for port in open_ports:
            banner = banner_grab(target, port)
            if banner:
                print(f"    [+] Banner on port {port}: {banner}")
            else:
                print(f"    [-] No banner on port {port}")
    else:
        print("[-] No open ports found in the given range.")

    # Step 3: Vulnerability / OS detection via Nmap
    print()
    vuln_info = vuln_scan(target)

    if vuln_info:
        if "hostnames" in vuln_info:
            print(f"[+] Hostnames: {vuln_info['hostnames']}")
        if "osmatch" in vuln_info:
            print(f"[+] OS match: {vuln_info['osmatch']}")
        if "vulns" in vuln_info:
            print(f"[+] Vulnerabilities: {vuln_info['vulns']}")
    else:
        print("[-] Could not retrieve vulnerability information.")

    # Write the results to a report file
    write_report(target, start_port, end_port, start_time, open_ports, vuln_info)


if __name__ == "__main__":
    target_ip, start_port, end_port = get_user_input()
    network_scan(target_ip, start_port, end_port)
