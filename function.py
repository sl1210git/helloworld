import boto3
import psycopg2

def lambda_handler(event, context):
    # establish Redshift connection
    redshift_endpoint = "your-redshift-endpoint"
    redshift_user = "your-redshift-username"
    redshift_pass = "your-redshift-password"
    port = 5439
    dbname = "your-db-name"
    
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=redshift_user,
            password=redshift_pass,
            port=port,
            host=redshift_endpoint
        )
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        raise e

    # extracting bucket and key info from the S3 event
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 

    print(f'Received file: {key} from bucket: {bucket}')

    # call Redshift Stored Procedure
    try:
        cursor = conn.cursor()
        sql = "CALL your_stored_procedure();"
        cursor.execute(sql)
        cursor.close()
        conn.commit()
    except Exception as e:
        print(f"Error executing RedShift command: {e}")
        raise e
    finally:
        conn.close()

    print("Stored procedure executed successfully.")
    return {
        'statusCode': 200,
        'body': f'Successfully processed S3 object {key} from bucket {bucket} and executed stored procedure.'
    }
