from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Функция, которую будет выполнять task
def simple_task(**kwargs):
    print("This is a simple task.")

# Определение DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 29),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'single_task_dag',
    default_args=default_args,
    description='A DAG with a single task',
    schedule_interval=timedelta(days=1),
)

# Определение задачи
simple_task = PythonOperator(
    task_id='simple_task',
    python_callable=simple_task,
    dag=dag,
)
