
import json
import os
import boto3


SUSPICIOUS_EVENTS = {
    "PutBucketPolicy",
    "PutBucketAcl",
    "DeletePublicAccessBlock",
    "AuthorizeSecurityGroupIngress",
    "ModifySecurityGroupRules",
}


def lambda_handler(event, context):
    """
    Detect suspicious CloudTrail API events
    and publish security alerts through SNS.
    """

    detail = event.get("detail", {})
    event_name = detail.get("eventName", "Unknown")
    username = detail.get("userIdentity", {}).get(
        "userName", "Unknown"
    )

    if event_name not in SUSPICIOUS_EVENTS:
        return {
            "statusCode": 200,
            "body": json.dumps("No suspicious activity detected.")
        }

    message = {
        "alert": "Suspicious AWS API activity detected",
        "event_name": event_name,
        "username": username,
        "region": detail.get("awsRegion", "Unknown"),
        "source_ip": detail.get("sourceIPAddress", "Unknown"),
        "event_time": detail.get("eventTime", "Unknown")
    }

    topic_arn = os.environ.get("SNS_TOPIC_ARN")

    if not topic_arn:
        raise ValueError("SNS_TOPIC_ARN environment variable is missing")

    sns = boto3.client(
        "sns",
        region_name=os.environ.get("AWS_REGION", "ap-south-1")
    )

    sns.publish(
        TopicArn=topic_arn,
        Subject="Cloud Security Alert",
        Message=json.dumps(message, indent=4)
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Security alert published successfully.")
    }
