import json
import boto3
import botocore

# Initialization of AWS
rekognition_client = boto3.client('rekognition')
s3_client = boto3.client('s3')
bedrock_client = boto3.client('bedrock-runtime')

# Services imports
from src.services.detect_faces_service import DetectFacesService
from src.services.detect_pets_faces_service import DetectPetsFacesService

def v2Vision(event, context):
    try:
        # Body request
        body = json.loads(event['body'])
        bucket_name = body['bucket']
        image_name = body['imageName']

        # Init services
        detect_faces_service = DetectFacesService(s3_client, rekognition_client)
        detect_pets_faces_service = DetectPetsFacesService(s3_client, rekognition_client, bedrock_client)
        
        # Init face rekognition service
        faces_response_body = detect_faces_service.process_image(bucket_name, image_name)
        
        # Init pet rekognition service
        pets_response_body = detect_pets_faces_service.process_image(bucket_name, image_name)

        # Format response body
        response_body = {
            "url_to_image": faces_response_body["url_to_image"],
            "created_image": faces_response_body["created_image"],
            "faces": faces_response_body["faces"],
            "pets": pets_response_body["pets"]
        }

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
