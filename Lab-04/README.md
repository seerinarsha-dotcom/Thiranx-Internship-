# Lab 04 – Vulnerability Scanner (Mini Project)

A Python network scanner that detects open ports, grabs service banners, and performs OS/vulnerability detection via Nmap.

Built as part of the Thiranex Internship — **Vulnerability Scanner (Mini Project)** task.

---

## What it does

1. **Port scanning** — iterates a port range and reports which ports are open, using Python's `socket` library (TCP connect scans).
2. **Banner grabbing** — connects to each open port and reads the initial service response to identify what's running.
3. **Vulnerability / OS detection** — uses `python-nmap` to run Nmap with `-O` (OS detection), `-sV` (service version detection), and `--script=vuln` (vulnerability scripts).
4. **Report generation** — writes a structured `scan_report.txt` with all findings.

## Requirements

- Python 3.14 (or 3.11+)
- `python-nmap` package (`py -m pip install python-nmap`)
- [Nmap for Windows](https://nmap.org/download.html) installed and on PATH (the script includes a fallback path for `C:\Program Files (x86)\Nmap`)

No other external packages needed — `socket`, `datetime`, and `os` are all standard library.

## How to run

```bash
py vuln_scanner.py
```

Or from the Lab-04 folder:

```bash
cd Lab-04
py vuln_scanner.py
```

When prompted:

- **Target IP** — the IP to scan (e.g. `127.0.0.1` for your own machine, or an authorized target)
- **Start port** — first port number to scan
- **End port** — last port number to scan

## Example output (abbreviated)

```
[*] Starting network scan for target: 10.136.3.136
[*] Scanning ports 1 to 100...

[*] Scanning target 10.136.3.136 for open ports...

[+] Open ports found: [53]
    [-] No banner on port 53

[*] Running Nmap vulnerability scan on 10.136.3.136 ...
[+] Hostnames: [{'name': '', 'type': ''}]
[+] OS match: [{'name': 'Android 9 (Linux 4.9)', 'accuracy': '98', ...}, ...]
[+] Report saved to: .../Lab-04/scan_report.txt
```

## Report file

After each scan, `scan_report.txt` is created in the same folder. It contains:

- Target, port range, scan times, duration
- Open ports and banner information
- Nmap host information (hostnames, OS matches with accuracy, CPEs)
- Nmap vulnerability results (or "No vulnerabilities detected")

## Scan performed

An authorized scan was run against `10.136.3.136` (ports 1–100):

- **Open port:** 53 (DNS)
- **Banner:** None (DNS on port 53/TCP does not send a text banner)
- **OS detection (top guess):** Android 9 (Linux 4.9) — 98% accuracy
- **Other OS guesses:** Android 10, OpenWrt 22.03, various Linux kernel versions
- **Vulnerabilities:** No vulnerabilities detected by Nmap vuln scripts

## Files

| File | Purpose |
|---|---|
| `vuln_scanner.py` | Main scanner script |
| `scan_report.txt` | Scan report from the authorized test scan |

## Authorization note

Only scan targets you own or have explicit written permission to scan.
Unauthorized scanning of networks or systems you do not control is illegal
in many jurisdictions and violates ethical security practice.

## Author

Arsha — cybersecurity student
- GitHub: https://github.com/seerinarsha-dotcom
- Email: seerinarsha@gmail.com
