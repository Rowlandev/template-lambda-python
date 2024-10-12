from inspect import currentframe
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from datetime import datetime
from pytz import timezone

deserializer = TypeDeserializer()
serializer = TypeSerializer()


def unmarshall(dynamo_item):
    """
    - Convert a DynamoDB item into a Python dictionary.
    - Makes DynamoDB items a bit easier to use.
    - a.k.a. deserialize
    :param dynamo_item: The DynamoDB item.
    :return: A Python dictionary from a DynamoDB item.
    """
    return {k: deserializer.deserialize(v) for k, v in dynamo_item.items()}


def marshall(obj):
    """
    - Convert a Python dictionary into a DynamoDB item.
    - Prevents you from having to prepare dictionaries for entry into DynamoDB yourself.
    - a.k.a. serialize.
    :param obj: The Python dictionary.
    :return: A DynamoDB item from a Python dictionary.
    """
    return {k: serializer.serialize(v) for k, v in obj.items()}


def meta_print(var):
    """
    - Prints a variable name and its contents.
    :param var: The variable being printed.
    :return: Absolutely nothing.
    """
    caller_frame = currentframe().f_back
    var_name = [name for name, value in caller_frame.f_locals.items() if value is var][0]
    print(f"{{{var_name}: {var}}}")


def now(code: str = 'America/Chicago') -> datetime:
    """
    Returns the current time.
    :param code: The timezone for the time being returned (CST, by default).
    :return: The current time in a particular time zone.
    """
    return datetime.now(timezone(code))