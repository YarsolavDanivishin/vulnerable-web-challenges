# SQL Injection and SSRF CTF Challenges

Each `tasks/<challenge>` directory is a self-contained CTFd-Owl source
catalog. Public services listen on port 80 and use the external network
`ctfd_frp_containers`. Multi-container SSRF tasks also create a private task
network for internal services.

| Challenge | Framework | SQLi type |
|---|---|---|
| error-based | Node.js + Express | error-based |
| double-query | Node.js + Express | double-query |
| boolean-blind | Python + Flask | boolean-blind |
| time-blind | Python + Flask | time-blind |
| auth-bypass | PHP + Laravel 12 | auth-bypass |
| sqli-insert | PHP + Laravel 12 | sqli-insert |
| dumping-data | Python + FastAPI | dumping-data |
| second-order | Python + FastAPI | second-order |
| sqli-update | Java + Spring Boot | sqli-update |
| sqli-delete | Java + Spring Boot | sqli-delete |
| sqli-lfi-rce | Go | sqli-lfi-rce |

| Challenge | Architecture | SSRF pattern |
|---|---|---|
| ssrf-scheme | Python stdlib | `file://` local file read |
| ssrf-redirect | Python stdlib | redirect to private service |
| ssrf-nginx-waf | Nginx + Python | incomplete loopback WAF |
| ssrf-blind | Python stdlib | blind callback + command injection |
| ssrf-dns-rebind | Python stdlib | controlled DNS rebinding |

## Local run

```bash
cd tasks/error-based
FLAG="$(openssl rand -hex 32)" docker compose up --build
```

For SSRF tasks, only the `service` container is exposed through Owl. Internal
services are intentionally not published with Docker `ports:`.

The external network must already exist for Owl-compatible compose files:

```bash
```

The services deliberately interpolate request data into SQL and expose
framework/database errors where relevant. They must only be run in an
isolated training environment.
