# H2 SQL Injection to RCE

The `id` parameter is concatenated into an H2 statement. H2 supports SQL
aliases backed by Java source; the task initializes an `EXEC` alias and the
intended path is to invoke it through an injected `UNION SELECT`. There is no
separate command query parameter: command execution must originate from SQL.

This application is intentionally vulnerable and must only run in the
isolated CTF environment.
