import os
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timezone, timedelta
from operator import itemgetter

from dotenv import load_dotenv
load_dotenv()


def get_date():
    return datetime.now().astimezone(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d %H:%M:%S')

import boto3
session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

dynamo_resource = session.resource('dynamodb', region_name=os.getenv("AWS_REGION"))


from functools import lru_cache

@lru_cache(maxsize=1)
def db_get_items(table_name, caching_aux):
    
    table = dynamo_resource.Table(table_name)
    
    response = table.scan()
    data = response['Items']
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return sorted(data, key=itemgetter('date'), reverse=True)

def db_get_items_by_query(table_name, key, value):
    
    table = dynamo_resource.Table(table_name)
    
    response = table.query(
    KeyConditionExpression=Key(key).eq(value)
    )
    return response['Items']

def db_put_item(payload, table_name, date=True):
    
    table = dynamo_resource.Table(table_name)
    
    if date:
        payload['date'] = get_date()
    
    response = table.put_item(Item=payload)
    
    return None
