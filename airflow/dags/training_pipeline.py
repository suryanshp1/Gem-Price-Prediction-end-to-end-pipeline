from __future__ import annotations
from textwrap import dedent
import pendulum
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator
from src.pipeline.training_pipeline import TrainingPipeline


training_pipeline = TrainingPipeline()

with DAG(
    dag_id="gemstone_training_pipeline",
    default_args={
        "retries": 3,
    },
    description="Training pipeline for gemstone dataset",
    schedule="@weekly",
    start_date=pendulum.datetime(2024, 10, 6, tz="UTC"),
    catchup=False,
    tags=["training", "machine_learning", "classification"],
) as dag:
    
    dag.doc_md = __doc__

    def data_ingestion(**kwargs):
        ti = kwargs.get("ti")
        train_data_path, test_data_path = training_pipeline.start_data_ingestion()
        ti.xcom_push(key="data_ingestion_artifact", value={"train_data_path": train_data_path, "test_data_path": test_data_path})

    def data_transformation(**kwargs):
        ti = kwargs.get("ti")
        data_ingestion_artifact = ti.xcom_pull(key="data_ingestion_artifact", task_ids="data_ingestion")
        train_arr, test_arr = training_pipeline.start_data_transformation(data_ingestion_artifact.get("train_data_path"), data_ingestion_artifact.get("test_data_path"))
        train_arr=train_arr.tolist()
        test_arr=test_arr.tolist()
        ti.xcom_push(key="data_transformation_artifact", value={"train_arr": train_arr, "test_arr": test_arr})

    def model_trainer(**kwargs):
        import numpy as np

        ti = kwargs.get("ti")
        data_transformation_artifact = ti.xcom_pull(key="data_transformation_artifact", task_ids="data_transformation")

        train_arr = np.array(data_transformation_artifact.get("train_arr"))
        test_arr = np.array(data_transformation_artifact.get("test_arr"))

        training_pipeline.start_model_trainer(train_arr, test_arr)

    def push_data_to_azureblob(**kwargs):
        # first configure azure cli in environment
        account_name = "<account-name>"
        destination_path = "<destination-path>"
        source_path = "<source-path>"
        subprocess.run(f"az storage blob upload-batch --account-name {account_name} --destination-path {destination_path} --source {source_path}", shell=False)

    data_ingestion_task = PythonOperator(
        task_id="data_ingestion",
        python_callable=data_ingestion,
    )
    data_ingestion_task.doc_md = dedent(
        """\
    #### Ingestion task
    this task creates a train and test file.
    """
    )

    data_transformation_task = PythonOperator(
        task_id="data_transformation",
        python_callable=data_transformation,
    )
    data_transformation_task.doc_md = dedent(
        """\
    #### Transformation task
    this task performs the transformation
    """
    )

    model_trainer_task = PythonOperator(
        task_id="model_trainer",
        python_callable=model_trainer,
    )
    model_trainer_task.doc_md = dedent(
        """\
    #### model trainer task
    this task perform training
    """
    )


    # push_data_to_azureblob_task = PythonOperator(
    #     task_id="push_data_to_azureblob",
    #     python_callable=push_data_to_azureblob,
    # )

    # push_data_to_azureblob_task.doc_md = dedent(
    #     """\
    # #### push data to azureblob task
    # this task push data to azureblob
    # """
    # )

    data_ingestion_task >> data_transformation_task >> model_trainer_task