import json
import boto3
import botocore

# Initialization of AWS
rekognition = boto3.client('rekognition')
s3_client = boto3.client('s3')

# Service import
from src.services.detect_faces_service import DetectFacesService

def v1Vision(event, context):
    try:
        # Body request
        body = json.loads(event['body'])
        bucket_name = body['bucket']
        image_name = body['imageName']

        # Init face rekognition service
        detect_faces = DetectFacesService(s3_client, rekognition)
        
        # Process image
        response_body = detect_faces.process_image(bucket_name, image_name)

        # Convert to JSON
        response_json = json.dumps(response_body)

        # Log to CloudWatch
        print(response_json)

        # Return success response
        return {
            'statusCode': 200,
            'body': response_json
        }

    except botocore.exceptions.ClientError as e:
        # Client error AWS (S3 or Rekognition)
        error_message = f'AWS Client Error: {str(e)}'
        print(error_message)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }

    except Exception as e:
        # Other errors
        error_message = f'Internal Server Error: {str(e)}'
        print(error_message)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_message})
        }
