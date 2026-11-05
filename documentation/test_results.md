# Cloud Security Incident Response – Test Results

## 1. Testing Environment

- Operating System: Windows 11
- Python Version: 3.12.6
- Testing Framework: pytest
- AWS Simulation: Moto
- Infrastructure Validation: cfn-lint
- CloudFormation YAML Parsing: PyYAML

## 2. Automated Test Results

The project contains 11 automated tests.

| Test Case | Result |
|---|---|
| Suspicious API event sends SNS alert | PASS |
| Normal API event is ignored | PASS |
| Public S3 bucket remediation | PASS |
| Already-private S3 bucket | PASS |
| Missing S3 bucket input | PASS |
| Public security group remediation | PASS |
| Already-restricted security group | PASS |
| Missing security group input | PASS |
| AWS-compatible S3 remediation using Moto | PASS |
| AWS-compatible security group remediation using Moto | PASS |
| Restricted CIDR preservation | PASS |

## 3. Latest Test Execution

Command:

`python -m pytest -v`

Result:

- Total tests: 11
- Passed: 11
- Failed: 0
- Execution time: 8.25 seconds

## 4. CloudFormation Validation

Command:

`cfn-lint cloudformation/main.yaml`

Result:

- Exit code: 0
- No lint errors reported.

Additional YAML inspection confirmed:

- Total CloudFormation resources: 19
- Dedicated test security group: Present
- CloudFormation outputs: 6

## 5. Security Testing

The tests verify that:

- S3 Public Access Block settings are enabled.
- Unrestricted security group ingress ranges are removed.
- Restricted CIDR ranges are preserved.
- Suspicious API activity generates an SNS notification.
- Normal API activity is ignored.
- Missing inputs are handled safely.

## 6. Testing Limitations

Testing was performed locally using Moto and mock objects.

No real AWS deployment was performed. Therefore, live CloudTrail event delivery, EventBridge rule matching, Lambda execution in AWS, IAM authorization and external SNS delivery still require verification in an AWS environment.

## 7. Conclusion

All 11 automated tests passed, and the CloudFormation template passed cfn-lint validation. The project demonstrates locally tested alerting and automated remediation workflows for common cloud security misconfigurations.