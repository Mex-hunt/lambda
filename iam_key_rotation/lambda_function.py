import boto3
import datetime

def lambda_handler(event, context):
    # create an IAM client object
    iam_client = boto3.client('iam')
    # create a paginator object for listing IAM users
    paginator = iam_client.get_paginator('list_users')
    # iterate over the IAM users using the paginator
    response_iterator = paginator.paginate()

    # loop through each IAM user
    for page in response_iterator:
        for user_data in page['Users']:
            # get the user name
            user_name = user_data['UserName']
            # get the metadata for the user's access keys
            access_key_metadata = iam_client.list_access_keys(UserName=user_name)

            if len(access_key_metadata['AccessKeyMetadata']) > 0:
                # sort the access keys by creation date, oldest to newest
                access_key_metadata['AccessKeyMetadata'].sort(key=lambda x: x['CreateDate'])
                # get the ID of the oldest access key
                oldest_access_key_id = access_key_metadata['AccessKeyMetadata'][0]['AccessKeyId']
                # check if the oldest access key is older than 93 days
                create_date_str = access_key_metadata['AccessKeyMetadata'][0]['CreateDate'].strftime('%Y-%m-%d %H:%M:%S')
                create_date = datetime.datetime.strptime(create_date_str, '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.utcnow()
                age = now - create_date
                if age.days > 93:
                    # delete the old access key
                    iam_client.delete_access_key(AccessKeyId=oldest_access_key_id, UserName=user_name)
                    # create a new access key
                    response = iam_client.create_access_key(UserName=user_name)
                    new_access_key_id = response['AccessKey']['AccessKeyId']
                    new_secret_access_key = response['AccessKey']['SecretAccessKey']
            else:
                # create a new access key for the user
                response = iam_client.create_access_key(UserName=user_name)
                new_access_key_id = response['AccessKey']['AccessKeyId']
                new_secret_access_key = response['AccessKey']['SecretAccessKey']

    # return a response indicating success
    return {
        'statusCode': 200,
        'body': 'Access keys rotated successfully for all IAM users'
    }

    
