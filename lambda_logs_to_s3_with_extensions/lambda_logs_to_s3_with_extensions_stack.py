from aws_cdk import aws_iam as _iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import aws_s3 as _s3
from aws_cdk import core


class GlobalArgs():
    """
    Helper to define global statics
    """

    OWNER = "MystiqueAutomation"
    ENVIRONMENT = "production"
    REPO_NAME = "lambda-logs-to-s3-with-extensions"
    SOURCE_INFO = f"https://github.com/miztiik/{REPO_NAME}"
    VERSION = "2020_12_01"
    MIZTIIK_SUPPORT_EMAIL = ["mystique@example.com", ]


class LambdaLogsToS3WithExtensionsStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct,
        construct_id: str,
        stack_log_level: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # Create an S3 Bucket
        lambda_logs_bkt = _s3.Bucket(
            self,
            "lambdaLogsBkt",
            versioned=True,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Lambda Layer for custom extensions
        lambda_extension_log_layer = _lambda.LayerVersion(
            self, "lambdaExtensionLayer",
            code=_lambda.Code.from_asset(
                "lambda_logs_to_s3_with_extensions/stacks/back_end/lambda_src/layers/extensions_src/extension.zip"),
            compatible_runtimes=[
                _lambda.Runtime.PYTHON_3_8],
            license=f"This layer show how to use lambda extension logs API",
            description="This layer show how to use lambda extension logs API and store them in S3"
        )
        # /lambda-logs-to-s3-with-extensions/lambda_logs_to_s3_with_extensions/stacks/back_end/lambda_src/layer_code/extensions.zip
        # Read Lambda Code:)
        try:
            with open("lambda_logs_to_s3_with_extensions/stacks/back_end/lambda_src/handler/lambda_logs_to_s3_with_extension.py",
                      encoding="utf-8",
                      mode="r"
                      ) as f:
                greeter_fn_code = f.read()
        except OSError:
            print("Unable to read lambda function code")
            raise

        roleStmt1 = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=[f"*"],
            actions=['s3:GetObject',
                     's3:PutObject']
        )
        roleStmt1.sid = "AllowS3ObjectReadWriteAccess"
        greeter_fn = _lambda.Function(
            self,
            "greeterFn",
            # function_name=f"greeter_fn_{id}",
            function_name=f"greeter_fn",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_logs_to_s3_with_extension.lambda_handler",
            # code=_lambda.InlineCode(greeter_fn_code),
            code=_lambda.Code.asset(
                "lambda_logs_to_s3_with_extensions/stacks/back_end/lambda_src/handler"),
            layers=[lambda_extension_log_layer],
            current_version_options={
                "removal_policy": core.RemovalPolicy.DESTROY,  # Remove old versions
                "retry_attempts": 1,
                "description": "Mystique Factory Build Version"
            },
            timeout=core.Duration.seconds(60),
            reserved_concurrent_executions=10,
            environment={
                "LD_LIBRARY_PATH": "/opt/python",
                "LOG_LEVEL": f"{stack_log_level}",
                "Environment": "Production",
                "ANDON_CORD_PULLED": "False",
                "RANDOM_SLEEP_ENABLED": "False",
                "RANDOM_SLEEP_SECS": "2",
                "LAMBDA_LOGS_BKT": f"{lambda_logs_bkt.bucket_name}"},
            description="A simple greeter function, which responds with a timestamp"
        )

        greeter_fn.add_to_role_policy(roleStmt1)

        # Create Custom Log group
        greeter_fn_lg = _logs.LogGroup(
            self,
            "greeterFnLogGroup",
            log_group_name=f"/aws/lambda/{greeter_fn.function_name}",
            retention=_logs.RetentionDays.ONE_DAY,
            removal_policy=core.RemovalPolicy.DESTROY
        )

        ###########################################
        ################# OUTPUTS #################
        ###########################################
        output_0 = core.CfnOutput(
            self,
            "AutomationFrom",
            value=f"{GlobalArgs.SOURCE_INFO}",
            description="To know more about this automation stack, check out our github page."
        )

        output_1 = core.CfnOutput(
            self,
            "GreeterFunction",
            value=f"https://console.aws.amazon.com/lambda/home?region={core.Aws.REGION}#/functions/{greeter_fn.function_name}",
            description="Access the function from here and invoke it."
        )

        output_2 = core.CfnOutput(
            self,
            "LambdaLogsS3Bucket",
            value=f"https://s3.console.aws.amazon.com/s3/buckets/{lambda_logs_bkt.bucket_name}",
            description="Access the lambda logs stored in this s3 bucket."
        )
