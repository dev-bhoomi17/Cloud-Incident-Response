# S3 Data Exposure Incident Response Runbook

## 1. Incident Overview

**Incident:** Accidental public exposure of an Amazon S3 bucket.

**Objective:** Detect, investigate, contain, eradicate and recover from an S3 bucket exposure.

**Severity:** High (depending on data sensitivity and exposure).

## 2. Detection

- Monitor CloudTrail API activity.
- Identify suspicious events such as:
  - PutBucketPolicy
  - PutBucketAcl
  - DeletePublicAccessBlock
- EventBridge detects matching API events.
- Alert Lambda publishes a notification through SNS.

## 3. Analysis

The security team should:

1. Identify the affected S3 bucket.
2. Review CloudTrail event details.
3. Identify the user or role responsible.
4. Check the bucket policy and ACL.
5. Determine whether sensitive data may have been exposed.
6. Review access logs, if available.

## 4. Containment

**Automated response:**

- EventBridge triggers the S3 remediation Lambda.
- Lambda enables all four S3 Block Public Access settings.

**Manual response:**

- Restrict public access through the AWS Management Console.
- Review bucket policies and ACLs.
- Restrict access to authorized users and roles.

## 5. Eradication

1. Remove unauthorized public bucket policies.
2. Remove unintended public ACL permissions.
3. Review IAM permissions.
4. Identify and correct the configuration error.
5. Rotate credentials if compromise is suspected.

## 6. Recovery

1. Verify that public access is blocked.
2. Confirm legitimate application access still works.
3. Restore approved access permissions.
4. Monitor CloudTrail for repeated suspicious activity.
5. Record the incident and corrective actions.

## 7. Manual Intervention

If automated remediation fails:

- Notify the security administrator.
- Identify the affected bucket.
- Apply Block Public Access manually.
- Review bucket policies and ACLs.
- Verify the corrected configuration.
- Document the failure and resolution.

## 8. NIST Incident Response Mapping

| NIST Phase | Runbook Activity |
|---|---|
| Preparation | Monitoring, IAM configuration and response planning |
| Detection and Analysis | CloudTrail review and SNS alerts |
| Containment | Block public access |
| Eradication | Remove unauthorized policies and permissions |
| Recovery | Verify and restore approved services |
| Post-Incident Activity | Document lessons learned |

## 9. Testing and Limitations

The remediation logic is tested locally using Python, pytest and Moto.

No real AWS deployment or public data exposure was performed. Actual AWS execution requires deployment, permissions and integration validation.