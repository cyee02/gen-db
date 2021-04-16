from faker import Faker
import names
import pandas as pd
import random
import string
import boto3
import sys

# Initialize boto3 client
dynamo = boto3.resource('dynamodb')
table_name = 'TT4_Users'
table = dynamo.Table(table_name)

fake = Faker()

# Variables
gender = ["male", "female"]
email_provider = ["gmail", "yahoo", "hotmail"]
age_range = range(22, 91)


def gen_email(first_name):
    provider = random.choice(email_provider)
    return first_name.lower() + "@" + provider + ".com"

# 0: First name 1: Last name 2: Gender 3: email
def gen_name_gender_email(num_cust_id):
    first_name_lst = []
    last_name_lst = []
    gender_lst = []
    email_lst = []
    for row in range(0, num_cust_id):
        # Gender
        choose_gender = random.choice(gender)
        gender_lst.append(choose_gender.capitalize())

        # Name
        name = names.get_full_name(gender=choose_gender)
        name = name.split()
        first_name_lst.append(name[0])
        last_name_lst.append(name[1])

        # Email
        email_lst.append(gen_email(name[0]))
    return [first_name_lst, last_name_lst, gender_lst, email_lst]


def gen_address(num_cust_id):
    address_lst = []
    for row in range(0, num_cust_id):
        address_lst.append(fake.address())
    return address_lst


# 0: nric 1: age
def gen_nric(num_cust_id, current_year):
    last_letter = list(f'{"ABCDEFGHIZJ"}')
    nric_lst = []
    age_lst = []
    for row in range(0, num_cust_id):
        # Age
        age = random.choice(age_range)
        age_lst.append(age)

        # nric
        first_two_digit = current_year - age - 1900
        nric = "S" + str(first_two_digit) + str(random.randint(10000, 99999)) + random.choice(last_letter)
        nric_lst.append(nric)
    return [nric_lst, age_lst]


def gen_phone_number(num_cust_id):
    number_lst = []
    for row in range(0, num_cust_id):
        number_lst.append("(+65) " + str(random.randint(80000000, 99999999)))
    return number_lst


# Create pandas dataframe
def create_df(num_cust_id, current_year):
    # Initialize variables
    person = gen_name_gender_email(num_cust_id)
    nric = gen_nric(num_cust_id, current_year)

    data = {}
    data["custID"] = range(1, num_cust_id+1)
    data["firstName"] = person[0]
    data["lastName"] = person[1]
    data["gender"] = person[2]
    data["email"] = person[3]
    data["nric"] = nric[0]
    data["age"] = nric[1]
    data["address"] = gen_address(num_cust_id)
    data["phoneNumber"] = gen_phone_number(num_cust_id)
    return pd.DataFrame(data=data)


# Generate random variables and push to AWS dynamoDB
def create(num_cust_id, current_year):
    df = create_df(num_cust_id, current_year)
    np = df.to_numpy()

    # Write row by row to dynamoDB
    np = df.to_numpy()
    try:
        for row in np:
            item = {
                'custID': row[0],
                'firstName': row[1],
                'lastName': row[2],
                'gender': row[3],
                'email': row[4],
                'nric': row[5],
                'age': row[6],
                'address': row[7],
                'phoneNumber': row[8]
            }
            table.put_item(Item=item)
        print("Write to {}: Success".format(table_name))
    except:
        e = sys.exc_info()[0]
        print(e)
        print("Write to {}: Fail".format(table_name))

    # Create local csv copy
    df.to_csv("./database/Users.csv", index=False)
    print("Exported Users.csv: Success")
