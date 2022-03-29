import json
from textwrap import dedent

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG(
    'dh_print_dag_sample',
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={'retries': 2},
    # [END default_args]
    description='DH Print DAG Sample',
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=['DH Print DAG Sample'],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]


    def task_01(**kwargs):
        print('task_01 is running')

    # [END extract_function]

    # [START transform_function]
    def task_02(**kwargs):
        print('task_02 is running')

    # [END transform_function]

    # [START load_function]
    def task_03(**kwargs):
        print('task_02 is running')

    # [END load_function]

    # [START main_flow]
    airflow_task01 = PythonOperator(
        task_id='task_01',
        python_callable=task_01,
    )
    airflow_task01.doc_md = dedent(
        """\
    #### Extract task
   
    """
    )

    airflow_task02 = PythonOperator(
        task_id='task_02',
        python_callable=task_02,
    )
    airflow_task02.doc_md = dedent(
        """\
    #### Transform task
   
    """
    )

    airflow_task03 = PythonOperator(
        task_id='task_03',
        python_callable=task_03,
    )
    airflow_task03.doc_md = dedent(
        """\
    #### Load task
  
    """
    )

    airflow_task01 >> airflow_task02 >> airflow_task03
