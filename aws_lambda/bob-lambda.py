import json

import boto3

# Get the service resource.
# dynamodb = boto3.client('dynamodb-local', endpoint_url='http://localhost:8000')


# For a Boto3 client ('client' is for low-level access to Dynamo service API)
# ddb1 = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2')
# response = ddb1.list_tables()
# print(response)

print('Loading function...')

# For a Boto3 service resource ('resource' is for higher-level, abstracted access to Dynamo)
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

print(f'\n\n==================== Tables in DynamoDB: ====================\n')
for table in dynamodb.tables.all():
    print(table.name)


# bob_ddb_table_name = 'bob-ddb'
# bob_ddb_partition_key = 'command_id'


# partition_value = 'todo'

##############################################################################
#                              Helper Functions                              #
##############################################################################


def get_table_resource(table_name):
    """
    Get a DynamoDB _table resource.
    :param table_name: The name of the _table.
    :return: The _table resource.
    """
    return dynamodb.Table(table_name)


def print_table(_table_resource):
    if _table_resource is None:
        print("Table is None.")
        return

    print(f'\n\n==================== Table `{_table_resource.name}` ====================\n')

    print(f'Items: {json.dumps(_table_resource.scan()["Items"], indent=2)}')


##############################################################################
#                              Main Functions                                #
##############################################################################

def create_new_table(table_name=None, rcu=1, wcu=1, pk_attribute_name=None, pk_attribute_type=None, pk_key_type=None,
                     sk_attribute_name=None, sk_attribute_type=None, sk_key_type=None):
    """
    Create a new DynamoDB _table.
    :param table_name: The name of the table.
    :param rcu: Read capacity units. (The maximum number of strongly consistent reads per second.)
    :param wcu: Write capacity units. (The maximum number of writes per second.)
    :param pk_attribute_name: The name of the primary key attribute. (e.g. 'id')
    :param pk_attribute_type: The type of the primary key attribute. ('S': String, 'N': Number, 'B': Binary)
    :param pk_key_type: The key type of the primary key attribute. (must be 'HASH' for primary key)
    :param sk_attribute_name: The name of the sort key attribute. (e.g. 'timestamp')
    :param sk_attribute_type: The type of the sort key attribute. ('S': String, 'N': Number, 'B': Binary)
    :param sk_key_type: The key type of the sort key attribute. (must be 'RANGE' for sort key)
    :return:
    """

    print(f'\n\n==================== Creating Table `{table_name}` ====================\n')

    # Raise an error if any of the required parameters are missing.
    if not all([table_name, rcu, wcu, pk_attribute_name, pk_attribute_type, pk_key_type]):
        raise ValueError('Missing required parameters. (_table_resource, rcu, wcu, pk_attribute_name, '
                         'pk_attribute_type, pk_key_type)')

    # Raise an error if the _table already exists.
    if table_name in [_table.name for _table in dynamodb.tables.all()]:
        delete_table(table_name)  # TODO: replace with: `raise ValueError(f'Table {_table_resource} already exists.')`

    # Create the key schema and attribute definitions.
    key_schema = [{'AttributeName': pk_attribute_name, 'KeyType': pk_key_type}]
    attribute_definitions = [{'AttributeName': pk_attribute_name, 'AttributeType': pk_attribute_type}]

    if all([sk_attribute_name, sk_attribute_type, sk_key_type]) not in [None, '']:
        key_schema.append({'AttributeName': sk_attribute_name, 'KeyType': sk_key_type})
        attribute_definitions.append({'AttributeName': sk_attribute_name, 'AttributeType': sk_attribute_type})

    # Create the DynamoDB _table.
    _table = dynamodb.create_table(TableName=table_name, KeySchema=key_schema,
                                   AttributeDefinitions=attribute_definitions,
                                   ProvisionedThroughput={'ReadCapacityUnits': rcu, 'WriteCapacityUnits': wcu})

    # Wait until the _table exists.
    _table.wait_until_exists()

    # Print out some data about the _table.
    _table = dynamodb.Table(table_name)
    print(f'Provisioned Throughput: {_table.provisioned_throughput}')
    print(f'Table Status: {_table.table_status}')
    print(f'Number of Items: {_table.item_count}')

    return _table


def delete_table(table_name):
    """
    Delete a DynamoDB _table.
    :param table_name: The name of the _table to delete.
    :return:
    """
    print(f'\n\n==================== Deleting Table `{table_name}` ====================\n')

    _table = dynamodb.Table(table_name)
    _table.delete()
    _table.wait_until_not_exists()

    return


def put_item(_table, item):
    """
    Create a new item in a DynamoDB table.
    :param _table: The table resource.
    :param item: The item to create.
    :return: The response from the DynamoDB API.
    """

    print(f'\n\n==================== Creating Item in Table `{_table.name}` ====================\n')
    print(f'Item: {item}')
    print(f'Creating item in _table {_table.name}...')

    try:
        response = _table.put_item(Item=item)
        print(f'Item created successfully in _table {_table.name}.')
        print(f'Response: {response}')
    except Exception as e:
        print(f'Error creating item in _table {_table.name}.')
        print(f'Error: {e}')
        raise e

    print_table(_table)

    return response


def get_item(_table, item):
    """
    Get an item from a DynamoDB table.
    :param _table: The table resource.
    :param item: The item to get.
    :return: The response from the DynamoDB API.
    """

    print(f'\n\n==================== Getting Item from Table `{_table.name}` ====================\n')
    print(f'Item: {item}')
    print(f'Getting item from _table {_table.name}...')

    try:
        response = _table.get_item(Key=item)
        print(f'Item retrieved successfully from _table {_table.name}.')
        print(f'Response: {response}')
    except Exception as e:
        print(f'Error retrieving item from _table {_table.name}.')
        print(f'Error: {e}')
        raise e

    print_table(_table)

    return response

def update_item(_table, item):
    """
    Update an item in a DynamoDB table.
    :param _table: The table resource.
    :param item: The item to update.
    :return: The response from the DynamoDB API.

    Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update_item.html
    """

    print(f'\n\n==================== Updating Item in Table `{_table.name}` ====================\n')
    print(f'Item: {item}')
    print(f'Updating item in _table {_table.name}...')

    try:
        response = _table.update_item(Key={'list_type': item['list_type'], 'list_name': item['list_name']},
                                      UpdateExpression="SET list_items = :i",
                                      ExpressionAttributeValues={':i': item['list_items']})
        print(f'Item updated successfully in _table {_table.name}.')
        print(f'Response: {response}')
    except Exception as e:
        print(f'Error updating item in _table {_table.name}.')
        print(f'Error: {e}')
        raise e

    print_table(_table)

    return response


def local_testing():
    t = create_new_table(table_name="dummy_table", rcu=1, wcu=1, pk_attribute_name='list_type', pk_attribute_type='S',
                         pk_key_type='HASH', sk_attribute_name='list_name', sk_attribute_type='S', sk_key_type='RANGE')

    put_item(t, {'list_type': 'todo', 'list_name': 'groceries', 'list_items': ['milk', 'eggs', 'bread']})
    put_item(t, {'list_type': 'todo', 'list_name': 'chores', 'list_items': ['laundry', 'dishes', 'vacuum']})

    get_item(t, {'list_type': 'todo', 'list_name': 'groceries'})
    get_item(t, {'list_type': 'todo', 'list_name': 'chores'})

    update_item(t, {'list_type': 'todo', 'list_name': 'groceries', 'list_items': ['milk', 'eggs', 'bread', 'cheese']})
    
    delete_table('dummy_table')


local_testing()

# def respond(err, res=None):
#     return {
#         'statusCode': '400' if err else '200',
#         'body': err.message if err else json.dumps(res),
#         'headers': {
#             'Content-Type': 'application/json',
#         },
#     }
#

# def lambda_handler(event, context):
#     '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
#     access to the request and response payload, including headers and
#     status codeself.
#
#     To scan a DynamoDB _table, make a GET request with the TableName as a
#     query string parameter. To put, update, or delete an item, make a POST,
#     PUT, or DELETE request respectively, passing in the payload to the
#     DynamoDB API as a JSON body.
#     '''
#     print("Received event: " + json.dumps(event, indent=2))
#
#     def validate_item(item):
#         # Implement item validation logic here
#         pass
#
#     operations = {
#         'DELETE': lambda dynamo, x: delete_item(dynamo, x),
#         'GET': lambda dynamo, x: get_item(dynamo, x),
#         # 'POST': lambda dynamodb, x: create_item(dynamodb, x),
#         'POST': lambda event: add_todo_item(event),
#         'PUT': lambda dynamo, x: update_item(dynamo, x),
#     }
#
#     def add_todo_item(event):
#         new_item = json.loads(event['body'])
#         response = dynamodb.update_item(
#             TableName=bob_ddb_table_name,
#             Key={bob_ddb_partition_key: {'S': partition_value}},
#             UpdateExpression="SET todo = list_append(todo, :i)",
#             ExpressionAttributeValues={
#                 ':i': {'L': [{'S': new_item}]}
#             },
#             ReturnValues="UPDATED_NEW"
#         )
#
#     return respond(None, response)
#
#     # POST operation
#     def create_item(dynamo, item):
#         validate_item(item)
#         # Check for duplicates, implement logic based on your requirements
#         return dynamo.put_item(
#             TableName='bob-ddb',
#             Item=item)
#
#     # PUT operation
#     def update_item(dynamo, item):
#         validate_item(item)
#         # Additional logic to check if item exists
#         return dynamo.update_item(TableName='bob-ddb', Key=item['key'], AttributeUpdates=item['updates'])
#
#     # DELETE operation
#     def delete_item(dynamo, key):
#         # Additional logic to check if item exists
#         return dynamo.delete_item(TableName='bob-ddb', Key=key)
#
#     #     'DELETE': lambda dynamodb, x: dynamodb.delete_item(**x),
#     #     'GET': lambda dynamodb, x: dynamodb.query(
#     #             TableName=x['TableName'],
#     #             KeyConditionExpression='command_id = :command_id',
#     #             ExpressionAttributeValues={
#     #                 ':command_id': {'S': x['command_id']}
#     #             }
#     #         ),
#     #     'POST': lambda dynamodb, x: dynamodb.put_item(**x),
#     #     'PUT': lambda dynamodb, x: dynamodb.update_item(**x),
#     # }
#
#     operation = event['httpMethod']
#     if operation in operations:
#         payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
#         return respond(None, operations[operation](dynamodb, payload))
#     else:
#         return respond(ValueError('Unsupported method "{}"'.format(operation)))
