import pandas as pd
import random
import boto3
import sys

# Initialize boto3 client
dynamo = boto3.resource('dynamodb')
table_name = 'TT4_BankInfo'
table = dynamo.Table(table_name)

# 0:accountName 1:custId 2:linked
def gen_accname_custid_linked(num_rows, num_cust_id):
    account_name = []
    cust_id = []
    linked=[]

    curr_id = 0
    mult_id = 0
    sav_id = 0
    for num in range(1, num_rows + 1):
        if num <= num_cust_id:
            curr_id += 1
            cust_id.append(curr_id)
            account_name.append("Current Account")
            linked.append(False)
        elif num <= num_cust_id*2:
            mult_id += 1
            cust_id.append(mult_id)
            account_name.append("Multiplier Account")
            linked.append(random.choice([True, False]))
        elif num <= num_cust_id*3:
            sav_id += 1
            cust_id.append(sav_id)
            account_name.append("Saving Account")
            linked.append(random.choice([True, False]))
    return [account_name, cust_id, linked]


def gen_acc_number(num_rows):
    account_number = []
    # Generate 8 digit account number
    for num in range(0, num_rows):
        account_number.append(random.randint(10000000, 99999999))
    return account_number


def gen_balance(num_rows):
    available_bal = []
    for num in range(0, num_rows):
        available_bal.append('%.2f'%(random.random()*10000.00))
    return available_bal


# Write to csv
def create_df(num_cust_id):
    account_types = 3
    num_rows = num_cust_id * account_types
    account = gen_accname_custid_linked(num_rows, num_cust_id)

    data = {}
    data["bankInfoID"] = range(1, num_rows + 1)
    data["accountName"] = account[0]
    data["accountNumber"] = gen_acc_number(num_rows)
    data["availableBal"] = gen_balance(num_rows)
    data["custID"] = account[1]
    data["linked"] = account[2]

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
                'bankInfoID': row[0],
                'accountName': row[1],
                'accountNumber': row[2],
                'availableBal': row[3],
                'custID': row[4],
                'linked': row[5]
            }
            table.put_item(Item=item)
        print("Write to {}: Success".format(table_name))
    except:
        e = sys.exc_info()
        print(e)
        print("Write to {}: Fail".format(table_name))

    # Create local csv copy
    df.to_csv("./database/BankInfo.csv", index=False)
    print("Exported BankInfo.csv: Success")
