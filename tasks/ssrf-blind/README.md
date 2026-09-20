# Blind SSRF + Command Injection

`/submit?url=...` performs an asynchronous request and never returns the
response body. The private `callback:8080` endpoint passes its `cmd` parameter
to an intentionally unsafe worker. Results are written to the shared task
volume and can be viewed with `/result?token=...`.

The worker is isolated, has no Docker socket, and is connected only to the task
network.
