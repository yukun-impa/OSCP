# OSCP note
## OSCP
### note structure
OSCP-Prep/
├── README.md                  # The master guide
├── Methodology/               # General workflows
│   ├── Network-Scanning.md
│   ├── Web-Enumeration.md
│   └── Active-Directory.md
├── Cheatsheets/               # Quick copy-paste commands
│   ├── Reverse-Shells.md
│   ├── File-Transfers.md
│   ├── Linux-Commands.md
│   ├── Windows-Commands.md
│   ├── SQL-Injection.md
│   └── Buffer-Overflow.md     # (Less critical now, but good to have)
├── Privilege-Escalation/
│   ├── Linux-PrivEsc.md
│   └── Windows-PrivEsc.md
├── Tools/                     # Custom scripts or links to tools
├── Writeups/                  # Your notes on HTB/TryHackMe boxes
│   ├── Windows/
│   └── Linux/
└── Report-Template/           # A draft report structure

### Phase 1: Enumeration (Information Gathering)
Port Scan:
Quick scan: nmap -p- --min-rate=1000 -T4 <IP>
Detailed scan: nmap -p<ports> -sC -sV -A <IP>
UDP scan (if stuck): nmap -sU --top-ports 100 <IP>
Service Enumeration (Based on ports found):
HTTP/HTTPS (80/443):
View source code.
Check robots.txt.
Identify technologies (Wappalyzer).
Directory Fuzzing: gobuster or feroxbuster to find hidden folders.
Subdomain Fuzzing: If access is via a domain name (e.g., box.htb).
SMB (139/445):
Can you list shares anonymously? (smbclient -L //IP -N)
Are there readable files?
FTP (21):
Is Anonymous login allowed?
SSH (22):
Usually not the entry point unless you find credentials elsewhere or it's a very old version.
### Phase 2: Vulnerability Assessment
Searchsploit: Run searchsploit <service name> <version> for every service found.
Google: Search "Service Name Version exploit github".
Web Apps: Check for default credentials (admin/admin), SQL Injection on login forms, or RCE (Remote Code Execution) vulnerabilities.
### Phase 3: Initial Access (Exploitation)
The Goal: Get a reverse shell.
Action: Execute the exploit found in Phase 2.
Stability: Once you get a shell, upgrade it to a stable TTY shell (so you can use arrows and don't accidentally kill it with Ctrl+C).
Python trick: python3 -c 'import pty; pty.spawn("/bin/bash")'
### Phase 4: Post-Exploitation (Privilege Escalation)
Now that you are a low-level user, you need to become Root (Linux) or Administrator/System (Windows).

#### Linux PrivEsc Steps:

Manual Check: sudo -l (What can I run as root without a password?).
SUID Check: Find files with SUID bit set. Check GTFOBins.
Kernel: Is the OS ancient? (DirtyCow, PwnKit).
Automation: Upload and run LinPEAS. It will highlight vectors in red/yellow.
Cron Jobs: Are there scripts running automatically that you can edit?
#### Windows PrivEsc Steps:

User Privileges: whoami /priv (Look for SeImpersonate).
Automation: Upload and run WinPEAS.
Services: Unquoted service paths, weak folder permissions on services.
Kernel: Watters/WinErase (if applicable).
### Phase 5: The Active Directory (AD) Set (Specific to OSCP)
Pivoting: You need to use tools like Chisel or Ligolo-ng to tunnel traffic through the first compromised machine to reach the internal network.
Lateral Movement:
Dump hashes (Mimikatz).
Pass-the-Hash (Evil-WinRM / CrackMapExec).
Kerberoasting / AS-REP Roasting (Impacket).
Bloodhound (Visualizing the domain path to Admin).

