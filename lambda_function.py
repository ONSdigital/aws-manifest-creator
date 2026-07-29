import json

def lambda_handler(event, context):
    return {
        'status_code': 200,
        'body': json.dumps('Hello from Lambda!')
    }