# DNS Rebinding SSRF

The validator performs one DNS lookup and checks the returned address. The
connection performs a second lookup, controlled by the private DNS service.
The deterministic resolver returns a documentation IP first and loopback on
the second lookup, allowing access to the local admin endpoint.

Use a hostname such as `rebind.test` in the URL. The DNS server is private to
the task network and is not exposed through Owl.
