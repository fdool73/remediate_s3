#!/usr/bin/env python3
'''Invoke S3 Bucket Remediation Lambda function

This function will scan all S3 buckets in the 
selected region to check if they are encrypted. If
an unencrypted S3 bucket is found it is encrypted
with default AES256 encryption. If the default AES256
is not sufficient this will need to be adjusted. See
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_encryption
'''

import boto3
import logging
import json
import os
import botocore.exceptions as bce

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    '''lambda handler function

    Args:
        event (dict):   Dictionary with event information
    
    Returns:
        (json):         HTML status and message
    '''
    if 'Enable' in event:
        encrypt = True
    else:
         encrypt = False
        
    if 'Region' in event:
        region = event['Region']
    else:
        region = os.environ['AWS_DEFAULT_REGION']   #assumes environment variable AWS_DEFAULT_REGION is set locally

    print(get_bucket_encryption(region, encrypt))   #main function entrypoint prints response to stdout

def get_bucket_encryption(region, encrypt):
    client = boto3.client('s3', region_name=region)
    for each in client.list_buckets()['Buckets']:
        bucketname = each.get('Name')
        print('S3 bucket name: ', bucketname)
        try:
            sse_rules = client.get_bucket_encryption(Bucket=bucketname).get('ServerSideEncryptionConfiguration')['Rules']
        except:
            sse_rules = []

        is_enabled = False
        for i in sse_rules:
            if i['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] != '':
                is_enabled = True
                print(bucketname + ' is encrypted')
                logger.info(bucketname + ' is encrypted')
        
        if not is_enabled:
            print('** Need to remediate**')
            try:
                if encrypt == True:
                    response = client.put_bucket_encryption(
                        Bucket=bucketname,
                        ServerSideEncryptionConfiguration={
                            'Rules': [
                                {
                                    'ApplyServerSideEncryptionByDefault': {
                                        'SSEAlgorithm': 'AES256'
                                    }
                                }
                            ]
                        }
                    )
                    print(bucketname + ' was encrypted with AES256')
                    return json.dumps(response['ResponseMetadata'])
                    
                elif encrypt == False:
                    print('Encryption remediation skipped')
                    logger.info('Encryption remediation skipped')
            except bce.ClientError as error:
                raise(error)

