import boto3
import copy
import sys
import time
from botocore.exceptions import ClientError
import config

table_names = config.TABLE_NAMES
table_infos = config.TABLE_INFO

client = boto3.client('dynamodb')

def delete_table(table_name):
    response = client.delete_table(TableName=table_name)
    return response


def create_table(table_name, att_def, key_schema):
    throughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }

    response = client.create_table(
        AttributeDefinitions=att_def,
        TableName=table_name,
        KeySchema=key_schema,
        ProvisionedThroughput=throughput
    )
    return response

def reset_table(table_names, table_infos):
    att_lst = copy.deepcopy(table_infos)
    key_lst = copy.deepcopy(table_infos)

    # Remove KeyType in attribute list
    for table_att in range(0, len(att_lst)):
        for attribute in att_lst[table_att]:
            if 'KeyType' in attribute:
                attribute.pop('KeyType')

    # Remove any attribute without KeyType, then remove AttributeType
    for table_att in range(0, len(key_lst)):
        for attribute in key_lst[table_att]:
            if 'KeyType' not in attribute:
                key_lst[table_att].remove(attribute)
                continue
            attribute.pop('AttributeType')

    print("=== Deleting Table ===")
    # Remove all tables
    for table in table_names:
        try:
            delete_response = delete_table(table)
            print("Deleting table {}".format(table))
        except ClientError:
            print("{} is non-existent".format(table))
        except:
            print("Unexpected error:")
            print(sys.exc_info())
            return False

    # Buffer time to delete table
    try:
        delete_response
    except:
        print("No table to be deleted, continuing to create tables")
    else:
        print("Buffer deletion for 10s")
        time.sleep(10)


    print("=== Creating Table ===")
    # Create tables
    for table in range(0, len(table_names)):
        try:
            create_table(table_names[table], att_lst[table], key_lst[table])
            print("Creating new table {}".format(table_names[table]))
        except:
            print("Unexpected error:")
            print(sys.exc_info())
            return False

    # Buffer time to create table
    print("Buffer for 10s")
    time.sleep(10)
    print("New tables ready")
    return True
