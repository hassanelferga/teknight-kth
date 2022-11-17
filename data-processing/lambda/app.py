import json



def lambda_handler(event, context):
    for record in event['Records']:
        order = json.loads(record['Sns']['Message'])
        print(order)
        print('processing order event with id ', order['orderId'])
        print('sending to data platform')