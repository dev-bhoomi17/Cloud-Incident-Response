# Cloud Security Incident Response Runbook with Automated Alerting

## 1. Introduction

The Cloud Security Incident Response System demonstrates how suspicious cloud activities can be detected, security alerts generated and common cloud security misconfigurations automatically remediated.

The project uses AWS-compatible infrastructure definitions and Python-based Lambda functions. Development and testing are performed locally using Moto because no live AWS account was used.

## 2. Objectives

- Monitor suspicious cloud API activities.
- Generate automated security notifications.
- Remediate insecure S3 bucket configurations.
- Restrict overly permissive security group rules.
- Follow the NIST incident response lifecycle.
- Provide manual intervention procedures when automation fails.

## 3. Technologies Used

- AWS CloudFormation
- AWS CloudTrail
- Amazon EventBridge
- AWS Lambda
- Amazon SNS
- Amazon S3
- Amazon EC2
- AWS IAM
- Python 3.12 and Boto3
- Moto
- Pytest
- PyYAML
- cfn-lint

## 4. Main Features

### Automated Security Alerting
Detects selected suspicious API activities and publishes notifications through SNS.

### S3 Remediation
Enables all four S3 Block Public Access settings.

### Security Group Remediation
Removes internet-wide inbound IPv4 and IPv6 CIDR entries while preserving restricted CIDR entries.

### Incident Response Runbooks
Provides procedures for detection, analysis, containment, eradication, recovery and manual intervention.

### NIST Lifecycle Mapping
Maps incident response activities to the NIST incident response lifecycle.

## 5. Project Structure

```text
Cloud-Incident-Response/
|
|-- cloudformation/
|   |-- main.yaml
|
|-- lambda/
|   |-- alert_handler/
|   |   |-- app.py
|   |-- s3_remediation/
|   |   |-- app.py
|   |-- security_group_remediation/
|       |-- app.py
|
|-- runbooks/
|   |-- s3_data_leak.md
|   |-- security_group_exposure.md
|
|-- tests/
|   |-- mock_cloud.py
|   |-- test_alert_handler.py
|   |-- test_remediation.py
|
|-- documentation/
|   |-- architecture.md
|   |-- nist_mapping.md
|   |-- test_results.md
|
|-- screenshots/
|   |-- alert_handler_test.png
|   |-- cloudformation_validation.png
|   |-- project_structure.png
|   |-- project_structure(1).png
|   |-- project_structure(2).png
|   |-- pytest_results.png
|   |-- s3_remediation_test.png
|   |-- security_group_remediation_test.png
|
|-- requirements.txt
|-- README.md
|-- .gitignore
```

## 6. Installation

Clone or download the project repository.

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 7. Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

Latest local test result:

**11 tests passed, 0 failed.**

## 8. CloudFormation Validation

Validate the template using:

```bash
cfn-lint cloudformation/main.yaml
```

Validation result: Exit code 0, with no lint errors reported.

The template contains **19 CloudFormation resources and 6 outputs**.

## 9. Security and Limitations

- The project was developed and tested locally.
- Moto was used to simulate AWS services.
- No live AWS infrastructure was deployed.
- Live CloudTrail, EventBridge, Lambda and SNS integration has not been verified.
- Production deployment requires IAM permission review, resource scoping, event-filter validation, monitoring and operational safeguards.

## 10. Future Enhancements

- Live AWS deployment and integration testing.
- Additional incident detection rules.
- More automated remediation playbooks.
- Centralized incident logging and reporting.
- Security dashboards and notification improvements.

## 11. Conclusion

The project demonstrates how cloud monitoring, automated alerting and remediation can support structured security incident response.

It combines AWS infrastructure definitions, Python Lambda functions, local testing and NIST-aligned runbooks to provide a foundation for cloud security incident management.