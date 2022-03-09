import aws_cdk as cdk

from stacks.config import cfg
from stacks.ecs_cognito_stack import ECSCognitoStack

app = cdk.App()
cdk_env = cdk.Environment(region=cfg.AWS_REGION, account=cfg.AWS_ACCOUNT)

ECSCognitoStack(app, f"{cfg.NAMESPACE}-stack", env=cdk_env)

app.synth()
