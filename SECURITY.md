# Security Policy

## Supported Versions

As AICF is currently in active specification and architectural design (v0.1-draft), security updates are applied directly to the active `main` branch.

| Version | Supported          | Status             |
| :------ | :----------------- | :----------------- |
| 0.1.x   | :white_check_mark: | Active Development |

---

## Reporting a Vulnerability

We take the security of AICF, its schemas, adapters, and downstream AI integration patterns seriously. 

If you discover a potential vulnerability or security concern—especially concerning:
- Agent permission escalation or prompt injection vulnerabilities in behavior contracts
- Template security flaws (e.g., accidental secret exposure patterns)
- Tooling or CLI execution security (once implemented)

Please report it responsibly:

1. **GitHub Security Advisories (Preferred):**  
   Use GitHub's [Private Vulnerability Reporting](https://github.com/<owner>/AICF/security/advisories/new) if enabled on this repository.

2. **Email Notification:**  
   Contact the repository maintainers via security advisory or designated security contact:
   - Point of Contact: *`[TODO: Maintainers to configure security contact email]`*

### What to Include
Please include as much information as possible to help us triage the issue:
- Description of the vulnerability or risk vector
- Steps to reproduce or demonstration prompt/configuration
- Potential impact on projects adopting AICF
- Any proposed mitigations or remediation strategies

### Response Timeline
- We will acknowledge receipt of the report within 3 business days.
- A remediation assessment and plan will be communicated within 7 business days.

---

> [!NOTE]
> **Maintainer TODO / Review Item:**  
> Finalize the project's official security email address and security response team roster prior to public release.
