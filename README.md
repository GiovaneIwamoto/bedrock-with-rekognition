# BEDROCK WITH REKOGNITION

### **OVERVIEW**

The objective of this project is to create an API using the serverless framework, which will receive images manually uploaded to an Amazon S3 bucket, and utilize the Amazon Rekognition service to identify people's faces and their emotions. Additionally, it will also identify pets and provide care tips for them through integration with the Amazon Bedrock service. Throughout this process, logs will be sent to Amazon CloudWatch.

[![My Skills](https://skillicons.dev/icons?i=aws,py,postman&theme=dark)](https://skillicons.dev)

---

### **ARCHITECTURE**

![alt text](/assets/architecture.png)

---

### **AWS SERVICES**

> [!WARNING]
> It is imperative for users to deploy their own application on AWS using their own credentials to ensure compliance and security. This ensures that users have full control over their application's environment and data, facilitating customization and enhancing security measures.

- **Amazon Rekognition**

A powerful image analysis service that uses deep learning technology to identify objects, people, text, scenes, and activities. In this project, AWS Rekognition is employed to detect faces and analyze the emotions displayed in the images. The service is capable of identifying a range of emotions, such as happiness, sadness, anger, and more, with high accuracy. Additionally, AWS Rekognition is used to detect pets and classify their breeds, providing a robust foundation for further processing and analysis.

- **Amazon Bedrock**

The project utilizes Amazon _Titan-Text-Express-V1_, an advanced generative AI tool, to enhance its capability in generating specific care tips based on the detected breed of the pet. _Titan-Text-Express-V1_ employs state-of-the-art natural language processing (NLP) models to create human-like text responses, ensuring that the generated tips are not only accurate but also contextually relevant to the pet's breed characteristics.

---

### **FUNCTIONALITIES**

- **Facial and Pet Recognition**

The facial and pet recognition functionality identifies both human faces and their apparent emotions in a photo, as well as pets, and provides specific care tips for the detected pet breeds.

| Method | Endpoint                                                    | Description                |
| ------ | ----------------------------------------------------------- | -------------------------- |
| POST   | https://xxxxx.execute-api.us-east-1.amazonaws.com/v1/vision | Rekognition for faces only |
| POST   | https://xxxxx.execute-api.us-east-1.amazonaws.com/v2/vision | Rekognition faces and pets |

> [!TIP]
> To utilize the API, the following JSON format must be used for POST requests. This format specifies the necessary details for the API to access and process the images stored in your S3 bucket:

```JSON
{
    "bucket": "my_bucket_s3",
   "imageName": "image_example.jpg"
}
```

> [!NOTE]
> Users are required to create their own Amazon S3 bucket and manually upload photos to this bucket. The API will utilize the photos stored in this user-created bucket for processing.

The expected response format is as follows:

```JSON
{
   "url_to_image": "https://myphotos/test.jpg",
   "created_image": "02-02-2023 17:00:00",
   "faces": [
     {
      "position":
      {
       "Height": 0.06333330273628235,
       "Left": 0.1718519926071167,
       "Top": 0.7366669774055481,
       "Width": 0.11061699688434601
      }
      "classified_emotion": "HAPPY",
      "classified_emotion_confidence": 99.92965151369571686
     }
   ],
   "pets": [
      {
      "labels": [
      {
         "Confidence": 96.59198760986328,
         "Name": "Animal"
      },
      {
         "Confidence": 96.59198760986328,
         "Name": "Dog"
      },
      {
         "Confidence": 96.59198760986328,
         "Name": "Pet"
      },
      {
         "Confidence": 96.59198760986328,
         "Name": "Golden Retriever"
      }
      ],
      "Tips": "Tips about Golden Retriever: Golden retrievers are known for their love of water and enjoy swimming and playing in the water.

        Energy Level and Exercise Needs: Golden retrievers are high-energy dogs that require regular exercise and playtime to stay healthy and happy.
        Temperament and Behavior: Golden retrievers are known for their friendly and outgoing temperament.
        Care and Needs: Golden retrievers require regular grooming to keep their coats healthy and free from tangles.
        Common Health Problems: Hip dysplasia: This is a common condition in Golden Retrievers where the hip joints don't fit properly, causing pain and lameness."
      }
   ]
}
```

> [!IMPORTANT]
> If there are timeout errors in the request, ensure that the Lambda function generated by Serverless named _vision-dev-visionV2_ has enough timeout to run the AWS Rekognition and Bedrock services.

---

### **INSTALLATION GUIDE**

- Configure your AWS credentials managed by IAM:

```javascript
$ aws configure
AWS Access Key ID [None]: ACCESSKEYEXAMPLE
AWS Secret Access Key [None]: SECRETKEYEXAMPLE
Default region name [None]: us-east-1
Default output format [None]: ENTER
```

> [!CAUTION]
> Credentials should remain local to your environment only. Never expose your credentials in any part of the code, such as in source files, comments, or commit history. Instead, use environment variables or secure secret management tools to manage and access your credentials securely.

- Install Serverless and deploy:

```ruby
$ npm install -g serverless
$ cd .\api\
$ serverless deploy
```

---

### **AUTHORS**

[Giovane Iwamoto](https://github.com/GiovaneIwamoto) | [Gustavo Vasconcelos](https://github.com/GustavoSVasconcelos) | [Renan Mazzilli](https://github.com/renan-mazzilli) | [Thomaz Casquel](https://github.com/Casquel)

Giovane Hashinokuti Iwamoto - Computer Science student at UFMS - Brazil - MS

I am always open to receiving constructive criticism and suggestions for improvement in my developed code. I believe that feedback is an essential part of the learning and growth process, and I am eager to learn from others and make my code the best it can be. Whether it's a minor tweak or a major overhaul, I am willing to consider all suggestions and implement the changes that will benefit my code and its users.
