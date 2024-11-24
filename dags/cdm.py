from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcdm.v1 import *
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime


start_date = datetime(2024, 11, 17)
default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

 # Replace with your region's CDM endpoint
job_id = "1ds2g3fdgf"

def start_cdm_job():
    
    ak = "MBJPQNO9ERO1VTQAJVG1"
    sk = "7rMeNDOW1AN0wAFguPFx4gOYCXVLdbXFzsKQEx3m"
    projectId = "9937744dea504761a47d4d18824ac963"
    job_id = "test"
    endpoint = "https://cdm.cn-north-4.myhuaweicloud.com" 

    credentials = BasicCredentials(ak, sk, projectId) \

    client = CdmClient.new_builder() \
        .with_credentials(credentials) \
        .with_endpoint(endpoint) \
        .build()

    try:
        request = StartJobRequest()
        request.cluster_id = "test_id"
        request.job_name = "test"
        request.body = CdmStartJobReq(
            variables={}
        )
        response = client.start_job(request)
        print(response)
    except exceptions.ClientRequestException as e:
        print(e.status_code)
        print(e.request_id)
        print(e.error_code)
        print(e.error_msg)



dag = DAG(
    "trigger_cdm_task",
    default_args=default_args,
    description="DAG to trigger Huawei Cloud CDM task",
    schedule_interval=None,  # Trigger manually or set a cron schedule
)

# Add a task to the DAG
trigger_task = PythonOperator(
    task_id="trigger_cdm_task",
    python_callable=start_cdm_job,
    provide_context=True,
    dag=dag,
)