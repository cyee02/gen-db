# Number of customer/ number of groups
CUSTOMER=20

# Number of transaction < 89,999
TRANSACTION=500

# Transaction date range (String, ddmmyyyyhhmm)
START_DATE='010120210000'
END_DATE='070520210600'

# Current year
CURRENT_YEAR=2021

# For table creation
TABLE_NAMES = ['TT4_BankInfo', 'TT4_Login', 'TT4_Transaction', 'TT4_Users']
TABLE_INFO = [
    [
        {
            'AttributeName': 'bankInfoID',
            'AttributeType': 'N',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'custID',
            'AttributeType': 'N',
            'KeyType': 'RANGE'
        }
    ],
    [
        {
            'AttributeName': 'custID',
            'AttributeType': 'N',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'userName',
            'AttributeType': 'S',
            'KeyType': 'RANGE'
        }
    ],
    [
        {
            'AttributeName': 'transactionID',
            'AttributeType': 'N',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'custID',
            'AttributeType': 'N',
            'KeyType': 'RANGE'
        }
    ],

    [
        {
            'AttributeName': 'custID',
            'AttributeType': 'N',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'firstName',
            'AttributeType': 'S',
            'KeyType': 'RANGE'
        }
    ]
]