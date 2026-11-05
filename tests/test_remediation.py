import importlib
import boto3
from moto import mock_aws

from tests.mock_cloud import (
    MockS3Bucket,
    MockSecurityGroup
)

s3_handler = importlib.import_module(
    "lambda.s3_remediation.app"
).lambda_handler

sg_handler = importlib.import_module(
    "lambda.security_group_remediation.app"
).lambda_handler


def test_s3_public_bucket_remediation():
    bucket = MockS3Bucket("test-bucket", public=True)

    result = s3_handler({"bucket": bucket}, None)

    assert result["statusCode"] == 200
    assert bucket.public is False
    assert bucket.block_public_access is True


def test_s3_already_private():
    bucket = MockS3Bucket("private-bucket", public=False)

    result = s3_handler({"bucket": bucket}, None)

    assert result["statusCode"] == 200
    assert bucket.public is False


def test_s3_missing_bucket():
    result = s3_handler({}, None)

    assert result["statusCode"] == 400


def test_security_group_remediation():
    group = MockSecurityGroup("sg-12345", open_to_world=True)

    result = sg_handler({"security_group": group}, None)

    assert result["statusCode"] == 200
    assert group.open_to_world is False


def test_security_group_already_restricted():
    group = MockSecurityGroup("sg-67890", open_to_world=False)

    result = sg_handler({"security_group": group}, None)

    assert result["statusCode"] == 200
    assert group.open_to_world is False


def test_security_group_missing():
    result = sg_handler({}, None)

    assert result["statusCode"] == 400

@mock_aws
def test_aws_s3_public_access_remediation():
    s3 = boto3.client("s3", region_name="ap-south-1")

    s3.create_bucket(
        Bucket="aws-test-bucket",
        CreateBucketConfiguration={
            "LocationConstraint": "ap-south-1"
        }
    )

    result = s3_handler(
        {"bucket": "aws-test-bucket"},
        None
    )

    config = s3.get_public_access_block(
        Bucket="aws-test-bucket"
    )

    assert result["statusCode"] == 200
    assert config["PublicAccessBlockConfiguration"] == {
        "BlockPublicAcls": True,
        "IgnorePublicAcls": True,
        "BlockPublicPolicy": True,
        "RestrictPublicBuckets": True
    }

@mock_aws
def test_aws_security_group_remediation():
    ec2 = boto3.client("ec2", region_name="ap-south-1")

    # Create a simulated VPC
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]

    # Create a security group
    group = ec2.create_security_group(
        GroupName="test-security-group",
        Description="Test public security group",
        VpcId=vpc_id
    )

    group_id = group["GroupId"]

    # Add an internet-wide inbound rule
    ec2.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [
                    {"CidrIp": "0.0.0.0/0"}
                ]
            }
        ]
    )

    # Execute remediation
    result = sg_handler(
        {"groupId": group_id},
        None
    )

    # Verify public inbound rule was removed
    updated_group = ec2.describe_security_groups(
        GroupIds=[group_id]
    )["SecurityGroups"][0]

    assert result["statusCode"] == 200
    assert updated_group["IpPermissions"] == []

@mock_aws
def test_security_group_preserves_restricted_cidr():
    ec2 = boto3.client("ec2", region_name="ap-south-1")

    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]

    group = ec2.create_security_group(
        GroupName="mixed-access-group",
        Description="Test mixed CIDR rules",
        VpcId=vpc_id
    )

    group_id = group["GroupId"]

    # Add both public and restricted IPv4 ranges
    ec2.authorize_security_group_ingress(
        GroupId=group_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [
                    {"CidrIp": "0.0.0.0/0"},
                    {"CidrIp": "10.0.0.0/24"}
                ]
            }
        ]
    )

    result = sg_handler({"groupId": group_id}, None)

    updated_group = ec2.describe_security_groups(
        GroupIds=[group_id]
    )["SecurityGroups"][0]

    remaining_ranges = (
        updated_group["IpPermissions"][0]["IpRanges"]
    )

    assert result["statusCode"] == 200
    assert {"CidrIp": "10.0.0.0/24"} in remaining_ranges
    assert {"CidrIp": "0.0.0.0/0"} not in remaining_ranges