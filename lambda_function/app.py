import boto3
import json

def lambda_handler(event, context):

# Define AWS resources used

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('visitor_counter')

# Check if table has already had values written by "except"

    try:
        response = table.get_item(
            Key = {'visitor_counter': 'count'},
            ProjectionExpression = 'visitors'
        ) 

# If table has already been accessed, retrieve counter value...

        onlyValue = response.get('Item')
        previousCount = int(onlyValue.get('visitors'))

# ...then increment the counter by 1.

        response = table.update_item(
            Key = {'visitor_counter': 'count'},
            UpdateExpression = 'SET visitors = :increase',
            ExpressionAttributeValues = {
                ':increase': (previousCount + 1)
            }
        )

# If table has not been accessed, give a counter value of "1" and set table up so that "try" block will work next time

    except:
        table.put_item(
            Item={
            'visitor_counter': 'count',
            'visitors': 1}
        )

        previousCount = 0

# Return the value

    newCount = int(previousCount + 1)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(newCount)
        }