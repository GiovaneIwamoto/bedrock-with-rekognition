import json

def v1_description(event, context):
    body = {
        "message": "Vision api version 1."
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response

def v2_description(event, context):
    body = {
        "message": "Vision api version 2."
    }
    response = {"statusCode": 200, "body": json.dumps(body)}
    return response