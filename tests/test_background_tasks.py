import os
from unittest import mock

import csv_detective
import pytest

from udata_analysis_service.background_tasks import manage_resource

pytestmark = pytest.mark.asyncio


async def test_manage_resource_send_produce_message(mocker):
    mocker.patch.dict(os.environ, {
        'CSV_DETECTIVE_REPORT_BUCKET': 'detective-bucket',
        'CSV_DETECTIVE_REPORT_FOLDER': 'report',
        'TABLESCHEMA_BUCKET': '',
        'TABLESCHEMA_FOLDER': '',
        'KAFKA_HOST': 'localhost',
        'KAFKA_PORT': '9092',
        'UDATA_INSTANCE_NAME': 'udata'
    })
    mocker.patch('boto3.client')
    routine = mocker.patch('udata_analysis_service.background_tasks.routine_minio')
    produce = mocker.patch('udata_analysis_service.background_tasks.produce')

    manage_resource(
        dataset_id = 'dataset_id',
        resource_id = 'resource_id',
        resource_location = {'netloc': 'netloc', 'bucket': 'bucket', 'key': 'key'},
        minio_user = 'minio_user',
        minio_pwd = 'minio_pwd',
    )

    produce.assert_called_with(
        'localhost:9092',
        'udata.resource.analysed',
        service='csvdetective',
        key_id='resource_id',
        document={
            'url': 'netloc',
            'bucket': 'detective-bucket',
            'key': 'report/dataset_id/resource_id.json'
        },
        meta={'dataset_id': 'dataset_id'},
    )
