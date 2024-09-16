from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'your_name',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
}

pod_args = [Variable.get("HOSTNAME", default_var="BAD VALUE")]

dag = DAG(
    'kubernetes_pod_operator_example_2',
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
    cmds=["ls", "-hla", "/opt/airflow/pod_templates"],
    # arguments=["Hello, Airflow!"],  # Command and arguments to run in the pod
    arguments=pod_args,  # Command and arguments to run in the pod
    labels={"app": "myapp"},
    get_logs=True,
    dag=dag,
    pod_template_file='/opt/airflow/pod_templates/pod_template_file.yaml',
    # kubernetes_conn_id="old",
    # service_account_name='airflow-service-account',
)

if __name__ == "__main__":
    dag.cli()
