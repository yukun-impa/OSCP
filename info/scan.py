import subprocess
import sys
import os
import argparse
import shutil
import socket

# --- CONFIGURATION ---
# Default wordlist commonly found on Kali Linux
DEFAULT_WORDLIST = "/usr/share/wordlists/dirb/common.txt"

def run_command(command, log_file=None):
    """
    Runs a shell command. 
    If log_file is provided, writes output to file AND prints to screen.
    """
    print(f"[*] Executing: {command}")
    try:
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        output_buffer = []

        for line in process.stdout:
            print(line, end='')
            output_buffer.append(line)
            
        process.wait()
        
        if log_file:
            with open(log_file, 'w') as f:
                f.writelines(output_buffer)

        if process.returncode != 0:
            print(f"\n[!] Warning: Command finished with errors or found nothing.")
            return False
        return True
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")
        sys.exit(0)

def is_port_open(ip, port):
    """
    Quickly checks if a specific TCP port is open using sockets.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, int(port)))
        s.close()
        return True
    except:
        return False

def scan_snmp(target_ip, output_dir):
    """
    Checks UDP 161 and runs SNMP tools.
    """
    print("\n" + "=" * 50)
    print("[*] Phase: SNMP Enumeration")
    print("=" * 50)

    # Check UDP 161 via Nmap (sockets are unreliable for UDP detection)
    print("[*] Checking if UDP port 161 is open...")
    check_cmd = f"sudo nmap -sU -p 161 --open {target_ip}"
    
    try:
        result = subprocess.check_output(check_cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError:
        return

    if "161/udp open" in result:
        print("[+] SNMP detected! Running tools...")
        
        # Nmap Scripts
        run_command(f"sudo nmap -sU -p 161 --script snmp-info,snmp-processes -oN {output_dir}/snmp_nmap.txt {target_ip}")

        # snmpwalk
        if shutil.which("snmpwalk"):
            print(f"[*] Running snmpwalk (public)...")
            os.system(f"snmpwalk -c public -v 2c {target_ip} > {output_dir}/snmpwalk.txt")
        
        # snmp-check
        if shutil.which("snmp-check"):
            run_command(f"snmp-check {target_ip}", log_file=f"{output_dir}/snmp-check.txt")
    else:
        print("[-] SNMP (UDP 161) appears closed.")

def scan_web(target_ip, output_dir, wordlist):
    """
    Checks Port 80/443 and runs Gobuster.
    """
    print("\n" + "=" * 50)
    print("[*] Phase: Web Enumeration (Gobuster)")
    print("=" * 50)

    if not shutil.which("gobuster"):
        print("[!] Gobuster is not installed. Skipping.")
        return

    if not os.path.exists(wordlist):
        print(f"[!] Wordlist not found at {wordlist}. Skipping Gobuster.")
        print("    Tip: Use --wordlist to specify a valid path.")
        return

    # Check HTTP (80)
    if is_port_open(target_ip, 80):
        print(f"[+] Port 80 is OPEN. Running Gobuster on HTTP...")
        outfile = os.path.join(output_dir, "gobuster_http.txt")
        # -k skips SSL check, -x looks for extensions, -t threads, --no-color for clean log files
        cmd = f"gobuster dir -u http://{target_ip} -w {wordlist} -o {outfile} -x php,txt,html,sh -t 50 --no-color"
        run_command(cmd)
    
    # Check HTTPS (443)
    if is_port_open(target_ip, 443):
        print(f"[+] Port 443 is OPEN. Running Gobuster on HTTPS...")
        outfile = os.path.join(output_dir, "gobuster_https.txt")
        cmd = f"gobuster dir -u https://{target_ip} -w {wordlist} -k -o {outfile} -x php,txt,html,sh -t 50 --no-color"
        run_command(cmd)

    if not is_port_open(target_ip, 80) and not is_port_open(target_ip, 443):
        print("[-] Neither port 80 nor 443 are open. Skipping Gobuster.")

def main():
    parser = argparse.ArgumentParser(description="CTF Scanner: Nmap, SNMP, and Gobuster")
    parser.add_argument("target", help="Target IP address")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--wordlist", "-w", default=DEFAULT_WORDLIST, help=f"Path to wordlist (default: {DEFAULT_WORDLIST})")
    
    args = parser.parse_args()
    target_ip = args.target
    output_dir = args.output
    wordlist = args.wordlist

    if output_dir != ".":
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    print(f"[*] Starting Comprehensive CTF Scan on {target_ip}")

    # --- PHASE 1: TCP Initial ---
    print(f"\n[*] Phase 1: Nmap Initial Scan (Top 1000)")
    run_command(f"nmap -sC -sV -T4 -oN {output_dir}/nmap_initial.txt {target_ip}")

    # --- PHASE 2: Web Enumeration ---
    scan_web(target_ip, output_dir, wordlist)

    # --- PHASE 3: SNMP Enumeration ---
    scan_snmp(target_ip, output_dir)

    # --- PHASE 4: TCP Full Scan ---
    print(f"\n[*] Phase 4: Nmap Full Scan (All Ports)")
    print("[*] This runs last as it takes the longest.")
    run_command(f"nmap -p- -T4 -oN {output_dir}/nmap_full.txt {target_ip}")

    print("\n" + "="*50)
    print(f"[*] All scans completed. Results in: {output_dir}")

if __name__ == "__main__":
    main()

