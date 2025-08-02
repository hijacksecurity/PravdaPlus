# Security Guide for PravdaPlus

This document outlines the security measures implemented in PravdaPlus and best practices for contributors.

## 🔒 Security Features

### 1. Secret Management
- **No Hardcoded Secrets**: All sensitive data is stored in environment variables
- **Environment Templates**: `.env.example` provides safe templates
- **Kubernetes Secrets**: Production secrets managed via Kubernetes secrets

### 2. Automated Security Scanning
- **Gitleaks Pre-commit Hook**: Prevents accidental secret commits
- **Pattern Detection**: Comprehensive regex patterns for common secret types
- **Custom Configuration**: Tailored `.gitleaks.toml` for project-specific needs

### 3. File Exclusions
- **Comprehensive .gitignore**: Excludes all sensitive file types
- **Environment Files**: All `.env*` files excluded except templates
- **Build Artifacts**: Temporary and generated files excluded

## 🛡️ Gitleaks Configuration

### Detected Secret Types
- OpenAI API Keys (`sk-*`)
- Anthropic API Keys (`sk-ant-*`)
- JWT Secrets
- Database Passwords
- AWS Keys
- SSH Keys
- Generic API Keys

### Allowlisted Files
- `.env.example` (template files)
- `README.md` and documentation
- Configuration files

## 🚨 Incident Response

### If Secrets Are Committed

1. **Immediate Actions**:
   ```bash
   # Remove the secret from the repository
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch path/to/file' --prune-empty --tag-name-filter cat -- --all
   
   # Force push (if you have permission)
   git push origin --force --all
   ```

2. **Rotate Compromised Secrets**:
   - Generate new API keys
   - Update production deployments
   - Monitor for unauthorized usage

3. **Review and Improve**:
   - Analyze how the secret was committed
   - Improve detection patterns if needed
   - Update team training

### Reporting Security Issues

- **Email**: security@your-domain.com
- **Encrypted**: Use GPG key [KEY_ID] for sensitive reports
- **Response Time**: 24 hours for acknowledgment, 72 hours for initial assessment

## 🔧 Developer Setup

### Initial Setup
```bash
# Install gitleaks
brew install gitleaks

# Pre-commit hook is automatically configured
# Test the setup
gitleaks detect --source . --verbose
```

### Before Committing
```bash
# Manual security scan
gitleaks detect --source . --verbose

# If clean, commit normally
git add .
git commit -m "Your commit message"

# The pre-commit hook will run automatically
```

### Bypassing Checks (Emergency Only)
```bash
# Only use in genuine emergencies
git commit --no-verify

# Always follow up with proper fix
```

## 📋 Security Checklist

### For Contributors
- [ ] Never commit `.env` files
- [ ] Use `.env.example` as template
- [ ] Test gitleaks before pushing: `gitleaks detect --source . --verbose`
- [ ] Use environment variables for all secrets
- [ ] Rotate any accidentally exposed secrets immediately

### For Maintainers
- [ ] Review all PRs for potential secrets
- [ ] Keep gitleaks configuration updated
- [ ] Monitor security advisories for dependencies
- [ ] Regular security audits of the codebase
- [ ] Ensure CI/CD pipelines include security checks

### For Deployment
- [ ] Use Kubernetes secrets for production
- [ ] Enable audit logging in production
- [ ] Implement network policies
- [ ] Regular security updates for base images
- [ ] Monitor for suspicious activity

## 🔐 Environment Variable Guidelines

### Required Format
```bash
# Use descriptive names
OPENAI_API_KEY="your-key-here"

# Not generic names
KEY="your-key-here"  # ❌ Too generic
```

### Secret Strength Requirements
- **API Keys**: Use provider-generated keys only
- **JWT Secrets**: Minimum 32 characters, cryptographically random
- **Database Passwords**: Minimum 16 characters, mixed case + numbers + symbols

### Storage
- **Development**: `.env` file (gitignored)
- **Production**: Kubernetes secrets or external secret management
- **CI/CD**: Encrypted environment variables

## 📚 Resources

### Documentation
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [OWASP Secret Management](https://owasp.org/www-community/vulnerabilities/Insufficiently_Protected_Credentials)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

### Tools
- **Gitleaks**: Secret scanning
- **GitGuardian**: Additional secret detection
- **Trivy**: Container vulnerability scanning
- **SAST Tools**: Static analysis security testing

---

**Remember**: Security is everyone's responsibility. When in doubt, ask for a security review.