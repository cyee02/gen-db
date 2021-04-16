import pandas as pd
import random
import string
import boto3
import sys

# Initialize boto3 client
dynamo = boto3.resource('dynamodb')
table_name = 'TT4_Login'
table = dynamo.Table(table_name)

# Variables
pass_len = 15
LETTERS = string.ascii_letters
LETTERS_LOWER = string.ascii_lowercase
NUMBERS = string.digits
PUNCTUATION = "!$%&_"
# create alphanumerical from string constants
printable = list(f'{LETTERS}{NUMBERS}{PUNCTUATION}')
printable_lower = list(f'{LETTERS_LOWER}{NUMBERS}')


# Generate userPass
def gen_password(num_cust_id):
    pass_lst = []
    for row in range(0, num_cust_id):
        random_password = []
        for char in range(0, pass_len):
            random_password.append(random.choice(printable))
        random_password = ''.join(random_password)
        pass_lst.append(random_password)
    return pass_lst


# Generate userName
def gen_username(num_cust_id):
    username_lst = []
    for num in range(1, num_cust_id+1):
        username_lst.append("Group" + str(num))
    return(username_lst)


# Generate accountKey
def gen_accountKey(num_cust_id):
    sequence = [8, 4, 4, 4, 11]
    key_lst = []
    for row in range(0, num_cust_id):
        random_password = []
        for num in sequence:
          seq = ''.join(random.choices(printable_lower, k=num))
          random_password.append(seq)
        random_password = '-'.join(random_password)
        key_lst.append(random_password)
    return key_lst


# Create pandas dataframe
def create_df(num_cust_id):
    data = {}
    data["custID"] = range(1, num_cust_id+1)
    data["userName"] = gen_username(num_cust_id)
    data["userPass"] = gen_password(num_cust_id)
    data["accountKey"] = gen_accountKey(num_cust_id)
    return pd.DataFrame(data=data)


# Generate random variables and push to AWS dynamoDB
def create(num_cust_id):
    df = create_df(num_cust_id)
    np = df.to_numpy()

    # Write row by row to dynamoDB
    np = df.to_numpy()
    try:
        for row in np:
            item = {
                'custID': row[0],
                'userName': row[1],
                'userPass': row[2],
                'accountKey': row[3]
            }
            table.put_item(Item=item)
        print("Write to {}: Success".format(table_name))
    except:
        e = sys.exc_info()
        print(e)
        print("Write to {}: Fail".format(table_name))

    # Create local csv copy
    df.to_csv("./database/Login.csv", index=False)
    print("Exported Login.csv: Success")
