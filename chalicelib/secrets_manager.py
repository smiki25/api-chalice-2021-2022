# Use this code snippet in your app.Z
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/
import json
import boto3

from botocore.exceptions import ClientError


def get_secret():
    secret_name = "arn:aws:secretsmanager:us-east-2:322321537707:secret:JWT_SECRET_KEY-7ZF1Q6"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        secret = get_secret_value_response['SecretString']

    if secret:
        secret = json.loads(secret)

    return secret["JWT_SECRET_KEY"]