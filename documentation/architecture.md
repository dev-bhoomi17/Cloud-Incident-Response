# Cloud Security Incident Response Architecture

## 1. Project Overview

The Cloud Security Incident Response project demonstrates automated detection, alerting and remediation of common cloud security misconfigurations using an AWS-compatible architecture.

The project is developed and tested locally using Python, pytest and Moto because an actual AWS account was not available.

## 2. Technology Stack

- AWS CloudFormation – Infrastructure as Code
- AWS Lambda – Automated incident response
- AWS CloudTrail – API activity monitoring
- Amazon EventBridge – Event detection and routing
- Amazon SNS – Security notifications
- Amazon S3 – Storage security monitoring
- Amazon EC2 – Security group monitoring
- Python 3.12 – Lambda implementation
- pytest and Moto – Local testing and AWS service simulation
- cfn-lint – CloudFormation template validation

## 3. Architecture Components

The CloudFormation template contains 19 resources:

1. Test S3 Bucket
2. Test VPC
3. Test Security Group
4. CloudTrail Log Bucket
5. CloudTrail Bucket Policy
6. Security Trail
7. Security Alert SNS Topic
8. Alert Lambda Execution Role
9. Alert Handler Lambda
10. Security Event EventBridge Rule
11. Alert Lambda Invocation Permission
12. S3 Remediation IAM Role
13. S3 Remediation Lambda
14. Security Group Remediation IAM Role
15. Security Group Remediation Lambda
16. S3 Remediation EventBridge Rule
17. S3 Remediation Invocation Permission
18. Security Group Remediation EventBridge Rule
19. Security Group Remediation Invocation Permission

## 4. Suspicious Activity Alert Workflow

1. An AWS API activity event is recorded by CloudTrail.
2. EventBridge evaluates the event against suspicious