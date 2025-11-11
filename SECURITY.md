# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing estopheles@proton.me.

**Please do not report security vulnerabilities through public GitHub issues.**

### What to include in your report:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if available)

### Response timeline:

- **Initial response**: Within 48 hours
- **Status update**: Within 7 days
- **Resolution**: Varies based on complexity

## Security Features

This project includes several security measures:

- **Path Traversal Protection**: All file paths are validated
- **SSRF Prevention**: URL validation with domain whitelisting
- **Input Sanitization**: All user inputs are validated
- **PDF Security Analysis**: Detection of malicious PDF content
- **Structured Logging**: Security events are logged for audit

## Security Best Practices

When using this tool:

1. Run in isolated environments for untrusted PDFs
2. Keep dependencies updated
3. Review security logs regularly
4. Use environment variables for sensitive configuration
5. Limit network access when possible
