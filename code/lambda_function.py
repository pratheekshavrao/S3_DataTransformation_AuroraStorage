import boto3
import logging
import csv
import io

s3_client = boto3.client('s3')
rds_client = boto3.client('rds-data')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#currency conversion dictionary
currency_conversion = {'USD': 1, 'CAD': 0.79, 'MXN': 0.05}

#database declarations
database_name = 'test_rds'
secret_store_arn = 'Insert ARN here'
db_cluster_arn = 'Insert ARN here'

def process_record(record):
#bill amount is the last field in the list
    id, company_name, country, city, product_line, item, bill_date, currency, bill_amount = record
    bill_amount = float(bill_amount)
 
#convert curreny to USD
    bill_amount_usd = 0
    rate = currency_conversion[currency]
    bill_amount_usd = bill_amount * rate
    print(f"currency: {currency}, bill amount: {bill_amount} , usd bill amount: {bill_amount_usd}")
    
#SQL statement for inserting into database
    sql_statement = ("INSERT IGNORE INTO billing_data "
                        "(id, company_name, country, city, product_line, item, bill_date, currency, bill_amount, bill_amount_usd) "
                        "VALUES (:id, :company_name, :country, :city, :product_line, :item, :bill_date, :currency, :bill_amount, :bill_amount_usd)"
    )
#SQL parameters for SQL statement
    sql_parameters = [
        {'name': 'id', 'value': {'stringValue': id}},
        {'name': 'company_name', 'value': {'stringValue': company_name}},
        {'name': 'country', 'value': {'stringValue': country}},
        {'name': 'city', 'value': {'stringValue': city}},
        {'name': 'product_line', 'value': {'stringValue': product_line}},
        {'name': 'item', 'value': {'stringValue': item}},
        {'name': 'bill_date', 'value': {'stringValue': bill_date}},
        {'name': 'currency', 'value': {'stringValue': currency}},
        {'name': 'bill_amount', 'value': {'doubleValue': bill_amount}},
        {'name': 'bill_amount_usd', 'value': {'doubleValue': bill_amount_usd}}
        ]
        
# Execute the SQL Statement and log the response
    response = execute_statement(sql_statement, sql_parameters)
    logger.info(f"SQL Execution response {response}")
            
def execute_statement(sql, sql_parameters):
    try:
        response = rds_client.execute_statement(
            secretArn = secret_store_arn,
            database = database_name,
            resourceArn = db_cluster_arn,
            sql = sql,
            parameters = sql_parameters
            )
        
    except Exception as e:
        logger.error(f"Could not connect to Aurora Serverless MySQL instance: {e}")
        return None
        
    return response
    
    
    
    
def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    csv_file = event['Records'][0]['s3']['object']['key']
    
    obj = s3_client.get_object(Bucket = bucket_name,Key = csv_file)
    data = obj['Body'].read().decode('utf-8').splitlines()

#read each record and call process record function    
    for record in csv.reader(data[1:], delimiter = ','):
        process_record(record)
    
    logger.info("Lambda has finished execution")
