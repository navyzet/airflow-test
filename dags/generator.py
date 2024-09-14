# import pendulum
# 
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# 
# DAGS_COUNT = 350
# 
# for i in range(DAGS_COUNT):
#     id = f"debug_{i}"
#     with DAG(
#         id,
#         schedule="@daily",
#         start_date=pendulum.today("UTC").add(days=-2),
#         catchup=False,
#         max_active_runs=1,
#         max_active_tasks=1,
#     ) as dag:
#         PythonOperator(
#             task_id=id,
#             python_callable=print,
#             op_args=(f"Hello from debug {i}",)
#         )
# 
#     globals()[id] = dag
# 
