# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago

#defining DAG arguments

default_args = {
    'owner': 'Juliano',
    'start_date': days_ago(0),
    'email': ['juliano@someemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# define the DAG
dag = DAG(
    dag_id='ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

# define the tasks

# define the first task

unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='tar -xvzf /home/project/tolldata.tgz -C /home/project/airflow/dags/finalassignment',
    dag=dag,
)

#define  second task

extract_data_from_csv = BashOperator(
    task_id='extract',
    bash_command='cut -f1-4 -d"," vehicle-data.csv > csv_data.csv',
    dag=dag,
)

#define third
extract_data_from_tsv = BashOperator(
    task_id='extract_tsv',
    bash_command='cut -f5-7 -d$"\t" tollplaza-data.tsv > tollplaza1-data.tsv &&  tr "\t" "," < tollplaza1-data.tsv > tsv_data.csv',
    dag=dag,
)

#define fourth
extract_data_from_fixed_width = BashOperator(
    task_id='extract_width',
    bash_command='cut -f6-7 -d" " vehicle-data.csv > vehicle1-data.csv && tr " " "," < vehicle1-data.csv > fixed_widht_data.csv',
    dag=dag,
)


#define fifth
consolidate_data = BashOperator(
    task_id='consolidate',
    bash_command='paste csv_data.csv tsv_data.csv fixed_width_data.csv > extracted_data.csv ',
    dag=dag,
)

#define sixth
transform_data = BashOperator(
    task_id='transform',
    bash_command='cut -f4 -d"," extracted-data.csv > csv_toupper.csv && tr "[a-z]" "[A-Z]" < csv_toupper > transformed_data.csv',
    dag=dag,
)

# task pipeline

unzip_data >> extract_data_from_csv >> 	extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
