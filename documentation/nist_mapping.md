# NIST Incident Response Lifecycle Mapping

## 1. Introduction

This project follows the NIST incident response lifecycle to provide a structured approach to detecting, analysing and responding to cloud security incidents.

The project uses AWS CloudTrail, EventBridge, Lambda and SNS to support automated monitoring and remediation.

## 2. NIST Lifecycle Phases

### Phase 1: Preparation

**Objective:** Establish the resources and procedures required to respond to security incidents.

Project implementation:
- CloudFormation defines the monitoring infrastructure.
- IAM roles provide required service permissions.
- SNS provides the security alert notification channel.
- Incident response runbooks define response procedures.
- Automated Lambda playbooks are prepared for common misconfigurations.

### Phase 2: Detection and Analysis

**Objective:** Identify suspicious activities and understand their impact.

Project implementation:
- CloudTrail records AWS API activity.
- EventBridge evaluates selected suspicious API events.
- Alert Handler Lambda processes matching events.
- SNS publishes security notifications.
- Security teams can investigate the event details.

### Phase 3: Containment

**Objective:** Limit the impact of a detected security incident.

Project implementation:
- S3 Remediation Lambda enables all four Block Public Access settings.
- Security Group Remediation Lambda removes internet-wide inbound CIDR entries.
- Manual intervention procedures are available if automation fails.

### Phase 4: Eradication

**Objective:** Remove the underlying security weakness.

Project implementation:
- Review and remove unauthorized S3 bucket policies and ACLs.
- Correct insecure security group rules.
- Review IAM permissions and configuration errors.
- Investigate possible unauthorized activity.

### Phase 5: Recovery

**Objective:** Restore secure and approved operations.

Project implementation:
- Verify S3 access configuration.
- Verify security group rules.
- Restore legitimate application access.
- Monitor for repeated suspicious activity.

### Phase 6: Post-Incident Activity

**Objective:** Learn from the incident and improve future security.

Project implementation:
- Maintain incident records.
- Document automation failures.
- Review test results.
- Improve monitoring and remediation procedures.
- Update runbooks based on lessons learned.

## 3. NIST Mapping Summary

| NIST Phase | Project Components |
|---|---|
| Preparation | CloudFormation, IAM, SNS, Runbooks |
| Detection and Analysis | CloudTrail, EventBridge, Alert Lambda |
| Containment | S3 and Security Group Remediation Lambdas |
| Eradication | Configuration correction and permission review |
| Recovery | Access verification and service restoration |
| Post-Incident Activity | Documentation, testing and improvements |

## 4. Conclusion

The project applies the NIST incident response lifecycle to two cloud security scenarios: S3 data exposure and overly permissive security group rules.

Automated detection, notification and remediation reduce the manual effort required during incident response. Manual procedures remain important when automation fails or human investigation is necessary.

**Implementation note:** The project is developed and tested locally using Python, pytest and Moto. Actual AWS deployment and live incident response have not been performed.