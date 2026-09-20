# Nginx WAF SSRF

An Nginx edge filter blocks a small list of obvious loopback spellings. The
backend fetcher does not repeat this validation, and its internal admin endpoint
is bound to `127.0.0.1:8081`.

This is intentionally vulnerable and must only run in the isolated CTF network.
