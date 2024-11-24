from obs import CreateBucketHeader, HeadPermission
from obs import ObsClient
import os
import traceback
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
start_date = datetime(2024, 11, 17)
default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}


# Create an ObsClient instance
def create_bucket():

    # Initialize credentials
    ak = 'MBJPQNO9ERO1VTQAJVG1'  # Replace with your Access Key ID
    sk = '7rMeNDOW1AN0wAFguPFx4gOYCXVLdbXFzsKQEx3m'  # Replace with your Secret Access Key
    server = 'https://obs.cn-north-4.myhuaweicloud.com'  # Replace with your endpoint


    # Create an ObsClient instance.
    obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)
    try:
        # Specify the additional headers to create a private bucket that is in the Standard storage class and supports multi-AZ storage.
        header = CreateBucketHeader(aclControl=HeadPermission.PRIVATE, storageClass="STANDARD", availableZone="3az")
        # Specify the region where you want to create the bucket. ap-southeast-1 is used here as an example. The region must be the one you specified in the endpoint.
        location = "cn-north-4"
        # Specify the region where you want to create the bucket. The region must be the one you specified in the endpoint.
        location = "cn-north-4"
        bucketName = "hkexend"
        # Create the bucket.
        resp = obsClient.createBucket(bucketName, header, location)
        # If status code 2xx is returned, the API call succeeds. Otherwise, the API call fails.
        if resp.status < 300:
            print('Create Bucket Succeeded')
            print('requestId:', resp.requestId)
        else:
            print('Create Bucket Failed')
            print('requestId:', resp.requestId)
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
    except:
        print('Create Bucket Failed')
        print(traceback.format_exc())
with DAG('create_bucket', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    create_bucket_task = PythonOperator(
        task_id='save_date',
        python_callable=create_bucket,
        dag=dag
    )