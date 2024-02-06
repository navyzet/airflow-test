from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

# Check variables
from airflow.models import Variable

from random import randint
from datetime import datetime

from kubernetes.client import models as k8s

pod_name = Variable.get("FOO", default_var="BAD VALUE")

def _choose_best_model(ti):
    accuracies = ti.xcom_pull(task_ids=[
        'training_model_A',
        'training_model_B',
        'training_model_C'
    ])
    best_accuracy = max(accuracies)
    if (best_accuracy > 8):
        return 'accurate'
    return 'inaccurate'


def _training_model():
    print(pod_name)
    return randint(1, 10)

def resource_configure(mem_request=None, cpu_request=None, mem_limit=None, cpu_limit=None ):
    resource_limits = {}
    resource_requests = {}
    if mem_limit is not None:
        resource_limits["memory"] = mem_limit
    if cpu_limit is not None:
        resource_limits["cpu"] = cpu_limit
    if mem_request is not None:
        resource_requests["memory"] = mem_request
    if cpu_request is not None:
        resource_requests["cpu"] = cpu_request
    return_executor_config_template = {
        "pod_override": k8s.V1Pod(
            spec=k8s.V1PodSpec(
                containers=[
                    k8s.V1Container(
                        name="base",
                        resources=k8s.V1ResourceRequirements(
                            requests = resource_requests,
                            limits = resource_limits
                        )
                    )
                ]
            )
        )
    }
    return return_executor_config_template

with (DAG("my_dag", start_date=datetime(2021, 1, 1),
         schedule_interval="@daily", catchup=False) as dag):
    executor_config_template = resource_configure(mem_request="128Mi", cpu_request="50m", mem_limit="256Mi")
    training_model_A = PythonOperator(
        task_id="training_model_A",
        python_callable=_training_model,
        executor_config = resource_configure(mem_request="256Mi", cpu_request="100m",
                                             mem_limit="400Mi", cpu_limit="200m")
    )

    training_model_B = PythonOperator(
        task_id="training_model_B",
        python_callable=_training_model
    )

    training_model_C = PythonOperator(
        task_id="training_model_C",
        python_callable=_training_model
    )

    choose_best_model = BranchPythonOperator(
        task_id="choose_best_model",
        python_callable=_choose_best_model
    )

    accurate = BashOperator(
        task_id="accurate",
        bash_command="echo 'accurate'"
    )

    inaccurate = BashOperator(
        task_id="inaccurate",
        bash_command="echo 'inaccurate'"
    )

    [training_model_A, training_model_B, training_model_C] >> choose_best_model >> [accurate, inaccurate]
