# Security Code Review Template

## Input Validation
- [ ] All user inputs are properly validated
- [ ] Input validation is performed on the server side
- [ ] SQL injection protection is in place
- [ ] XSS protection is implemented

## Authentication & Authorization
- [ ] Authentication mechanisms are secure
- [ ] Passwords are properly hashed and salted
- [ ] Role-based access control implemented correctly
- [ ] Session management follows best practices

## Data Protection
- [ ] Sensitive data is encrypted at rest
- [ ] Secure communication protocols (HTTPS, SSL/TLS) are used
- [ ] API keys and secrets are not hardcoded
- [ ] No sensitive information in logs

## Dependency Security
- [ ] Third-party libraries are up-to-date
- [ ] Dependencies have been checked for known vulnerabilities
- [ ] Minimum required permissions are used

## Error Handling
- [ ] Errors are handled properly
- [ ] No sensitive information is exposed in error messages
- [ ] Applications fails securely

## Additional Notes:
(Add any specific security observations or suggestions here)