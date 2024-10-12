FROM public.ecr.aws/lambda/python:3.9

# You don't actually have to copy everything.
# Feel free to only copy the files you need.
COPY . .

RUN  pip3 install -r requirements.txt --target .

CMD [ "lambda_function.lambda_handler" ]