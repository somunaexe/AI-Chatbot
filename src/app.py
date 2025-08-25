import json, boto3, time

dynamo = boto3.resource("dynamodb")
table = dynamo.Table("RMAI-Chat-Messages")

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    message = body.get("message", "")

    response = f"You said: {message}" if message else "Wagwan"

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"reply": response})
    }


