# Framework-specific SQL Injection and SSRF Challenges

Independent CTFd-Owl challenge source directories. Each public service exposes
port 80, joins the external `ctfd_frp_containers` network, and receives its flag
through `FLAG`. Multi-container SSRF tasks keep internal services on a private
task network.

| Challenge | Framework | Database |
|---|---|---|
| error-based | Node.js + Express | SQLite |
| double-query | Node.js + Express | SQLite |
| boolean-blind | Python + Flask | SQLite |
| time-blind | Python + Flask | SQLite |
| auth-bypass | PHP + Laravel 12 | SQLite |
| sqli-insert | PHP + Laravel 12 | SQLite |
| dumping-data | Python + FastAPI | SQLite |
| second-order | Python + FastAPI | SQLite |
| sqli-update | Java + Spring Boot | H2 |
| sqli-delete | Java + Spring Boot | H2 |
| sqli-lfi-rce | Go net/http | SQLite |

| Challenge | Pattern | Stack |
|---|---|---|
| ssrf-scheme | `file://` scheme | Python stdlib |
| ssrf-redirect | redirect to internal service | Python stdlib |
| ssrf-nginx-waf | incomplete loopback WAF | Nginx + Python |
| ssrf-blind | blind callback + command injection | Python stdlib |
| ssrf-dns-rebind | deterministic DNS rebinding | Python stdlib |

Run an individual challenge from its source directory with `docker compose up
--build`. These applications are intentionally vulnerable and are for isolated
CTF use only. The former root-level PHP/MySQL implementation has been removed.
