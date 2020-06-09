import boto3
import botocore
import requests

# Invokes the Lambda function
lambda_client = boto3.client('lambda', 
	region_name='us-west-1',
	)
lambda_response = lambda_client.invoke(
	FunctionName="sam-app-CountUpdaterFunction-LK1JG5VM5BAP",
	InvocationType='RequestResponse',
	)
lambda_metadata = lambda_response.get('ResponseMetadata')

# Performs a GET request on the API
api_response = requests.get('https://kesy6eh1ce.execute-api.us-west-1.amazonaws.com/prod/proxy')
api_statuscode = str(api_response)

# Retrieves the value of the visitor counter from the DynamoDB table
dynamodb_resource = boto3.resource('dynamodb', region_name='us-west-1')
dynamodb_table = dynamodb_resource.Table('visitor_counter')
dynamodb_response = dynamodb_table.get_item(
    Key = {'visitor_counter': 'count'},
    ProjectionExpression = 'visitors'
)
item_response = dynamodb_response.get('Item')

# PyTest tests
def test_lambda_status_code():
	assert lambda_metadata.get('HTTPStatusCode') == 200

def test_api_status_code():
	assert api_statuscode == '<Response [200]>'

def test_table():
	assert int(item_response.get('visitors')) == int(api_response.text)