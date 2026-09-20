# SSRF Scheme

The URL fetcher accepts `http`, `https`, and `file` schemes. The intended path
is to use the `file` scheme to read local files from the challenge container.

The flag is stored at `/opt/secret/flag.txt`.

This application is intentionally vulnerable and must only run in the isolated
CTF network.
