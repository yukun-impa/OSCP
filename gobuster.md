# Directory brute-forcing with a common wordlist
```
gobuster dir -u http://<target>/ -w /usr/share/wordlists/dirb/common.txt
``

# More advanced with extensions
gobuster dir -u http://<target>/ -w /usr/share/wordlists/dirb/common.txt -x .js,.json,.txt

# Using ffuf (often faster)
ffuf -u http://<target>/FUZZ -w /usr/share/wordlists/dirb/common.txt
Common Wordlists:

common.txt (included in Kali Linux's dirb/dirbuster)
directory-list-2.3-medium.txt (from SecLists project)
api_endpoints.txt (from SecLists)
