import boto3

def lambda_handler(event, context):

# Define AWS resources used

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('visitor_counter')

# Obtain the previous value of the visitor counter from the DynamoDB table

    response = table.get_item(
	    Key = {'counters': 'visitor_counter'},
	    ProjectionExpression = 'visitor_count'
	    )

    onlyValue = response.get('Item')
    previousCount = int(onlyValue.get('visitor_count'))

# Increment the DynamoDB table by 1 and return the new value

    response = table.update_item(
        Key = {'counters': 'visitor_counter'},
        UpdateExpression = 'SET visitor_count = :increase',
        ExpressionAttributeValues = {
            ':increase': (previousCount + 1)
        }
    )

    return previousCount + 1