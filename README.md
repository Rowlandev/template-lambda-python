# Template AWS Lambda Function: Python

A template for an AWS Lambda Function written in Python.

---

## Publish Docker Image to AWS ECR

To publish this to ECR, after you've created the repository as `<lambda function name>`, use the following command:

```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your aws account id>.dkr.ecr.us-east-1.amazonaws.com

docker build --platform linux/x86_64 -t docker-image:<lambda function name> .;

docker tag docker-image:<lambda function name> <your aws account id>.dkr.ecr.us-east-1.amazonaws.com/<lambda function name>:latest;

docker push <your aws account id>.dkr.ecr.us-east-1.amazonaws.com/<lambda function name>:latest;
```

You may need to also update your AWS Lambda Function after, to ensure it's using the latest image version.

