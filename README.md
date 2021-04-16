**Objective**
Randomly generate 4 table, push them into dynamoDB and creates csv copy in the database directory

**Info**
Uses boto3 client to interact with AWS
Run "aws configure" to link up with your AWS account

Tables generated:
1. BankInfo
2. Login
3. Transaction
4. Users

**Note**
Configure variables in config.py and trigger run.sh

_Pipeline to be updated to make database creation more flexible_