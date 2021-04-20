# Delete table before putting new items
import pandas as pd
import random
import string
import time
import boto3
import sys
from decimal import Decimal

# Initialize boto3 client
dynamo = boto3.resource('dynamodb')
table_name = 'TT4_Transaction'
table = dynamo.Table(table_name)

# Variables
proximity = 3
categories = ["Transport", "Food", "Shopping", "Entertainment", "Insurance", "Others", "Transfer"]
message = ["Thanks", "Lunch", "Dinner", "thank you", "", "", "", "", "DBS", "Breakfast"]
format = '%d%m%Y%H%M'

# # Generate list of random unique ids
# def gen_transaction_id(num_rows):
#     id_lst = []
#     # Transaction id is 5 digit
#     range_lst = list(range(10000, 100000))

#     # remove id from list so there is no transaction id duplicates
#     for row in range(0, num_rows):
#         id = random.choice(range_lst)
#         range_lst.remove(id)
#         id_lst.append(id)
#     return id_lst


# Generate list of random transaction amount
def gen_amount(proximity, num_rows):
    transaction_lst = []
    for row in range(0, num_rows):
        transaction_lst.append('%.2f'%(random.random()*pow(10, proximity)))
    return transaction_lst


# Generate customer and payee ID
def gen_cp_id(num_cust_id, num_rows):
    cust_lst = []
    payee_lst = []
    cust_ids = list(range(1, num_cust_id+1))

    for row in range(0, num_rows):
        cust_id = random.choice(cust_ids)
        payee_id = random.choice(cust_ids)
        cust_lst.append(cust_id)
        
        # customer id and payee id must not be the same
        while cust_id == payee_id:
            payee_id = random.choice(cust_ids)
            if cust_id != payee_id:
                break
        payee_lst.append(payee_id)

    return [cust_lst, payee_lst]


# Generate a random date within defined range as epoch
def gen_date(start, end, format):
    prop = random.random()
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    # Output as epoch
    ptime = round(stime + prop * (etime - stime))

    # # To output as specific format instead of epoch
    # output_format = '%Y-%m-%dT%H:%M:%S%'
    # output_format = '%d %b %Y %H:%M'
    # ptime = str(time.strftime(output_format, time.localtime(ptime)))

    return ptime


# Generate list of random dates
def gen_date_list(start, end, format, num_rows):
    date_lst = []
    for row in range(0, num_rows):
        date_lst.append(gen_date(start, end, format))
    return date_lst


# Generate random eGift boolean
def gen_egift(num_rows):
    egift_lst = []
    for row in range(0, num_rows):
        egift_lst.append(random.choice([True, False]))
    return egift_lst


# Generate random message from a list
def gen_message(message, num_rows):
    message_lst = []
    for row in range(0, num_rows):
        message_lst.append(random.choice(message))
    return message_lst


# Generate random category from a list
def gen_category(categories, num_rows):
    category_lst = []
    for row in range(0, num_rows):
        category_lst.append(random.choice(categories))
    return category_lst


# Create pandas dataframe
def create_df(start_date, end_date, num_cust_id, num_rows):
    cp = gen_cp_id(num_cust_id, num_rows)
    # Write to csv
    data = {}
    data["transactionID"] = range(1, num_rows+1)
    data["amount"] = gen_amount(proximity, num_rows)
    data["custID"] = cp[0]
    data["datetime"] = gen_date_list(start_date, end_date, format, num_rows)
    data["eGift"] = gen_egift(num_rows)
    data["message"] = gen_message(message, num_rows)
    data["payeeID"] = cp[1]
    data["expenseCat"] = gen_category(categories, num_rows)
    return pd.DataFrame(data=data)


# Generate random variables and push to AWS dynamoDB
def create(start_date, end_date, num_cust_id, num_rows):
    df = create_df(start_date, end_date, num_cust_id, num_rows)

    # Write row by row to dynamoDB
    np = df.to_numpy()
    try:
        for row in np:
            item = {
                'transactionID': row[0],
                'amount': row[1],
                'custID': row[2],
                'datetime': row[3],
                'eGift': row[4],
                'message': row[5],
                'payeeID': row[6],
                'expenseCat': row[7]
            }
            table.put_item(Item=item)
        print("Write to {}: Success".format(table_name))
    except:
        e = sys.exc_info()
        print(e)
        print("Write to {}: Fail".format(table_name))

    # Create local csv copy
    df.to_csv("./database/Transaction.csv", index=False)
    print("Exported Transaction.csv: Success")
