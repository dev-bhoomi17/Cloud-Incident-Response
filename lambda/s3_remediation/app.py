
import boto3


def lambda_handler(event, context):
    """
    Block public access to an S3 bucket.
    Supports local simulation and AWS execution.
    """

    bucket = event.get("bucket") or event.get("bucketName")

    if not bucket:
        return {
            "statusCode": 400,
            "message": "Bucket name is required."
        }

    # Local simulation
    if not isinstance(bucket, str):
        if not bucket.public:
            return {
                "statusCode": 200,
                "message": f"Bucket {bucket.name} is already private."
            }

        bucket.enable_block_public_access()

        return {
            "statusCode": 200,
            "message": f"Public access blocked for bucket {bucket.name}.",
            "public": bucket.public,
            "block_public_access": bucket.block_public_access
        }

    # AWS execution
    s3 = boto3.client("s3")

    s3.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        }
    )

    return {
        "statusCode": 200,
        "message": f"Public access blocked for bucket {bucket}."
    }
