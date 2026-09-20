# SSRF Redirect

The public fetcher follows redirects without validating the final destination.
The internal redirector can point it to `http://internal:8081/flag`.

Only `service` is exposed through Owl. `redirector` and `internal` are private
members of the task network.
