## Brief overview
A rule to handle specific command syntax for the PowerShell environment, based on repeated errors encountered during development.

## Command Syntax
- Do not use the `rem` command for comments, as it is not compatible with PowerShell. Use `#` for comments instead.
- When executing scripts or executables in the current directory, always prefix them with `.\` (e.g., `.\start_all_services.bat`).
- When chaining commands, use a semicolon (`;`) instead of `&&`.
- When using `curl` (which is an alias for `Invoke-WebRequest`), construct headers as a dictionary (`@{"key"="value"}`) instead of a string.
