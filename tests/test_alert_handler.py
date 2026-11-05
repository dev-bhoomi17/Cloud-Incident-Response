
import json
import os
import boto3
import importlib

from moto import mock_aws

alert_handler = importlib.import_module(
    "lambda.alert_handler.app"
).lambda_handler


@mock_aws
def test_suspicious_event_sends_alert(monkeypatch):
    sns = boto3.client("sns", region_name="ap-south-1")
    sqs = boto3.client("sqs", region_name="ap-south-1")

    # Create SNS topic
    topic = sns.create_topic(Name="security-alerts")
    topic_arn = topic["TopicArn"]

    # Create SQS queue
    queue = sqs.create_queue(QueueName="security-alert-queue")
    queue_url = queue["QueueUrl"]

    queue_arn = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]

    # Allow SNS to send messages to SQS
    sqs.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={
            "Policy": json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "sns.amazonaws.com"},
                    "Action": "sqs:SendMessage",
                    "Resource": queue_arn,
                    "Condition": {
                        "ArnEquals": {
                            "aws:SourceArn": topic_arn
                        }
                    }
                }]
            })
        }
    )

    # Subscribe SQS queue to SNS topic
    sns.subscribe(
        TopicArn=topic_arn,
        Protocol="sqs",
        Endpoint=queue_arn
    )

    monkeypatch.setenv("SNS_TOPIC_ARN", topic_arn)

    event = {
        "detail": {
            "eventName": "PutBucketPolicy",
            "userIdentity": {"userName": "test-user"},
            "awsRegion": "ap-south-1",
            "sourceIPAddress": "192.0.2.10",
            "eventTime": "2026-11-05T10:00:00Z"
        }
    }

    result = alert_handler(event, None)

    assert result["statusCode"] == 200

    # Receive the actual SNS notification from SQS
    received = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )

    assert "Messages" in received

    notification = json.loads(
        received["Messages"][0]["Body"]
    )

    alert_message = json.loads(notification["Message"])

    assert alert_message["event_name"] == "PutBucketPolicy"
    assert alert_message["username"] == "test-user"
    assert alert_message["source_ip"] == "192.0.2.10"


def test_normal_event_is_ignored():
    event = {
        "detail": {
            "eventName": "DescribeInstances"
        }
    }

    result = alert_handler(event, None)

    assert result["statusCode"] == 200
    assert "No suspicious activity" in json.loads(result["body"])
