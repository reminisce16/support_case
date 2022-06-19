import boto3

def desribe_case(support_client):
    response = support_client.describe_cases()
    print(response)
def get_sts_token():
    sts_client = boto3.client('sts')
    role_session_name = "cross_cases_session"
    assumed_role_object=sts_client.assume_role(
        RoleArn="arn:aws:iam::366935765673:role/SupportECR",
        RoleSessionName=role_session_name
    )
    ACCESS_KEY    = assumed_role_object['Credentials']['AccessKeyId']
    SECRET_KEY    = assumed_role_object['Credentials']['SecretAccessKey']
    SESSION_TOKEN = assumed_role_object['Credentials']['SessionToken']
    
    support_resources=boto3.client(
        'Support',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
    print(support_resources)
    #return support_resources
def main():
    get_sts_token()