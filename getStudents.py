import json
import boto3

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
table = dynamodb.Table('studentData')

def lambda_handler(event, context):
    # Determine the HTTP method from the event
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        # Handle the GET request: Scan the table to retrieve all items
        response = table.scan()
        data = response['Items']
        
        # Continue scanning if there are more items to retrieve
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        
        # Return the retrieved data
        return {
            'statusCode': 200,
            'body': json.dumps(data)
        }
    
    elif http_method == 'POST':
        # Handle the POST request: Extract values and insert a new item
        student_id = event['studentid']
        name = event['name']
        student_class = event['class']
        age = event['age']
        
        # Write student data to the DynamoDB table
        response = table.put_item(
            Item={
                'studentid': student_id,
                'name': name,
                'class': student_class,
                'age': age
            }
        )
        
        # Return a success message
        return {
            'statusCode': 200,
            'body': json.dumps('Student data saved successfully!')
        }
    
    else:
        # Handle unsupported HTTP methods
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported HTTP method')
        }
