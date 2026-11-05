
import boto3


def lambda_handler(event, context):
    """
    Restrict overly permissive security groups.

    Supports both local mock testing and AWS Lambda execution.
    """

    security_group = event.get("security_group") or event.get("groupId")

    if not security_group:
        return {
            "statusCode": 400,
            "message": "Security group is required."
        }

    # Local simulation mode
    if not isinstance(security_group, str):
        if not security_group.open_to_world:
            return {
                "statusCode": 200,
                "message": (
                    f"Security group {security_group.group_id} "
                    "is already restricted."
                )
            }

        security_group.restrict_public_access()

        return {
            "statusCode": 200,
            "message": (
                f"Public access restricted for "
                f"{security_group.group_id}."
            ),
            "open_to_world": security_group.open_to_world
        }

    # Actual AWS mode
    ec2 = boto3.client(
        "ec2",
        region_name=boto3.session.Session().region_name or "ap-south-1"
    )

    response = ec2.describe_security_groups(
        GroupIds=[security_group]
    )

    for group in response["SecurityGroups"]:
        for permission in group.get("IpPermissions", []):

            # Identify only internet-wide IPv4 and IPv6 ranges
            public_ipv4 = [
                item for item in permission.get("IpRanges", [])
                if item.get("CidrIp") == "0.0.0.0/0"
            ]

            public_ipv6 = [
                item for item in permission.get("Ipv6Ranges", [])
                if item.get("CidrIpv6") == "::/0"
            ]

            if public_ipv4 or public_ipv6:

                # Build a permission containing only public ranges
                revoke_permission = {
                    "IpProtocol": permission["IpProtocol"]
                }

                for key in ("FromPort", "ToPort"):
                    if key in permission:
                        revoke_permission[key] = permission[key]

                if public_ipv4:
                    revoke_permission["IpRanges"] = public_ipv4

                if public_ipv6:
                    revoke_permission["Ipv6Ranges"] = public_ipv6

                ec2.revoke_security_group_ingress(
                    GroupId=security_group,
                    IpPermissions=[revoke_permission]
                )

    return {
        "statusCode": 200,
        "message": (
            f"Public ingress access restricted for {security_group}."
        )
    }