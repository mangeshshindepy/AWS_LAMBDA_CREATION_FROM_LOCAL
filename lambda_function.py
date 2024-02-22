import boto3
import zipfile
import os

# Your AWS credentials
AWS_ACCESS_KEY_ID = 'AKIAZHUXVDY7XT3CNLXF'
AWS_SECRET_ACCESS_KEY = 'Bu4aAdNq4hs2tM1uILQKTQWF9EH4XpsZkPLKN7z1'
AWS_REGION = 'ap-southeast-1'  # Replace with your desired AWS region

# Define your Lambda function code
lambda_function_code = """
def lambda_handler(event, context):
    print("Hello from Lambda!")
    return {
        'statusCode': 200,
        'body': 'Hello Arjun!'
    }
"""

# Zip the Lambda function code
with zipfile.ZipFile('lambda_function.zip', 'w') as zipf:
    zipf.writestr('lambda_function.py', lambda_function_code)

# Create Lambda client
lambda_client = boto3.client('lambda', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)

# Create Lambda function
with open('lambda_function.zip', 'rb') as f:
    response = lambda_client.create_function(
        FunctionName='Testlocallambda',
        Runtime='python3.8',
        Role='arn:aws:iam::634899471935:role/eve_dev_data_onboarding_role',  # Replace with your IAM role ARN
        Handler='lambda_function.lambda_handler',
        Code={
            'ZipFile': f.read()
        }
    )

# Execute Lambda function
response = lambda_client.invoke(
    FunctionName='Testlocallambda',
    InvocationType='RequestResponse'
)

print(response['Payload'].read().decode('utf-8'))
