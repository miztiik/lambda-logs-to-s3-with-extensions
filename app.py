#!/usr/bin/env python3

from aws_cdk import core

from lambda_logs_to_s3_with_extensions.lambda_logs_to_s3_with_extensions_stack import LambdaLogsToS3WithExtensionsStack


app = core.App()


# Deploy Lambda Extensions Log API Demonstration
lambda_logs_to_s3_with_extensions = LambdaLogsToS3WithExtensionsStack(
    app,
    f"{app.node.try_get_context('project')}-stack",
    stack_log_level="INFO",
    description="Miztiik Automation: Deploy Lambda Extensions Log API Demonstration"
)




# Stack Level Tagging
_tags_lst = app.node.try_get_context("tags")

if _tags_lst:
    for _t in _tags_lst:
        for k, v in _t.items():
            core.Tags.of(app).add(k, v, apply_to_launched_instances=True)


app.synth()
