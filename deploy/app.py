import aws_cdk as cdk

from stacks.config import cfg

app = cdk.App()
cdk_env = cdk.Environment(region=cfg.AWS_REGION, account=cfg.AWS_ACCOUNT)

# TODO stacks

app.synth()
