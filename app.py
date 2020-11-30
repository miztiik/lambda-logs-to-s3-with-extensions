#!/usr/bin/env python3

from aws_cdk import core

from lambda_logs_to_s3_with_extensions.lambda_logs_to_s3_with_extensions_stack import LambdaLogsToS3WithExtensionsStack


app = core.App()
LambdaLogsToS3WithExtensionsStack(app, "lambda-logs-to-s3-with-extensions")

app.synth()
