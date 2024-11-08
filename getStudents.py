import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize a DynamoDB resource object for the specified region
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')

# Select the DynamoDB table named 'studentData'
table = dynamodb.Table('studentData')

def lambda_handler(event, context):
    
    http_method = event.get('httpMethod', 'GET')
    logger.info("#### http_method event #### - %s" % http_method)
    if http_method == 'GET':
        # Scan the table to retrieve all items
        response = table.scan()

        data = response['Items']
        
        # If there are more items to scan, continue scanning until all items are retrieved
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        # Return the retrieved data
        return data
    elif http_method == 'POST':
        # Extract values from the event object we got from the Lambda service and store in variables
        student_id = event['studentid']
        name = event['name']
        student_class = event['class']
        age = event['age']

        # Write student data to the DynamoDB table and save the response in a variable
        response = table.put_item(
            Item={
                'studentid': student_id,
                'name': name,
                'class': student_class,
                'age': age
            }
        )
        
        # Return a properly formatted JSON object
        return {
            'statusCode': 200,
            'body': json.dumps('Student data saved successfully!')
        }