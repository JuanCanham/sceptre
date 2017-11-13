import os
from awscli.customizations.cloudformation.artifact_exporter import Template, EXPORT_DICT
from awscli.customizations.cloudformation.yamlhelper import yaml_parse, yaml_dump
from awscli.customizations.s3uploader import S3Uploader


class SamTemplate(Template):
    """
    Class to export a CloudFormation template
    """

    def __init__(self, stack):
        """
        Reads the template and makes it ready for export
        """
        s3_client = stack.connection_manager._get_client("s3")

        s3_bucket = stack.environment_config["template_bucket_name"]
        template_prefix = [
            stack.region,
            stack.environment_config.environment_path,
            stack.template.name
        ]

        if "template_key_prefix" in stack.environment_config:
            template_prefix.insert(0, stack.environment_config["template_key_prefix"])

        template_key_prefix = "/".join(template_prefix)

        self.uploader = S3Uploader(s3_client,
                                   s3_bucket,
                                   stack.region,
                                   template_key_prefix,
                                   stack.environment_config.get("kms_key_id", None),
                                   True)

        self.template = stack.template
        self.template_dict = yaml_parse(self.template.body)
        self.template_dir = os.path.dirname(self.template.path)
        self.resources_to_export = EXPORT_DICT

    def export(self):
        self.template_dict = super(SamTemplate, self).export()
        self.template._body = yaml_dump(self.template_dict)
