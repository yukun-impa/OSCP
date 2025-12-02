import os
import stat
import platform
import subprocess

# python3 -m http.server 8000 
def get_system_info():
    """
    Gathers basic system information to check for Kernel vulnerabilities.
    """
    print("[-] Gathering System Information...")
    try:
        uname = platform.uname()
        print(f"    OS: {uname.system}")
        print(f"    Release: {uname.release}")
        print(f"    Version: {uname.version}")
        print(f"    Machine: {uname.machine}")
    except Exception as e:
        print(f"    Error gathering system info: {e}")
    print("-" * 40)

def find_suid_binaries():
    """
    Scans the filesystem for SUID binaries.
    SUID (Set owner User ID up on execution) allows a user to run an executable 
    with the permissions of the executable's owner (usually root).
    """
    print("[-] Searching for SUID binaries...")
    suid_files = []
    # Common directories to scan to save time (avoiding /proc, /sys, etc.)
    search_paths = ['/bin', '/sbin', '/usr/bin', '/usr/sbin', '/usr/local/bin']
    
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    filepath = os.path.join(root, name)
                    try:
                        # Get file stats
                        file_stat = os.stat(filepath)
                        # Check if SUID bit is set (stat.S_ISUID)
                        if file_stat.st_mode & stat.S_ISUID:
                            suid_files.append(filepath)
                            print(f"    [+] SUID Found: {filepath}")
                    except PermissionError:
                        continue # Skip files we can't read
                    except Exception:
                        continue
    
    if not suid_files:
        print("    No SUID binaries found in common paths.")
    print("-" * 40)

def check_writable_etc():
    """
    Checks if critical configuration files or directories are world-writable.
    If /etc/passwd or /etc/shadow are writable, a user might add a root user.
    """
    print("[-] Checking for writable critical files...")
    critical_paths = ['/etc/passwd', '/etc/shadow', '/etc/sudoers']
    
    for filepath in critical_paths:
        if os.path.exists(filepath):
            try:
                # Check if the file is writable by the current user
                if os.access(filepath, os.W_OK):
                    print(f"    [!] CRITICAL: {filepath} is writable!")
                else:
                    print(f"    [OK] {filepath} is not writable.")
            except Exception as e:
                print(f"    Error checking {filepath}: {e}")
    print("-" * 40)

def check_sudo_privileges():
    """
    Attempts to list sudo privileges for the current user.
    Equivalent to running 'sudo -l'.
    """
    print("[-] Checking sudo privileges (sudo -l)...")
    try:
        # This command might prompt for a password, so it requires interaction
        # or NOPASSWD to be set in sudoers.
        result = subprocess.run(['sudo', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("    Could not run 'sudo -l' (User may need password or has no sudo access).")
    except FileNotFoundError:
        print("    'sudo' command not found.")
    print("-" * 40)

if __name__ == "__main__":
    print("=== Basic CTF Privilege Escalation Enumerator ===\n")
    get_system_info()
    check_writable_etc()
    check_sudo_privileges()
    find_suid_binaries()

