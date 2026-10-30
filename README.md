# Raw Socket Port Clients

Python clients that talk directly to five standard network ports using only the built-in `socket` and `ssl` modules. Every protocol command is written and sent by hand. No `requests`, `urllib` or FTP/SMTP libraries are used.

Built for the **Computer Networks (CSNT207T)** assignment, Department of AIML, Assam Don Bosco University.

## Ports covered

| Script | Port | Protocol | Transport | Target |
|---|---|---|---|---|
| `port443_https.py` | 443 | HTTPS | TCP + TLS | example.com |
| `port80_http.py` | 80 | HTTP | TCP | example.com |
| `port21_ftp.py` | 21 | FTP (passive mode) | TCP, control + data sockets | test.rebex.net |
| `port465_smtp.py` | 465 | SMTP over SSL | TCP + TLS | smtp.gmail.com |
| `port53_dns.py` | 53 | DNS (A record lookup) | UDP | 8.8.8.8 |

## What each script does

- **443 / 80:** sends a raw `GET /` request over a socket, reads the response until the server closes the connection, decodes chunked transfer encoding, and saves the page as an HTML file that opens in the browser.
- **21:** logs in with `USER` and `PASS`, requests passive mode with `PASV`, opens the data connection the server names, downloads a file with `RETR`, and saves it locally. Handles both `227` and `229` passive replies.
- **465:** connects over TLS, greets with `EHLO`, authenticates with `AUTH LOGIN` (base64), and sends an email with `MAIL FROM`, `RCPT TO` and `DATA`.
- **53:** builds a DNS query packet byte by byte, sends it over UDP, and parses the answer section to print the IPv4 addresses.

## Requirements

- Python 3.8 or newer
- An internet connection
- For the SMTP script: a Gmail account with 2-Step Verification and an [app password](https://myaccount.google.com/apppasswords)

No third-party packages are needed.

## Running the scripts

From the folder containing the scripts:

```bash
python3 port443_https.py
python3 port80_http.py
python3 port53_dns.py
python3 port21_ftp.py
```

On Windows, use `python` instead of `python3`.

### Sending email (port 465)

The SMTP script reads its credentials from environment variables, so the password never appears in the code.

**bash / zsh:**
```bash
export SMTP_USER="you@gmail.com"
export SMTP_PASS="yourapppassword"
export SMTP_TO="recipient@example.com"   # optional, defaults to SMTP_USER
python3 port465_smtp.py
```

**PowerShell:**
```powershell
$env:SMTP_USER = "you@gmail.com"
$env:SMTP_PASS = "yourapppassword"
$env:SMTP_TO = "recipient@example.com"   # optional
python port465_smtp.py
```

**Windows Command Prompt:**
```cmd
set SMTP_USER=you@gmail.com
set SMTP_PASS=yourapppassword
set SMTP_TO=recipient@example.com
python port465_smtp.py
```

Enter the app password without spaces. The variables last only for the current terminal window.

## Example output

Running `port53_dns.py` prints the query and reply as hex, then the resolved addresses:

```
[+] Sent 29 bytes to 8.8.8.8:53
[+] ID=0x1234 Flags=0x8180 Questions=1 Answers=2
[+] example.com -> 172.66.147.243 (TTL 187s)
[+] example.com -> 104.20.23.154 (TTL 187s)
```

Addresses and TTL values change over time, so your output will differ.

## Changing the target

- **Web (443, 80):** change the `host` default in `fetch_page_via_port_443` or `fetch_page_via_port_80`.
- **FTP (21):** change `HOST`, `USER`, `PASSWORD` and `FILENAME` at the top of the file. The login and file must exist on the server you choose.
- **DNS (53):** change `DOMAIN` or `DNS_SERVER`.
- **SMTP (465):** set `SMTP_TO` to send to a different recipient.

## Notes

- Some websites reject requests without a `User-Agent` header. The web scripts send only the minimum headers, so pages on strict sites may return an error page.
- Generated files (`output.html`, `output_http.html`, `readme.txt`) are written to the current folder when the scripts run.
- The scripts are educational. Use them only against servers you are allowed to query.

## Assignment context

The assignment asks for five ports, raw-socket Python code for each, and captured terminal output, submitted as a LaTeX report. This repository holds the code only.
