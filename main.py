import login
import bankinfo
import transaction
import users
import dynamodb
import config

# Import from config
table_names = config.TABLE_NAMES
table_infos = config.TABLE_INFO
num_cust_id = config.CUSTOMER
num_transaction = config.TRANSACTION
current_year = config.CURRENT_YEAR
start_date = config.START_DATE
end_date = config.END_DATE

# Reset database in AWS
response = dynamodb.reset_table(table_names, table_infos)

# Create database
if response:
    login.create(num_cust_id)
    users.create(num_cust_id, current_year)
    bankinfo.create(num_cust_id)
    transaction.create(start_date, end_date, num_cust_id, num_transaction)
else:
    print("Database not created")