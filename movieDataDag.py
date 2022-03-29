import json
from textwrap import dedent

import pendulum
import requests
from airflow import DAG
from airflow.operators.python import PythonOperator
from bs4 import BeautifulSoup



with DAG(
    'dh_movie_data_etl_dag_sample',
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={'retries': 2},
    # [END default_args]
    description='DH MOVIE DATA DAG Sample',
    # schedule_interval='@weekly',
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 1, 1, tz="UTC"),
    catchup=False,
    tags=['DH MOVIE DATA DAG Sample'],
) as dag:
    # [END instantiate_dag]
    # [START documentation]
    dag.doc_md = __doc__
    # [END documentation]

    # [START extract_function]
    def extract(**kwargs):
        ti = kwargs['ti']
        url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
        response = requests.get(url=url)
        ti.xcom_push('movie_data', response.text)

    # [END extract_function]

    # [START transform_function]
    def transform(**kwargs):
        ti = kwargs['ti']
        extract_data_string = ti.xcom_pull(task_ids='extract', key='movie_data')

        soup = BeautifulSoup(extract_data_string, 'lxml')
        info_items = soup.find_all('div', 'release_info')

        data = []
        for item in info_items:
            name = item.find('div', 'release_movie_name').a.text.strip()
            english_name = item.find('div', 'en').a.text.strip()
            release_time = item.find('div', 'release_movie_time').text.split('：')[-1].strip()
            level = item.find('div', 'leveltext').span.text.strip()

            data.append({'name': name, 'english_name': english_name, 'release_time': release_time, 'level': level})


        json_string = json.dumps(data)
        ti.xcom_push('movie_ranking', json_string)

    # [END transform_function]

    # [START load_function]
    def load(**kwargs):
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='transform', key='movie_ranking')
        movie_data = json.loads(data)

        print(movie_data)

        with open('./movies.txt', 'w') as f:
            for data in movie_data:
                f.write('{}, {}, {} , {} \n'.format(data['name'], data['english_name'], data['release_time'], data['level']))

    # [END load_function]

    # [START main_flow]
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    """
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    """
    )

    extract_task >> transform_task >> load_task

