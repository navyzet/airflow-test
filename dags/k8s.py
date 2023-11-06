from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable

default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'retries': 1,
    'start_date': None
}

pod_args = [Variable.get("HOSTNAME", default_var="BAD VALUE")]

dag = DAG(
    'simple_kubernetes_pod_operator_example',
    default_args=default_args,
    description='A simple example DAG with KubernetesPodOperator',
    schedule_interval=None,  # You can set the schedule_interval as needed
    catchup=False,
)

task = KubernetesPodOperator(
    task_id='run_kubernetes_pod_task',
    name='run-k8s-pod-task',
    namespace='default',  # Change to your desired Kubernetes namespace
    image='ubuntu:latest',  # Specify the Docker image to run in the pod
    cmds=["echo"],
    # arguments=["Hello, Airflow!"],  # Command and arguments to run in the pod
    arguments=pod_args,  # Command and arguments to run in the pod
    labels={"app": "myapp"},
    get_logs=True,
    dag=dag,
)

if __name__ == "__main__":
    dag.cli()