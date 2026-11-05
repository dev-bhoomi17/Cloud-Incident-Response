class MockS3Bucket:
    def __init__(self, name, public=False):
        self.name = name
        self.public = public
        self.block_public_access = not public

    def enable_block_public_access(self):
        self.block_public_access = True
        self.public = False


class MockSecurityGroup:
    def __init__(self, group_id, open_to_world=False):
        self.group_id = group_id
        self.open_to_world = open_to_world

    def restrict_public_access(self):
        self.open_to_world = False


class MockCloudEnvironment:
    def __init__(self):
        self.buckets = {}
        self.security_groups = {}

    def add_bucket(self, bucket):
        self.buckets[bucket.name] = bucket

    def add_security_group(self, security_group):
        self.security_groups[security_group.group_id] = security_group


import yaml


class CloudFormationLoader(yaml.SafeLoader):
    pass


def cloudformation_tag_constructor(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)

    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)

    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)

    return None


CloudFormationLoader.add_multi_constructor(
    "!",
    cloudformation_tag_constructor
)
