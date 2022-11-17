import json
import uuid
import os;
import boto3;


snsTopicArn = region = os.environ['TargetSnsTopicArn']

snsClient = boto3.client('sns')

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    order = json.loads(event["body"])
    order = processorder(order)
    orderId = order['orderId']
    print(order)
    print('publishing order with Id {0} to sns topic.', orderId)
    publish_to_topic(order)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "order placed sucessfully.",
            "orderId": orderId
        }),
    }


def processorder(order):
    orderId = str(uuid.uuid4())
    order["orderId"] = orderId
    print(orderId)
    return order

def publish_to_topic(order):
    response = snsClient.publish(
        TargetArn = snsTopicArn,
        Message = json.dumps({'default': json.dumps(order)}),
        MessageStructure = 'json'
    )
    print(response)


