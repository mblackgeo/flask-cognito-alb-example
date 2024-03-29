# Flask - Load Balancer + Cognito integration example

An example of an Application Load Balanced Fargate service deployed in Elastic Container Service (ECS) using [Flask](https://flask.palletsprojects.com/en/2.0.x/) with [AWS Cognito](https://aws.amazon.com/cognito/) applied to the Load Balancer.

* [`home`](src/webapp/home/routes.py): a simple homepage.
* [`auth`](src/webapp/auth/routes.py): routes to check user info from Cognito, verify the JWT and logout.

When accessing the the application, the load balancer will redirect a user to the Cognito hosted UI. After successful authentication with the user pool, the Load Balancer will set a new JSON Web Token (JWT) which can be verified through the `/verify` endpoint. Note that the [ALB sets this JWT](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html) in the HTTP header `x-amzn-oidc-data`, and this is not the same JWT that Cognito would issue. 

For the deployment side, [CDK](https://aws.amazon.com/cdk/) python code is provided in [`/deploy`](/deploy/app.py). The CDK stacks will deploy the Flask application as a [docker container](Dockerfile) to ECS (backed by Fargate), with an Application Load Balancer in front. A Cognito User Pool is created along with a User Pool Client for the load balancer.

## Getting started

Prequisites:

* [poetry](https://python-poetry.org/)
* [pre-commit](https://pre-commit.com/)
* [AWS CDK](https://aws.amazon.com/cdk/) (v2.15.0)

Setup as follows:

```shell
# setup the python environment with poetry
make install

# Populate the .env file the required parameters
cp .env.example .env
vi .env

# deploy the infra (Cognito, API Gateway, Lambda)
cd deploy
cdk deploy --all

# Populate AWS_COGNITO user pool parameters after deploying
# Obtain these values from the Systems Manager Parameter Store
vi .env

# run locally using Workzeug
make local  # or go to the AWS API Gateway URL

# check other useful commands
make help
```

The [Makefile](Makefile) includes helpful commands for setting up a development environment, get started by installing the package into a new virtual environment and setting up pre-commit with `make install`. Run `make help` to see additional available commands (e.g. linting, testing, docker, and so on).

The application can be run locally through docker (`make docker-build && make docker-run`) or from the installed virtualenv with `make local`. The app should launched at [http://localhost:5000](http://localhost:5000) and ALB/Cognito integration is not applied when running locally, ideal for building, developing and debugging the app locally without needed to provision any infrastructure in AWS or worry about the authentication/authorisation flow.


## Development

* [Pytest](https://docs.pytest.org/en/6.2.x/) is used for the functional tests of the application (see `/tests`).
* Code is linted using [flake8](https://flake8.pycqa.org/en/latest/)
* Code formatting is validated using [Black](https://github.com/psf/black)
* [pre-commit](https://pre-commit.com/) is used to run these checks locally before files are pushed to git
* The [Github Actions pipeline](.github/workflows/pipeline.yml) also runs these checks and tests


## TODO

- [ ] Separate out the monitlitic CDK stack
- [ ] Add a route that verifies the claims with the Cognito user pool directly (e.g. to get a list of Cognito groups for the user)
