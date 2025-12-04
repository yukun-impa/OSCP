### NMap result
```
# Nmap 7.95 scan initiated Tue Dec  2 21:26:29 2025 as: /usr/lib/nmap/nmap --privileged -sC -sV -T4 -oN output/nmap_initial.txt 192.168.237.58
Nmap scan report for 192.168.237.58 (192.168.237.58)
Host is up (0.10s latency).
Not shown: 993 filtered tcp ports (no-response)
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.2
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:192.168.45.168
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.2 - secure, fast, stable
|_End of status
22/tcp   open  ssh         OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 4a:79:67:12:c7:ec:13:3a:96:bd:d3:b4:7c:f3:95:15 (RSA)
|   256 a8:a3:a7:88:cf:37:27:b5:4d:45:13:79:db:d2:ba:cb (ECDSA)
|_  256 f2:07:13:19:1f:29:de:19:48:7c:db:45:99:f9:cd:3e (ED25519)
80/tcp   open  http        Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-title: Simple PHP Photo Gallery
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16
111/tcp  open  rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: SAMBA)
445/tcp  open  netbios-ssn Samba smbd 4.10.4 (workgroup: SAMBA)
3306/tcp open  mysql       MySQL (unauthorized)
Service Info: Host: SNOOKUMS; OS: Unix

Host script results:
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2025-12-02T13:26:55
|_  start_date: N/A
|_clock-skew: mean: 1h40m01s, deviation: 2h53m15s, median: 0s
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.10.4)
|   Computer name: snookums
|   NetBIOS computer name: SNOOKUMS\x00
|   Domain name: \x00
|   FQDN: snookums
|_  System time: 2025-12-02T08:26:56-05:00
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Tue Dec  2 21:27:33 2025 -- 1 IP address (1 host up) scanned in 63.66 seconds
```
### Gobuster result
```
/db.php               (Status: 200) [Size: 0]
/functions.php        (Status: 200) [Size: 0]
/image.php            (Status: 200) [Size: 1508]
/images               (Status: 301) [Size: 237] [--> http://192.168.237.58/images/]
/index.php            (Status: 200) [Size: 2730]
/index.php            (Status: 200) [Size: 2730]
/js                   (Status: 301) [Size: 233] [--> http://192.168.237.58/js/]
/license.txt          (Status: 200) [Size: 18511]
/photos               (Status: 301) [Size: 237] [--> http://192.168.237.58/photos/]
/README.txt           (Status: 200) [Size: 4041]
```

Found you can access to images by `/images` and `/photos`

Try
