from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'navyzet',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

dag = DAG(
    'sleep',
    default_args=default_args,
    description='A simple example DAG with KubernetesPodOperator',
    schedule_interval=None,  # You can set the schedule_interval as needed
    catchup=False,
)

task = KubernetesPodOperator(
    task_id='sleep',
    name='sleep-2-min',
    namespace='airflow',  # Change to your desired Kubernetes namespace
    image='ubuntu:latest',  # Specify the Docker image to run in the pod
    cmds=["bash", "-c"],
    # arguments=["Hello, Airflow!"],  # Command and arguments to run in the pod
    arguments=["for i in {0..12}; do echo seconds: $(($i * 10)); sleep 10; done"],  # Command and arguments to run in the pod
    labels={"app": "myapp"},
    get_logs=True,
    dag=dag,
)

if __name__ == "__main__":
    dag.cli()
