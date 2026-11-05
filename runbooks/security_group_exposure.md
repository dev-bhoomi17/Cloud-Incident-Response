# Security Group Exposure Incident Response Runbook

## 1. Incident Overview

**Incident:** Overly permissive AWS Security Group inbound rules.

**Objective:** Detect and restrict unintended internet-wide network access.

**Severity:** High, depending on the exposed services and systems.

## 2. Detection

- Monitor AWS API activity using CloudTrail.
- Identify suspicious events:
  - AuthorizeSecurityGroupIngress
  - ModifySecurityGroupRules
- EventBridge detects matching events.
- The security monitoring system routes the event to the remediation Lambda.

## 3. Analysis

The security team should:

1. Identify the affected security group.
2. Review its inbound rules.
3. Identify ports and protocols exposed.
4. Check for unrestricted IPv4 (`0.0.0.0/0`) or IPv6 (`::/0`) access.
5. Identify the user or role responsible.
6. Determine whether any affected resources require further investigation.

## 4. Containment

**Automated response:**

- EventBridge triggers the Security Group Remediation Lambda.
- Lambda identifies internet-wide IPv4 and IPv6 CIDR entries.
- It removes those public CIDR entries while preserving restricted CIDR entries.

**Manual response:**

- Review the affected security group in AWS.
- Remove unauthorized inbound rules.
- Restrict access to approved source IP ranges.
- Confirm that necessary application connectivity remains available.

## 5. Eradication

1. Remove unintended inbound permissions.
2. Review security group configurations.
3. Check related network access controls.
4. Review IAM permissions for users and roles.
5. Correct the configuration mistake.
6. Investigate possible unauthorized access.

## 6. Recovery

1. Verify that unrestricted inbound access has been removed.
2. Confirm legitimate application connectivity.
3. Restore only approved inbound rules.
4. Monitor further security group modifications.
5. Document the incident and corrective actions.

## 7. Manual Intervention

If automated remediation fails:

- Notify the security administrator.
- Identify the affected security group.
- Review all inbound rules.
- Remove unauthorized public CIDR entries manually.
- Verify required application connectivity.
- Record the reason for automation failure and its resolution.

## 8. NIST Incident Response Mapping

| NIST Phase | Runbook Activity |
|---|---|
| Preparation | IAM permissions and monitoring configuration |
| Detection and Analysis | CloudTrail event monitoring and investigation |
| Containment | Remove unrestricted inbound access |
| Eradication | Correct insecure network rules |
| Recovery | Verify and restore approved connectivity |
| Post-Incident Activity | Record lessons learned and improve controls |

## 9. Testing and Limitations

The security group remediation logic is tested locally using Python, pytest and Moto.

Testing includes:
- Removing internet-wide IPv4 access.
- Preserving restricted CIDR access.
- Handling missing security group identifiers.
- Handling already restricted security groups.

No real AWS deployment or production network changes were performed. Actual AWS execution requires deployment, permissions and integration validation.