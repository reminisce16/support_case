import boto3

def desribe_case(support_client):
    response = support_client.describe_cases()
    print(response)
def listBucket(support_resources):
    for bucket in support_resources.buckets.all():
        print(bucket.name)
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
    print(ACCESS_KEY)
    print(SECRET_KEY)
    print(SESSION_TOKEN)
    
    support_resources=boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
    return support_resources
def main():
    support_resources=get_sts_token()
    listBucket(support_resources=support_resources)

if __name__ == '__main__':
    main()