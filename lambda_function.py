from traceback import format_exc
from boto3 import client
from functions import meta_print, marshall, now
from aws_lambda_powertools.utilities.idempotency import (DynamoDBPersistenceLayer, IdempotencyConfig, idempotent_function)

# We declare the AWS clients outside the function handler in the hope that it's occasionally reused across invocations.
# We can't really control it, but we can give Lambda a chance to reuse our client.
# The benefit of this approach is even more evident when you make database connections from Lambda Functions.
# Your clients/database will thank you later. As will your wallet.
dynamo_client = client('dynamodb')
result_table_name = '<whatever you wish to call your table for execution results>'

# https://docs.powertools.aws.dev/lambda/dotnet/utilities/idempotency/
# The value doesn't matter; it just needs to reference an existing DynamoDB table.
# Make sure the partition key of the table is `id: string`.
# I recommend making this table's billing mode on demand. Go serverless.
idempotency_table_name = 'idempotent-store'
persistence = DynamoDBPersistenceLayer(table_name=idempotency_table_name)
config = IdempotencyConfig()


@idempotent_function(data_keyword_argument='record', persistence_store=persistence, config=config)
def process(record):
    """
    - Separated from the function handler to make it easier to add idempotency and error handling for each record.
    :param record: A single record from many; could be from services like SNS, SQS, EventBridge, etc.
    :return: Absolutely nothing.
    """
    meta_print(record)

    start_time = now()
    error = ''
    try:
        meta_print(record)
        print('Doing whatever you need to do for each record...')
    except Exception as exception:
        error = str(exception) + '\n' + format_exc()

    end_time = now()
    item = {
        'your_partition_key': '<literally anything>',
        'maybe_even_a_sort_key': '<literally anything again, but sorted>',
        'duration': str(end_time - start_time),
        'end_time': str(end_time),
        'error': error
    }
    dynamo_client.put_item(TableName=result_table_name, Item=marshall(item))


def lambda_handler(event, context):
    message = ''
    try:
        request = [event, context]
        meta_print(request)

        config.register_lambda_context(context)  # You'll need this for idempotency to not give you a warning. Or a howler.

        records = event.get('Records') or []
        for record in records:
            process(record=record)  # Make sure you pass the argument by name for idempotency to work properly.

        record_count = len(records)
        message = f'Successfully processed {record_count} records.'
    except Exception as exception:
        message = str(exception) + '\n' + format_exc()

    print(message)

    return message
