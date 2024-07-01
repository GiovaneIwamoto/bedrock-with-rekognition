import json
import botocore

class DetectPetsFacesService:
    def __init__(self, s3_client, rekognition_client, bedrock_client):
        self.s3_client = s3_client
        self.rekognition_client = rekognition_client
        self.bedrock_client = bedrock_client

    # Formatting the prompt to be sent to Bedrock
    def prompt_format(self, breed):
        prompt = f"""
        For the {breed} pet breed, complete the following information on the topics presented in detail and in the format as presented.
        
        Tips about {breed}: 
        Energy Level and Exercise Needs: 
        Temperament and Behavior: 
        Care and Needs: 
        Common Health Problems:
        """
        return prompt
    
    # Definition of the request body for the Bedrock API
    def bedrock_api_request_body(self, prompt):
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 8192,
                "temperature": 0.25,
                "topP": 1
            }
        }
        return json.dumps(body)

    # Function to get Bedrock tips based on the animal's breed
    def get_animal_tips(self, breed):
        try:
            prompt = self.prompt_format(breed)
            
            # Invoke model bedrock
            response = self.bedrock_client.invoke_model(
                modelId='amazon.titan-text-express-v1',
                contentType='application/json',
                body=self.bedrock_api_request_body(prompt)
            )
            
            bedrock_response = json.loads(response["body"].read().decode('utf-8'))
            if "results" in bedrock_response and bedrock_response["results"]:
                return bedrock_response["results"][0]["outputText"]
            return None
        
        except botocore.exceptions.EndpointConnectionError:
            return "Bedrock connection error"
        
        except botocore.exceptions.ClientError as e:
            return f"Bedrock client error: {str(e)}"
        
        except Exception as e:
            return f"Unknown error when getting Bedrock tips: {str(e)}"

    # Function to extract animal characteristics based on labels
    def extract_animal_characteristics(self, labels):
        characteristics = []
        for label in labels:
            if any(parent.get("Name") in ["Pet"] for parent in label.get("Parents", [])):
                if label["Name"].lower() not in ["dog", "cat", "fish", "bird", "reptile", "mammal", "canine", "kitten"]:
                    characteristics.append(label)
        return characteristics

    # Function to assemble pet information from the extracted characteristics
    def assemble_pet_info(self, characteristics):
        pet_info = {"labels": []}
        for label in characteristics:
            pet_info["labels"].append({
                "Confidence": label["Confidence"],
                "Name": label["Name"]
            })
        return pet_info
    
    # Process the image and return information about the animals
    def process_image(self, bucket_name, image_name):
        response_labels = self.rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': image_name}},
            MaxLabels=50
        )
        
        # Processing detected labels
        animal_characteristics = self.extract_animal_characteristics(response_labels["Labels"])
        
        # Structure to store information about pets
        pets_info = self.assemble_pet_info(animal_characteristics)
        
        # Getting the first race detected to search for tips in Bedrock
        breed = pets_info["labels"][0]["Name"] if pets_info["labels"] else None
        
        # Adding tips to the pets_info object if there is an identified breed
        if breed:
            dicas = self.get_animal_tips(breed)
            pets_info["Dicas"] = dicas

        # Construindo o corpo da resposta
        response_body = {
            "pets": [pets_info]  
        }

        return response_body
