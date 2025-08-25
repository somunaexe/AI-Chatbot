import json, boto3, time, random, os

dynamo = boto3.resource("dynamodb")
table = dynamo.Table(os.environ["TABLE_NAME"])

bedrock = boto3.client("bedrock-runtime")
MODEL_ID = os.environ["MODEL_ID"]

def save_message(userId, role, text):
    table.put_item(Item={
        "userId": userId,
        "timestamp": int(time.time()),
        "role": role,
        "message": text
    })


def get_messages(userId, limit=10):
    resp = table.query(
        KeyConditionExpress = "userId = :uid",
        ExpressionAttributeValues = {":uid": userId},
        Limit = limit
    )
    return resp["Items"]


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    userId = body.get("userId", f"guest-{random.randint(100,900)}")
    role = body.get("role", "sender")
    user_message = body.get("message", "")

    save_message(userId, "user", user_message)
    save_message(userId, "bot", "Hello, I’m your bot!")

    history = get_messages(userId)
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"reply": response})
    }


