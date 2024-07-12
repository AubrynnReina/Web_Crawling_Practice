from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from extract import extract
from transform import transform
from load import load
from airflow.utils.db import provide_session
from airflow.models import XCom

@provide_session
def clean_xcom(session=None, **context):
    dag = context["dag"]
    dag_id = dag._dag_id
    session.query(XCom).filter(XCom.dag_id == dag_id).delete()

dag = DAG(
    dag_id='ETL_dag',
    default_args={
        'start_date': days_ago(0),
    },
    schedule_interval='*/2 * * * *',
    catchup=False
)

extract = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform,
    dag=dag,
)

load = PythonOperator(
    task_id='load',
    python_callable=load,
    dag=dag
)

# cleanup_xcom = PythonOperator(
#     task_id='cleanup_xcom',
#     python_callable=cleanup_xcom,
#     dag=dag
# )

delete_xcom = PythonOperator(
    task_id="delete_xcom",
    python_callable = clean_xcom, 
    dag=dag
)

extract >> transform >> load >> delete_xcom
# transform >> [load, load_2] # parallel