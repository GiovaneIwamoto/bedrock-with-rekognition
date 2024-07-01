class DetectFacesService:
    def __init__(self, s3_client, rekognition_client):
        self.s3_client = s3_client
        self.rekognition = rekognition_client

    def process_image(self, bucket_name, image_name):
        
        # Calling Rekognition to detect faces in the image
        response = self.rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': image_name}}, Attributes=['ALL'])

        # Image metadata
        response_metadata = self.s3_client.head_object(Bucket=bucket_name, Key=image_name)
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
        creation_time = response_metadata['LastModified'].strftime('%d-%m-%Y %H:%M:%S')

        # Processing the detected faces
        faces = self.process_faces(response)

        # Response body
        response_body = {
            "url_to_image": image_url,
            "created_image": creation_time,
            "faces": faces
        }

        return response_body

    def process_faces(self, response):
        faces = []
        if 'FaceDetails' in response:
            for faceDetail in response['FaceDetails']:
                face = {
                    "position": {
                        "Height": float(faceDetail["BoundingBox"]["Height"]),
                        "Left": float(faceDetail["BoundingBox"]["Left"]),
                        "Top": float(faceDetail["BoundingBox"]["Top"]),
                        "Width": float(faceDetail["BoundingBox"]["Width"])
                    },
                    "classified_emotion": faceDetail["Emotions"][0]["Type"],
                    "classified_emotion_confidence": float(faceDetail["Emotions"][0]["Confidence"])
                }
                faces.append(face)

        # Case no faces detected
        if not faces:
            faces = [{
                "position": {
                    "Height": None,
                    "Left": None,
                    "Top": None,
                    "Width": None
                },
                "classified_emotion": None,
                "classified_emotion_confidence": None
            }]

        return faces
