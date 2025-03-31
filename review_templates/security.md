# Security Code Review Template

## Overview
**Reviewer:** [Reviewer Name]  
**Date:** [YYYY-MM-DD]  
**Code/Project:** [Project Name]  
**Version/Commit:** [Version or Commit Hash]  
**Scope:** [Full/Partial codebase review]

## Risk Assessment Summary
- **Overall Security Risk:** [High/Medium/Low]
- **Critical Issues Found:** [Number]
- **Major Issues Found:** [Number]
- **Minor Issues Found:** [Number]

## Input Validation & Data Sanitization
- [ ] All user inputs are properly validated with whitelisting approach
- [ ] Input validation is performed on both client and server side
- [ ] SQL injection protection is implemented (parameterized queries/ORM)
- [ ] XSS protection is in place (output escaping/encoding)
- [ ] CSRF protections are implemented for all state-changing operations
- [ ] File upload validation and sanitization is implemented
- [ ] JSON/XML parsers are configured securely (prevent XXE attacks)

## Authentication & Authorization
- [ ] Authentication mechanisms follow modern security standards
- [ ] Passwords are properly hashed using strong algorithms (bcrypt/Argon2)
- [ ] Multi-factor authentication is available for sensitive operations
- [ ] Role-based access control is implemented with principle of least privilege
- [ ] Session management follows best practices (secure cookies, proper timeouts)
- [ ] API authentication uses secure methods (OAuth 2.0, API keys with proper rotation)
- [ ] Credential storage is secure (no plaintext or reversible encryption)

## Data Protection & Privacy
- [ ] Sensitive data is encrypted at rest using strong algorithms
- [ ] Secure communication protocols (TLS 1.2+) are enforced
- [ ] API keys, tokens and secrets are stored securely (not hardcoded)
- [ ] Personal data handling complies with relevant regulations (GDPR, CCPA)
- [ ] Data minimization principles are followed
- [ ] Proper data retention/deletion policies are implemented
- [ ] Logging doesn't contain sensitive or personal information

## Dependency Security
- [ ] Third-party libraries are up-to-date with no known vulnerabilities
- [ ] Software supply chain security considerations are addressed
- [ ] Dependencies have appropriate integrity checks
- [ ] Container images (if used) are scanned for vulnerabilities
- [ ] Package lockfiles are used to prevent dependency confusion attacks

## Secure Configuration & Infrastructure
- [ ] Environment-specific configurations use secure defaults
- [ ] No sensitive information in configuration files
- [ ] Infrastructure as Code security checks are performed
- [ ] Security headers are properly configured (CSP, HSTS, etc.)
- [ ] Rate limiting/throttling is implemented for sensitive operations
- [ ] Proper error handling without information disclosure

## Cryptographic Practices
- [ ] Strong, modern crypto algorithms and protocols are used
- [ ] Secure random number generation for security-critical operations
- [ ] Proper key management practices are followed
- [ ] No custom cryptographic implementations

## Security Testing Evidence
- [ ] SAST results reviewed and addressed
- [ ] DAST/penetration testing performed
- [ ] Dependency scanning results reviewed
- [ ] Security-focused code review performed

## Specific Findings
1. **[Critical/High/Medium/Low]**: [Brief issue description]
   - Location: [File/function reference]
   - Details: [Detailed explanation]
   - Recommendation: [Fix recommendation]

2. **[Critical/High/Medium/Low]**: [Brief issue description]
   - Location: [File/function reference]
   - Details: [Detailed explanation]
   - Recommendation: [Fix recommendation]

## Additional Notes
[Any other security observations or recommendations that don't fit in the categories above]

## Resources
- [Links to relevant security guidelines, standards, or best practices]