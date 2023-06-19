import boto3
from botocore.exceptions import ClientError
from retry import retry


class ItemOutdatedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


@retry(ItemOutdatedException, tries=5, delay=2, max_delay=4)
def write_item(number):
    dynamodb = boto3.resource("dynamodb", "us-east-1")

    # Instantiate a table resource object without actually
    # creating a DynamoDB table. Note that the attributes of this table
    # are lazy-loaded: a request is not made nor are the attribute
    # values populated until the attributes
    # on the table resource are accessed or its load() method is called.
    table = dynamodb.Table("TableName")
    response = table.get_item(Key={"id": "4c8613b9-2874-42e6-abf2-898c80bb5979"})
    item = response["Item"]
    try:
        size = len(item["docs"])
        item["docs"].append(number)
        response = table.update_item(
            Key={
                "id": item["id"],
            },
            UpdateExpression="SET docs = :docs",
            ConditionExpression="size(docs) = :size",
            ExpressionAttributeValues={":docs": item["docs"], ":size": size},
            ReturnValues="UPDATED_NEW",
        )

        print("Update response", response)

    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            print(e.response["Error"])
            raise ItemOutdatedException(e)


@retry(ItemOutdatedException, tries=5, delay=0.1)
def write_item_with_error(number):
    raise ItemOutdatedException("some")


def handle_with_error():
    try:
        write_item_with_error(1)
    except ItemOutdatedException:
        raise Exception("should return 5xx")
