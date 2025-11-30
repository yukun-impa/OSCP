
# Phase 1: Host & Port Discovery
First, you need to find the target. This could be a single IP address, a domain name, or a range of networks.

1.1 Network Scanning with nmap
nmap (Network Mapper) is the primary tool for this phase.

Basic Scan:

BASH
## Scan the most common 1000 ports
nmap -sV -sC <target_ip_or_domain>

## Scan all ports (slower but thorough)
nmap -sV -sC -p- <target_ip_or_domain>
-sV: Probes open ports to determine service/version info.
-sC: Runs default NSE (Nmap Scripting Engine) scripts, which can provide valuable info.
-p-: Scans all 65,535 ports.
Look for common web ports:

80 (HTTP)
443 (HTTPS)
3000, 8000, 8080, 8888 (Common Node.js development ports)
8443 (Alternative HTTPS)
