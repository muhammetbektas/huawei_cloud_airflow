from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
start_date = datetime(2024, 11, 17)
default_args = {
    'owner': 'airflow',
    'start_date': start_date,
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}
with DAG('my_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:
    t0 = BashOperator(task_id='ls_data', bash_command='echo "Listing data..."', retries=2, retry_delay=timedelta(seconds=15))
    t1 = BashOperator(task_id='download_data',
                      bash_command='echo "Downloading data..."',
                      retries=2, retry_delay=timedelta(seconds=15))
    t2 = BashOperator(task_id='check_file_exists', bash_command='echo "Checking data..."',
                      retries=2, retry_delay=timedelta(seconds=15))
    t3 = BashOperator(task_id='hello_world_task',bash_command='python -c "print(\'Hello, world!\')"',dag=dag)

    t0 >> t1 >> t2 >> t3